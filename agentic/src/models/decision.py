"""
Approval Decision Models

Defines the structure of decisions made by the agentic system.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any
import uuid
import requests
import logging

from ..config import config

logger = logging.getLogger(__name__)


class DecisionStatus(Enum):
    """Possible decision outcomes"""
    APPROVE = "approve"
    REJECT = "reject"
    ESCALATE = "escalate"  # Escalate to human for review
    QUARANTINE = "quarantine"  # Hold for investigation


class DecisionReason(Enum):
    """Categorized reasons for decisions"""
    # Approval reasons
    ROUTINE_REQUEST = "routine_request"
    LOW_RISK_LOW_COST = "low_risk_low_cost"
    WITHIN_POLICY = "within_policy"
    
    # Rejection reasons
    INSUFFICIENT_BUDGET = "insufficient_budget"
    POLICY_VIOLATION = "policy_violation"
    UNAUTHORIZED_PROVIDER = "unauthorized_provider"
    UNAUTHORIZED_MODEL = "unauthorized_model"
    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"
    FRAUD_DETECTED = "fraud_detected"
    HIGH_RISK = "high_risk"
    
    # Escalation reasons
    UNCERTAIN = "uncertain"
    HIGH_VALUE = "high_value"
    UNUSUAL_PATTERN = "unusual_pattern"
    EDGE_CASE = "edge_case"


@dataclass
class ApprovalDecision:
    """
    Represents a decision made by the agentic system.
    
    Example (Medical Store - Approved):
        decision = ApprovalDecision(
            request_id="req_abc123",
            status=DecisionStatus.APPROVE,
            reason="Low cost routine query within all policies",
            risk_score=2.0,
            agent_tier="FLASH",
            provider_selected="openai",
            model_selected="gpt-3.5-turbo",
            estimated_cost=0.002,
            actual_cost=0.0018,
            policies_checked=["provider_whitelist", "budget_check", "rate_limit"],
            transaction_hash="0x3f8d2e..."
        )
    """
    
    # Identifiers
    decision_id: str = field(default_factory=lambda: f"dec_{uuid.uuid4().hex[:16]}")
    request_id: str = ""
    
    # Decision outcome
    status: DecisionStatus = DecisionStatus.APPROVE
    reason: str = ""
    reasoning_details: Dict[str, Any] = field(default_factory=dict)
    
    # Risk assessment
    risk_score: float = 0.0  # 1-10 scale
    risk_factors: List[str] = field(default_factory=list)
    
    # Agent info
    agent_tier: str = ""  # "FLASH" or "PRO"
    
    # Provider/Model selection
    provider_selected: str = ""
    model_selected: str = ""
    
    # Cost tracking
    estimated_cost: float = 0.0  # USDC, estimated before execution
    actual_cost: Optional[float] = None  # USDC, actual cost after execution
    cost_variance: Optional[float] = None  # actual - estimated (for anomaly detection)
    
    # Policy compliance
    policies_checked: List[str] = field(default_factory=list)
    policy_violations: List[str] = field(default_factory=list)
    
    # Metadata
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    # Payment execution
    transaction_hash: Optional[str] = None  # Blockchain tx hash for USDC payment
    receipt_id: str = field(default_factory=lambda: f"rcpt_{uuid.uuid4().hex[:12]}")
    
    # Audit trail
    audit_trail_id: Optional[str] = None
    
    # Escalation info (if applicable)
    escalation_reason: Optional[str] = None
    escalation_to: Optional[str] = None  # "human", "admin", etc.
    
    # Additional context
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert decision to dictionary for serialization"""
        return {
            "decision_id": self.decision_id,
            "request_id": self.request_id,
            "status": self.status.value,
            "reason": self.reason,
            "reasoning_details": self.reasoning_details,
            "risk_score": self.risk_score,
            "risk_factors": self.risk_factors,
            "agent_tier": self.agent_tier,
            "provider_selected": self.provider_selected,
            "model_selected": self.model_selected,
            "estimated_cost": self.estimated_cost,
            "actual_cost": self.actual_cost,
            "cost_variance": self.cost_variance,
            "policies_checked": self.policies_checked,
            "policy_violations": self.policy_violations,
            "timestamp": self.timestamp.isoformat(),
            "transaction_hash": self.transaction_hash,
            "receipt_id": self.receipt_id,
            "audit_trail_id": self.audit_trail_id,
            "escalation_reason": self.escalation_reason,
            "escalation_to": self.escalation_to,
            "metadata": self.metadata,
        }
    
    def calculate_cost_variance(self) -> Optional[float]:
        """Calculate variance between estimated and actual cost"""
        if self.actual_cost is not None:
            self.cost_variance = self.actual_cost - self.estimated_cost
            return self.cost_variance
        return None
    
    def is_approved(self) -> bool:
        """Check if decision was approval"""
        return self.status == DecisionStatus.APPROVE
    
    def is_rejected(self) -> bool:
        """Check if decision was rejection"""
        return self.status == DecisionStatus.REJECT
    
    def is_escalated(self) -> bool:
        """Check if decision was escalation"""
        return self.status == DecisionStatus.ESCALATE
    
    @classmethod
    def fetch_from_backend(cls, decision_id: str) -> Optional['ApprovalDecision']:
        """
        Fetch decision from backend.
        
        Args:
            decision_id: Decision identifier
            
        Returns:
            ApprovalDecision object or None if not found
        """
        try:
            url = config.get_endpoint('decisions', 'get_decision', decision_id=decision_id)
            response = requests.get(url, timeout=config.API_TIMEOUT)
            response.raise_for_status()
            data = response.json()
            
            status = DecisionStatus(data.get('status', 'approve'))
            
            return cls(
                decision_id=data['decision_id'],
                request_id=data['request_id'],
                status=status,
                reason=data.get('reason', ''),
                reasoning_details=data.get('reasoning_details', {}),
                risk_score=data.get('risk_score', 0.0),
                risk_factors=data.get('risk_factors', []),
                agent_tier=data.get('agent_tier', ''),
                provider_selected=data.get('provider_selected', ''),
                model_selected=data.get('model_selected', ''),
                estimated_cost=data.get('estimated_cost', 0.0),
                actual_cost=data.get('actual_cost'),
                cost_variance=data.get('cost_variance'),
                policies_checked=data.get('policies_checked', []),
                policy_violations=data.get('policy_violations', []),
                transaction_hash=data.get('transaction_hash'),
                receipt_id=data.get('receipt_id', ''),
                audit_trail_id=data.get('audit_trail_id'),
                escalation_reason=data.get('escalation_reason'),
                escalation_to=data.get('escalation_to'),
                metadata=data.get('metadata', {}),
            )
        except Exception as e:
            logger.error(f"Failed to fetch decision from backend: {e}")
            return None

