"""
User Context and Policy Models

Defines user/project configuration and policies.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any
import requests
import logging

from ..config import config

logger = logging.getLogger(__name__)


@dataclass
class UserPolicy:
    """
    User-defined policies for API request approval.
    
    Example (Medical Store Chatbot):
        policy = UserPolicy(
            user_id="medical_store_001",
            project_id="chatbot_24_7",
            allowed_providers=["openai", "google"],
            allowed_models={
                "openai": ["gpt-3.5-turbo", "gpt-4", "gpt-4-vision"],
                "google": ["gemini-pro"]
            },
            per_request_limit=1.00,
            daily_budget=50.00,
            rate_limit_per_minute=10
        )
    """
    
    # Identifiers
    user_id: str
    project_id: str
    policy_id: str = ""
    
    # Provider/Model whitelists (CRITICAL)
    allowed_providers: List[str] = field(default_factory=list)  # ["openai", "google", "anthropic"]
    allowed_models: Dict[str, List[str]] = field(default_factory=dict)  # {"openai": ["gpt-4", "gpt-3.5-turbo"]}
    forbidden_providers: List[str] = field(default_factory=list)  # Explicit blocks
    forbidden_operations: List[str] = field(default_factory=list)  # e.g., ["openai.gpt-4.batch-processing"]
    
    # Budget limits
    per_request_limit: float = 10.0  # Max USDC per single request
    daily_budget: float = 100.0  # Max USDC per day
    monthly_budget: float = 3000.0  # Max USDC per month
    
    # Rate limits
    rate_limit_per_minute: int = 10
    rate_limit_per_hour: int = 100
    rate_limit_per_day: int = 1000
    
    # Spending periods (when spending is allowed)
    allowed_hours: Optional[List[int]] = None  # [9, 10, 11, ..., 17] for 9am-5pm
    allowed_days: Optional[List[int]] = None  # [0, 1, 2, 3, 4] for Mon-Fri
    
    # Risk thresholds
    max_risk_score: float = 7.0  # Reject if risk > this
    auto_approve_risk_threshold: float = 3.0  # Auto-approve if risk < this
    
    # Recipient restrictions
    allowed_recipients: Optional[List[str]] = None  # Wallet addresses
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    is_active: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert policy to dictionary"""
        return {
            "user_id": self.user_id,
            "project_id": self.project_id,
            "policy_id": self.policy_id,
            "allowed_providers": self.allowed_providers,
            "allowed_models": self.allowed_models,
            "forbidden_providers": self.forbidden_providers,
            "forbidden_operations": self.forbidden_operations,
            "per_request_limit": self.per_request_limit,
            "daily_budget": self.daily_budget,
            "monthly_budget": self.monthly_budget,
            "rate_limit_per_minute": self.rate_limit_per_minute,
            "rate_limit_per_hour": self.rate_limit_per_hour,
            "rate_limit_per_day": self.rate_limit_per_day,
            "allowed_hours": self.allowed_hours,
            "allowed_days": self.allowed_days,
            "max_risk_score": self.max_risk_score,
            "auto_approve_risk_threshold": self.auto_approve_risk_threshold,
            "allowed_recipients": self.allowed_recipients,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "is_active": self.is_active,
        }
    
    @classmethod
    def fetch_from_backend(cls, user_id: str, project_id: str) -> 'UserPolicy':
        """
        Fetch user policy from backend API.
        
        Args:
            user_id: User identifier
            project_id: Project identifier
            
        Returns:
            UserPolicy object populated from backend
        """
        try:
            url = config.get_endpoint('policies', 'get_policy', user_id=user_id, project_id=project_id)
            response = requests.get(url, timeout=config.API_TIMEOUT)
            response.raise_for_status()
            data = response.json()
            
            return cls(
                user_id=data['user_id'],
                project_id=data['project_id'],
                policy_id=data.get('policy_id', ''),
                allowed_providers=data.get('allowed_providers', []),
                allowed_models=data.get('allowed_models', {}),
                forbidden_providers=data.get('forbidden_providers', []),
                forbidden_operations=data.get('forbidden_operations', []),
                per_request_limit=data.get('per_request_limit', config.DEFAULTS['per_request_limit']),
                daily_budget=data.get('daily_budget', config.DEFAULTS['daily_budget']),
                monthly_budget=data.get('monthly_budget', config.DEFAULTS['monthly_budget']),
                rate_limit_per_minute=data.get('rate_limit_per_minute', config.DEFAULTS['rate_limit_per_minute']),
                rate_limit_per_hour=data.get('rate_limit_per_hour', config.DEFAULTS['rate_limit_per_hour']),
                rate_limit_per_day=data.get('rate_limit_per_day', 1000),
                allowed_hours=data.get('allowed_hours'),
                allowed_days=data.get('allowed_days'),
                max_risk_score=data.get('max_risk_score', config.DEFAULTS['max_risk_score']),
                auto_approve_risk_threshold=data.get('auto_approve_risk_threshold', config.DEFAULTS['auto_approve_risk_threshold']),
                allowed_recipients=data.get('allowed_recipients'),
                is_active=data.get('is_active', True),
            )
        except Exception as e:
            logger.error(f"Failed to fetch user policy from backend: {e}")
            raise


