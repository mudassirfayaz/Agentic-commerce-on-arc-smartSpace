"""
Payment execution system for SmartSpace.

Handles automatic payment for approved API requests using Arc blockchain and USDC.

Payment Flow:
1. Request approved → Reserve budget (hold USDC)
2. Execute API call → Get actual cost
3. Commit payment → Transfer USDC to provider
4. Release any excess reservation
5. Log payment transaction

This enables true pay-per-use AI commerce:
- Users only pay for actual usage
- No monthly subscriptions
- Automatic payment on approval
- Blockchain receipts for every transaction
"""

from .payment_executor import (
    PaymentExecutor,
    PaymentReservation,
    PaymentResult,
    PaymentStatus,
)

__all__ = [
    "PaymentExecutor",
    "PaymentReservation",
    "PaymentResult",
    "PaymentStatus",
]
