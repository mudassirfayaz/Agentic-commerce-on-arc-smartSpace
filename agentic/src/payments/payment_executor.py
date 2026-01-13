"""
Payment Execution System

Handles automatic payment for approved API requests.

Payment Flow:
1. ESTIMATE: Brain estimates cost (can be +/- actual amount)
2. RESERVE: Brain calls backend -> Backend locks ESTIMATED amount on blockchain
3. EXECUTE: Brain makes API call and gets actual cost
4. COMMIT: Brain logs actual vs estimated difference (no refund on blockchain)

Architecture:
- Brain: Calls payment functions (reserve, commit)
- Backend: Executes blockchain transactions (Arc + USDC)
- Backend: Returns transaction hashes and status to brain
- Brain: Logs payment events in audit trail

Cost Variance:
- Estimated cost may be higher or lower than actual
- Users pay ESTIMATED amount (single blockchain transaction)
- No refunds on blockchain (avoids gas fees)
- Backend cost estimator aims for accuracy
- Differences logged for transparency and estimator improvement

This enables:
- Pay-per-use (no monthly subscriptions)
- Automatic payment on approval
- Single blockchain transaction (lower gas fees)
- Accurate cost estimation (backend improves over time)
- Transparent logging of estimate vs actual
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any
import logging
import requests

from config import Config

logger = logging.getLogger(__name__)


class PaymentStatus(str, Enum):
    """Payment transaction status."""
    PENDING = "pending"
    RESERVED = "reserved"
    COMMITTED = "committed"
    FAILED = "failed"
    REFUNDED = "refunded"
    CANCELLED = "cancelled"


@dataclass
class PaymentReservation:
    """
    Payment reservation for a request.
    
    Reserves (pays) estimated amount via blockchain transaction.
    This is a SINGLE payment transaction - no refunds to avoid gas fees.
    """
    reservation_id: str
    request_id: str
    user_id: str
    project_id: str
    
    # Amount details
    estimated_amount: float  # What user pays (single blockchain TX)
    currency: str = "USDC"
    
    # Status
    status: PaymentStatus = PaymentStatus.RESERVED
    
    # Timestamps
    reserved_at: datetime = field(default_factory=datetime.utcnow)
    
    # Blockchain
    tx_hash: Optional[str] = None  # Single payment transaction
    block_number: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "reservation_id": self.reservation_id,
            "request_id": self.request_id,
            "user_id": self.user_id,
            "project_id": self.project_id,
            "estimated_amount": self.estimated_amount,
            "currency": self.currency,
            "status": self.status.value,
            "reserved_at": self.reserved_at.isoformat(),
            "tx_hash": self.tx_hash,
            "block_number": self.block_number,
        }


@dataclass
class PaymentResult:
    """
    Result of payment execution.
    
    Contains details of the payment and actual API cost.
    User paid estimated amount - actual may differ (+/- variance).
    No refunds on blockchain to avoid gas fees.
    """
    payment_id: str
    request_id: str
    reservation_id: str
    
    # Amount details
    estimated_amount: float  # What user paid (blockchain TX)
    actual_amount: float     # What API actually cost
    variance_amount: float   # Difference (positive = overpaid, negative = underpaid)
    variance_percent: float  # Percentage difference
    currency: str = "USDC"
    
    # Payment details
    status: PaymentStatus = PaymentStatus.COMMITTED
    provider: str = ""
    
    # Timestamps
    initiated_at: datetime = field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    
    # Blockchain
    payment_tx_hash: Optional[str] = None  # Single payment transaction
    block_number: Optional[int] = None
    
    # Error handling
    error: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "payment_id": self.payment_id,
            "request_id": self.request_id,
            "reservation_id": self.reservation_id,
            "estimated_amount": self.estimated_amount,
            "actual_amount": self.actual_amount,
            "variance_amount": self.variance_amount,
            "variance_percent": self.variance_percent,
            "currency": self.currency,
            "status": self.status.value,
            "provider": self.provider,
            "initiated_at": self.initiated_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "payment_tx_hash": self.payment_tx_hash,
            "block_number": self.block_number,
            "error": self.error,
        }


class PaymentExecutor:
    """
    Handles automatic payment execution for approved API requests.
    
    Payment Model:
    1. Backend cost estimator provides estimated cost
    2. User pays estimated amount (single blockchain TX)
    3. API executes and returns actual cost
    4. Brain logs estimate vs actual variance
    5. No refunds on blockchain (avoids gas fees)
    
    Cost Variance:
    - Estimate may be +/- actual cost
    - Backend improves estimator accuracy over time
    - Transparency: all variances logged
    - Users understand they pay estimated amount
    
    This ensures:
    - Single blockchain transaction (lower gas fees)
    - Fast payment execution
    - No refund complexity
    - Clear cost expectations
    """
    
    def __init__(self):
        """Initialize payment executor."""
        self.config = Config()
    
    async def reserve_payment(
        self,
        request_id: str,
        user_id: str,
        project_id: str,
        estimated_amount: float,
        buffer_percent: float = 0.0  # No buffer needed - pay estimate
    ) -> PaymentReservation:
        """
        Pay estimated amount for request (single blockchain transaction).
        
        Brain calls this, then Backend executes payment on blockchain, then Backend responds.
        
        Payment Model:
        - User pays ESTIMATED amount upfront (single TX)
        - No refunds (avoid gas fees and multiple TXs)
        - Backend cost estimator aims for accuracy
        - Variance (estimate vs actual) logged for transparency
        
        Backend responsibilities:
        - Get accurate cost estimate from cost estimator
        - Execute blockchain payment transaction (USDC transfer)
        - Return transaction hash and confirmation
        
        Brain responsibilities:
        - Call this function with estimated cost
        - Receive and log blockchain transaction details
        - Later compare estimate vs actual for logging
        
        Args:
            request_id: Request identifier
            user_id: User identifier
            project_id: Project identifier
            estimated_amount: Estimated cost in USDC (from backend estimator)
            buffer_percent: Unused (kept for compatibility)
            
        Returns:
            PaymentReservation with blockchain transaction details from backend
            
        Raises:
            InsufficientFundsError: If user doesn't have enough balance
            PaymentError: If blockchain transaction fails
        """
        try:
            # Call backend to execute blockchain payment
            url = self.config.get_endpoint('payments', 'reserve')
            response = requests.post(
                url,
                json={
                    'request_id': request_id,
                    'user_id': user_id,
                    'project_id': project_id,
                    'estimated_amount': estimated_amount,
                    'currency': 'USDC'
                },
                timeout=self.config.API_TIMEOUT
            )
            response.raise_for_status()
            
            # Backend responds with blockchain transaction details
            data = response.json()
            
            reservation = PaymentReservation(
                reservation_id=data['reservation_id'],
                request_id=request_id,
                user_id=user_id,
                project_id=project_id,
                estimated_amount=estimated_amount,
                status=PaymentStatus.RESERVED,
                tx_hash=data.get('tx_hash'),  # Payment TX from backend
                block_number=data.get('block_number'),  # Block number from backend
            )
            
            logger.info(
                f"Payment executed: ${estimated_amount:.4f} USDC for {request_id} | "
                f"TX: {reservation.tx_hash}"
            )
            
            return reservation
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 402:
                raise InsufficientFundsError(f"Insufficient funds for {user_id}")
            logger.error(f"Payment failed: {e}")
            raise PaymentError(f"Payment failed: {e}")
            
        except Exception as e:
            logger.error(f"Payment error: {e}")
            raise PaymentError(f"Payment error: {e}")
    
    async def commit_payment(
        self,
        reservation: PaymentReservation,
        actual_amount: float,
        provider: str,
        recipient_address: Optional[str] = None
    ) -> PaymentResult:
        """
        Log actual cost vs estimated amount (no additional blockchain TX).
        
        Payment already completed in reserve_payment() - this just logs variance.
        
        Brain responsibilities:
        - Call this function with actual cost from API
        - Calculate and log estimate vs actual variance
        - Update audit trail with cost accuracy
        
        Backend responsibilities:
        - Store variance data for estimator improvement
        - Update payment record with actual cost
        
        Cost Variance:
        - Positive variance: User overpaid (estimate > actual)
        - Negative variance: User underpaid (estimate < actual)
        - Zero variance: Perfect estimate
        
        Args:
            reservation: Payment reservation from reserve_payment()
            actual_amount: Actual cost from API execution
            provider: Provider name (openai, anthropic, etc.)
            recipient_address: Unused (kept for compatibility)
            
        Returns:
            PaymentResult with variance analysis
        """
        try:
            # Calculate variance
            variance_amount = reservation.estimated_amount - actual_amount
            variance_percent = (variance_amount / reservation.estimated_amount * 100) if reservation.estimated_amount > 0 else 0
            
            # Call backend to log actual cost and variance
            url = self.config.get_endpoint('payments', 'commit')
            response = requests.post(
                url,
                json={
                    'reservation_id': reservation.reservation_id,
                    'request_id': reservation.request_id,
                    'estimated_amount': reservation.estimated_amount,
                    'actual_amount': actual_amount,
                    'variance_amount': variance_amount,
                    'variance_percent': variance_percent,
                    'provider': provider,
                    'currency': 'USDC'
                },
                timeout=self.config.API_TIMEOUT
            )
            response.raise_for_status()
            
            # Backend responds with payment completion details
            data = response.json()
            
            result = PaymentResult(
                payment_id=data['payment_id'],
                request_id=reservation.request_id,
                reservation_id=reservation.reservation_id,
                estimated_amount=reservation.estimated_amount,
                actual_amount=actual_amount,
                variance_amount=variance_amount,
                variance_percent=variance_percent,
                currency='USDC',
                status=PaymentStatus.COMMITTED,
                provider=provider,
                payment_tx_hash=reservation.tx_hash,  # Same TX from reserve
                block_number=reservation.block_number,
                completed_at=datetime.utcnow(),
            )
            
            # Log with variance info
            if variance_amount > 0:
                logger.info(
                    f"Payment completed: ${reservation.estimated_amount:.4f} USDC to {provider} | "
                    f"Actual: ${actual_amount:.4f} (saved ${variance_amount:.4f}, {variance_percent:.1f}%) | "
                    f"TX: {result.payment_tx_hash}"
                )
            elif variance_amount < 0:
                logger.info(
                    f"Payment completed: ${reservation.estimated_amount:.4f} USDC to {provider} | "
                    f"Actual: ${actual_amount:.4f} (over by ${abs(variance_amount):.4f}, {abs(variance_percent):.1f}%) | "
                    f"TX: {result.payment_tx_hash}"
                )
            else:
                logger.info(
                    f"Payment completed: ${reservation.estimated_amount:.4f} USDC to {provider} | "
                    f"Perfect estimate! | TX: {result.payment_tx_hash}"
                )
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to log payment completion: {e}")
            raise PaymentError(f"Payment logging error: {e}")
    
    async def get_payment_status(
        self,
        payment_id: str
    ) -> Dict[str, Any]:
        """
        Get status of a payment transaction.
        
        Args:
            payment_id: Payment identifier
            
        Returns:
            Payment status details from backend
        """
        try:
            url = self.config.get_endpoint('payments', 'status', payment_id=payment_id)
            response = requests.get(url, timeout=self.config.API_TIMEOUT)
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            logger.error(f"Failed to get payment status: {e}")
            return {"status": "unknown", "error": str(e)}


# Custom Exceptions

class PaymentError(Exception):
    """Base payment error."""
    pass


class InsufficientFundsError(PaymentError):
    """User has insufficient funds for payment."""
    pass
