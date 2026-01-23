"""
Budget and Cost Tracking Models

Defines budget policies and spending tracking.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, Optional, Any
import requests
import logging

from config import config

logger = logging.getLogger(__name__)


class BudgetStatus(Enum):
    """Status of budget availability"""
    AVAILABLE = "available"
    LOW = "low"  # < 20% remaining
    CRITICAL = "critical"  # < 5% remaining
    EXHAUSTED = "exhausted"
    EXCEEDED = "exceeded"


@dataclass
class BudgetCheck:
    """
    Result of a budget availability check.
    
    Example:
        check = BudgetCheck(
            sufficient=True,
            available=48.76,
            required=0.002,
            daily_limit=50.00,
            daily_spent=1.24,
            status=BudgetStatus.AVAILABLE
        )
    """
    
    # Check result
    sufficient: bool
    
    # Budget details
    available: float  # Available budget in USDC
    required: float  # Required amount for this request
    
    # Daily budget
    daily_limit: float
    daily_spent: float
    daily_remaining: float = 0.0
    
    # Monthly budget
    monthly_limit: float = 0.0
    monthly_spent: float = 0.0
    monthly_remaining: float = 0.0
    
    # Status
    status: BudgetStatus = BudgetStatus.AVAILABLE
    
    # Warning flags
    is_low_balance: bool = False  # < 20% remaining
    is_critical_balance: bool = False  # < 5% remaining
    
    # Timestamp
    checked_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        """Calculate derived fields"""
        self.daily_remaining = max(0.0, self.daily_limit - self.daily_spent)
        self.monthly_remaining = max(0.0, self.monthly_limit - self.monthly_spent)
        
        # Calculate percentage remaining
        daily_pct = (self.daily_remaining / self.daily_limit * 100) if self.daily_limit > 0 else 0
        monthly_pct = (self.monthly_remaining / self.monthly_limit * 100) if self.monthly_limit > 0 else 0
        
        min_pct = min(daily_pct, monthly_pct)
        
        # Set warning flags
        if min_pct < 5:
            self.is_critical_balance = True
            self.status = BudgetStatus.CRITICAL
        elif min_pct < 20:
            self.is_low_balance = True
            self.status = BudgetStatus.LOW
        
        if self.daily_spent >= self.daily_limit or self.monthly_spent >= self.monthly_limit:
            self.status = BudgetStatus.EXHAUSTED
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "sufficient": self.sufficient,
            "available": self.available,
            "required": self.required,
            "daily_limit": self.daily_limit,
            "daily_spent": self.daily_spent,
            "daily_remaining": self.daily_remaining,
            "monthly_limit": self.monthly_limit,
            "monthly_spent": self.monthly_spent,
            "monthly_remaining": self.monthly_remaining,
            "status": self.status.value,
            "is_low_balance": self.is_low_balance,
            "is_critical_balance": self.is_critical_balance,
            "checked_at": self.checked_at.isoformat(),
        }
    
    @classmethod
    def check_from_backend(cls, user_id: str, project_id: str, required_amount: float) -> 'BudgetCheck':
        """
        Check budget availability via backend API.
        
        Args:
            user_id: User identifier
            project_id: Project identifier
            required_amount: Amount needed in USDC
            
        Returns:
            BudgetCheck object with availability details
        """
        try:
            url = config.get_endpoint('budgets', 'check_budget', user_id=user_id, project_id=project_id)
            response = requests.post(url, json={'amount': required_amount}, timeout=config.API_TIMEOUT)
            response.raise_for_status()
            data = response.json()
            
            status_value = data.get('status', 'available')
            try:
                status = BudgetStatus(status_value)
            except ValueError:
                status = BudgetStatus.AVAILABLE
            
            return cls(
                sufficient=data.get('sufficient', False),
                available=data.get('available', 0.0),
                required=required_amount,
                daily_limit=data.get('daily_limit', 0.0),
                daily_spent=data.get('daily_spent', 0.0),
                daily_remaining=data.get('daily_remaining', 0.0),
                monthly_limit=data.get('monthly_limit', 0.0),
                monthly_spent=data.get('monthly_spent', 0.0),
                monthly_remaining=data.get('monthly_remaining', 0.0),
                status=status,
                is_low_balance=data.get('is_low_balance', False),
                is_critical_balance=data.get('is_critical_balance', False),
            )
        except Exception as e:
            logger.error(f"Failed to check budget from backend: {e}")
            raise


@dataclass
class BudgetPolicy:
    """
    Budget policy configuration for a user/project.
    
    Defines spending limits and thresholds.
    """
    
    # Identifiers
    user_id: str
    project_id: str
    
    # Limits (in USDC)
    per_request_max: float = 10.0
    daily_limit: float = 100.0
    monthly_limit: float = 3000.0
    
    # Alert thresholds (percentage)
    alert_threshold_low: float = 20.0  # Alert at 20% remaining
    alert_threshold_critical: float = 5.0  # Alert at 5% remaining
    
    # Auto-reload configuration (future feature)
    auto_reload_enabled: bool = False
    auto_reload_threshold: float = 10.0  # Reload when balance < $10
    auto_reload_amount: float = 100.0
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def is_within_limits(self, amount: float, daily_spent: float, monthly_spent: float) -> bool:
        """Check if amount is within all budget limits"""
        per_request_ok = amount <= self.per_request_max
        daily_ok = (daily_spent + amount) <= self.daily_limit
        monthly_ok = (monthly_spent + amount) <= self.monthly_limit
        
        return per_request_ok and daily_ok and monthly_ok
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "user_id": self.user_id,
            "project_id": self.project_id,
            "per_request_max": self.per_request_max,
            "daily_limit": self.daily_limit,
            "monthly_limit": self.monthly_limit,
            "alert_threshold_low": self.alert_threshold_low,
            "alert_threshold_critical": self.alert_threshold_critical,
            "auto_reload_enabled": self.auto_reload_enabled,
            "auto_reload_threshold": self.auto_reload_threshold,
            "auto_reload_amount": self.auto_reload_amount,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
    
    @classmethod
    def fetch_from_backend(cls, user_id: str, project_id: str) -> 'BudgetPolicy':
        """
        Fetch budget policy from backend API.
        
        Args:
            user_id: User identifier
            project_id: Project identifier
            
        Returns:
            BudgetPolicy object
        """
        try:
            url = config.get_endpoint('budgets', 'get_budget', user_id=user_id, project_id=project_id)
            response = requests.get(url, timeout=config.API_TIMEOUT)
            response.raise_for_status()
            data = response.json()
            
            return cls(
                user_id=data['user_id'],
                project_id=data['project_id'],
                per_request_max=data.get('per_request_max', 10.0),
                daily_limit=data.get('daily_limit', 100.0),
                monthly_limit=data.get('monthly_limit', 3000.0),
                alert_threshold_low=data.get('alert_threshold_low', 20.0),
                alert_threshold_critical=data.get('alert_threshold_critical', 5.0),
                auto_reload_enabled=data.get('auto_reload_enabled', False),
                auto_reload_threshold=data.get('auto_reload_threshold', 10.0),
                auto_reload_amount=data.get('auto_reload_amount', 100.0),
            )
        except Exception as e:
            logger.error(f"Failed to fetch budget policy from backend: {e}")
            raise