@dataclass
class UserContext:
    """
    Complete context about a user/project for decision-making.
    
    Includes policy, spending history, and behavioral patterns.
    """
    
    # Identifiers
    user_id: str
    project_id: str
    
    # Policy
    policy: UserPolicy
    
            "created_at": self.created_at.isoformat(),
            "last_activity": self.last_activity.isoformat(),
        }
    
    @classmethod
    def fetch_from_backend(cls, user_id: str, project_id: str) -> 'UserContext':
        """
        Fetch complete user context from backend.
        
        Args:
            user_id: User identifier
            project_id: Project identifier
            
        Returns:
            UserContext object with all data from backend
        """
        try:
            url = config.get_endpoint('users', 'get_context', user_id=user_id)
            response = requests.get(url, params={'project_id': project_id}, timeout=config.API_TIMEOUT)
            response.raise_for_status()
            data = response.json()
            
            policy = UserPolicy.fetch_from_backend(user_id, project_id)
            
            return cls(
                user_id=data['user_id'],
                project_id=data['project_id'],
                policy=policy,
                agents=data.get('agents', []),
                total_spent_today=data.get('total_spent_today', 0.0),
                total_spent_this_month=data.get('total_spent_this_month', 0.0),
                total_requests_today=data.get('total_requests_today', 0),
                total_requests_this_month=data.get('total_requests_this_month', 0),
                recent_requests=data.get('recent_requests', []),
                recent_rejections=data.get('recent_rejections', 0),
                average_request_cost=data.get('average_request_cost', 0.0),
                average_requests_per_day=data.get('average_requests_per_day', 0.0),
                typical_providers=data.get('typical_providers', []),
                typical_request_times=data.get('typical_request_times', []),
                account_status=data.get('account_status', 'active'),
                is_verified=data.get('is_verified', True),
            )
        except Exception as e:
            logger.error(f"Failed to fetch user context from backend: {e}")
            raise
    # Spending history
    total_spent_today: float = 0.0
    total_spent_this_month: float = 0.0
    total_requests_today: int = 0
    total_requests_this_month: int = 0
    
    # Recent activity
    recent_requests: List[str] = field(default_factory=list)  # Recent request IDs
    recent_rejections: int = 0
    
    # Behavioral baseline (for anomaly detection)
    average_request_cost: float = 0.0
    average_requests_per_day: float = 0.0
    typical_providers: List[str] = field(default_factory=list)
    typical_request_times: List[int] = field(default_factory=list)  # Hours of day
    
    # Account status
    account_status: str = "active"  # "active", "suspended", "frozen"
    is_verified: bool = True
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_activity: datetime = field(default_factory=datetime.utcnow)
    
    def get_remaining_daily_budget(self) -> float:
        """Calculate remaining budget for today"""
        return max(0.0, self.policy.daily_budget - self.total_spent_today)
    
    def get_remaining_monthly_budget(self) -> float:
        """Calculate remaining budget for this month"""
        return max(0.0, self.policy.monthly_budget - self.total_spent_this_month)
    
    def is_within_budget(self, amount: float) -> bool:
        """Check if request amount is within available budget"""
        daily_ok = (self.total_spent_today + amount) <= self.policy.daily_budget
        monthly_ok = (self.total_spent_this_month + amount) <= self.policy.monthly_budget
        return daily_ok and monthly_ok
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert context to dictionary"""
        return {
            "user_id": self.user_id,
            "project_id": self.project_id,
            "policy": self.policy.to_dict(),
            "agents": self.agents,
            "total_spent_today": self.total_spent_today,
            "total_spent_this_month": self.total_spent_this_month,
            "total_requests_today": self.total_requests_today,
            "total_requests_this_month": self.total_requests_this_month,
            "recent_requests": self.recent_requests,
            "recent_rejections": self.recent_rejections,
            "average_request_cost": self.average_request_cost,
            "average_requests_per_day": self.average_requests_per_day,
            "typical_providers": self.typical_providers,
            "typical_request_times": self.typical_request_times,
            "account_status": self.account_status,
            "is_verified": self.is_verified,
            "created_at": self.created_at.isoformat(),
            "last_activity": self.last_activity.isoformat(),
        }
