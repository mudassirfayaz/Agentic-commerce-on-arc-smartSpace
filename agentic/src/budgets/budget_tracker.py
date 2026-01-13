"""
Budget tracking system for SmartSpace agentic decisions.

Tracks user/project USDC balances, manages budget reservations, monitors spending,
and provides spending analytics. This system is READ-ONLY from backend perspective -
it fetches data and makes decisions but doesn't persist changes.

Key responsibilities:
- Check available balance from backend
- Reserve budget for pending requests
- Validate spending against limits
- Track spending by period (hourly, daily, monthly)
- Detect budget anomalies
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional, Dict, List
from enum import Enum
import requests
import logging

from config import Config
from models.budget import BudgetCheck as BudgetCheckModel, BudgetPolicy

# Configure logging
logger = logging.getLogger(__name__)


class SpendingPeriod(str, Enum):
    """Time periods for spending analysis."""
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


@dataclass
class BudgetCheck:
    """Result of budget availability check."""
    sufficient: bool
    available_balance: float
    requested_amount: float
    currency: str = "USDC"
    checked_at: datetime = field(default_factory=datetime.utcnow)
    shortfall: Optional[float] = None
    message: str = ""
    
    def __post_init__(self):
        """Calculate shortfall and generate message."""
        if not self.sufficient:
            self.shortfall = self.requested_amount - self.available_balance
            self.message = f"Insufficient budget: need ${self.requested_amount:.4f}, have ${self.available_balance:.4f}"
        else:
            self.message = f"Budget check passed: ${self.available_balance:.4f} available"


@dataclass
class BudgetStatus:
    """Current budget status for user/project."""
    user_id: str
    project_id: str
    total_balance: float
    available_balance: float
    reserved_amount: float
    currency: str = "USDC"
    
    # Spending metrics
    spent_today: float = 0.0
    spent_this_month: float = 0.0
    spent_total: float = 0.0
    
    # Limits (from policy)
    daily_limit: Optional[float] = None
    monthly_limit: Optional[float] = None
    per_request_limit: Optional[float] = None
    
    # Status flags
    daily_limit_reached: bool = False
    monthly_limit_reached: bool = False
    low_balance_warning: bool = False
    
    checked_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        """Calculate status flags."""
        # Check limit thresholds
        if self.daily_limit:
            self.daily_limit_reached = self.spent_today >= self.daily_limit
        
        if self.monthly_limit:
            self.monthly_limit_reached = self.spent_this_month >= self.monthly_limit
        
        # Low balance warning at 20% remaining
        if self.total_balance > 0:
            usage_percent = (self.total_balance - self.available_balance) / self.total_balance
            self.low_balance_warning = usage_percent >= 0.8
    
    def get_remaining_today(self) -> Optional[float]:
        """Get remaining budget for today."""
        if self.daily_limit:
            return max(0, self.daily_limit - self.spent_today)
        return None
    
    def get_remaining_monthly(self) -> Optional[float]:
        """Get remaining budget for this month."""
        if self.monthly_limit:
            return max(0, self.monthly_limit - self.spent_this_month)
        return None


@dataclass
class BudgetReservation:
    """Budget reservation for pending request."""
    reservation_id: str
    user_id: str
    project_id: str
    request_id: str
    amount: float
    currency: str = "USDC"
    reserved_at: datetime = field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None
    status: str = "active"  # active, committed, released, expired
    
    def is_expired(self) -> bool:
        """Check if reservation has expired."""
        if self.expires_at:
            return datetime.utcnow() > self.expires_at
        return False


@dataclass
class SpendingAnalytics:
    """Spending analytics for a period."""
    user_id: str
    project_id: str
    period: SpendingPeriod
    start_date: datetime
    end_date: datetime
    
    total_spent: float = 0.0
    request_count: int = 0
    average_per_request: float = 0.0
    
    # Provider breakdown
    spending_by_provider: Dict[str, float] = field(default_factory=dict)
    requests_by_provider: Dict[str, int] = field(default_factory=dict)
    
    # Model breakdown
    spending_by_model: Dict[str, float] = field(default_factory=dict)
    requests_by_model: Dict[str, int] = field(default_factory=dict)
    
    # Trends
    spending_trend: str = "stable"  # increasing, decreasing, stable, volatile
    anomaly_detected: bool = False
    anomaly_details: Optional[str] = None


class BudgetTracker:
    """
    Budget tracking and spending management system.
    
    This system operates in READ-ONLY mode from backend:
    - Fetches balance and spending data from backend
    - Performs local calculations and validations
    - Returns decisions without persisting data
    - Backend handles actual balance updates and persistence
    """
    
    def __init__(self):
        """Initialize budget tracker."""
        self.config = Config()
        self.base_url = self.config.get_endpoint("budgets")
        self._cache: Dict[str, tuple[BudgetStatus, datetime]] = {}
        self._cache_ttl = 30  # Cache for 30 seconds
    
    async def get_available_balance(self, user_id: str, project_id: str) -> float:
        """
        Get available balance for user/project from backend.
        
        Args:
            user_id: User identifier
            project_id: Project identifier
            
        Returns:
            Available balance in USDC
        """
        try:
            url = f"{self.base_url}/user/{user_id}/project/{project_id}/balance"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            available = data.get("available_balance", 0.0)
            
            logger.info(f"Available balance for {user_id}/{project_id}: ${available:.4f}")
            return float(available)
            
        except requests.RequestException as e:
            logger.error(f"Failed to fetch balance: {e}")
            raise
    
    async def check_sufficient_budget(
        self, 
        user_id: str, 
        project_id: str,
        amount: float
    ) -> BudgetCheck:
        """
        Check if user has sufficient budget for requested amount.
        
        Args:
            user_id: User identifier
            project_id: Project identifier
            amount: Requested amount in USDC
            
        Returns:
            BudgetCheck with availability status
        """
        try:
            available = await self.get_available_balance(user_id, project_id)
            
            sufficient = available >= amount
            
            return BudgetCheck(
                sufficient=sufficient,
                available_balance=available,
                requested_amount=amount
            )
            
        except Exception as e:
            logger.error(f"Budget check failed: {e}")
            # Fail closed - reject if we can't verify budget
            return BudgetCheck(
                sufficient=False,
                available_balance=0.0,
                requested_amount=amount,
                message=f"Budget check error: {str(e)}"
            )
    
    async def get_budget_status(
        self, 
        user_id: str, 
        project_id: str,
        use_cache: bool = True
    ) -> BudgetStatus:
        """
        Get comprehensive budget status including spending metrics.
        
        Args:
            user_id: User identifier
            project_id: Project identifier
            use_cache: Whether to use cached data
            
        Returns:
            BudgetStatus with all metrics
        """
        # Check cache
        cache_key = f"{user_id}:{project_id}"
        if use_cache and cache_key in self._cache:
            cached_status, cached_at = self._cache[cache_key]
            if (datetime.utcnow() - cached_at).seconds < self._cache_ttl:
                logger.debug(f"Using cached budget status for {cache_key}")
                return cached_status
        
        try:
            url = f"{self.base_url}/user/{user_id}/project/{project_id}/status"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            
            status = BudgetStatus(
                user_id=user_id,
                project_id=project_id,
                total_balance=data.get("total_balance", 0.0),
                available_balance=data.get("available_balance", 0.0),
                reserved_amount=data.get("reserved_amount", 0.0),
                spent_today=data.get("spent_today", 0.0),
                spent_this_month=data.get("spent_this_month", 0.0),
                spent_total=data.get("spent_total", 0.0),
                daily_limit=data.get("daily_limit"),
                monthly_limit=data.get("monthly_limit"),
                per_request_limit=data.get("per_request_limit")
            )
            
            # Update cache
            self._cache[cache_key] = (status, datetime.utcnow())
            
            logger.info(f"Budget status for {user_id}/{project_id}: ${status.available_balance:.4f} available")
            return status
            
        except requests.RequestException as e:
            logger.error(f"Failed to fetch budget status: {e}")
            raise
    
    async def get_spending_by_period(
        self, 
        user_id: str, 
        project_id: str,
        period: SpendingPeriod
    ) -> float:
        """
        Get total spending for specified period.
        
        Args:
            user_id: User identifier
            project_id: Project identifier
            period: Time period to analyze
            
        Returns:
            Total spending in USDC for the period
        """
        try:
            url = f"{self.base_url}/user/{user_id}/project/{project_id}/spending/{period.value}"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            spending = data.get("total_spent", 0.0)
            
            logger.info(f"Spending for {user_id}/{project_id} ({period.value}): ${spending:.4f}")
            return float(spending)
            
        except requests.RequestException as e:
            logger.error(f"Failed to fetch spending: {e}")
            raise
    
    async def get_spending_analytics(
        self, 
        user_id: str, 
        project_id: str,
        period: SpendingPeriod,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> SpendingAnalytics:
        """
        Get detailed spending analytics with breakdowns.
        
        Args:
            user_id: User identifier
            project_id: Project identifier
            period: Time period to analyze
            start_date: Optional start date (defaults to period start)
            end_date: Optional end date (defaults to now)
            
        Returns:
            SpendingAnalytics with detailed breakdown
        """
        try:
            # Set default dates based on period
            if not end_date:
                end_date = datetime.utcnow()
            
            if not start_date:
                if period == SpendingPeriod.HOURLY:
                    start_date = end_date - timedelta(hours=1)
                elif period == SpendingPeriod.DAILY:
                    start_date = end_date - timedelta(days=1)
                elif period == SpendingPeriod.WEEKLY:
                    start_date = end_date - timedelta(weeks=1)
                elif period == SpendingPeriod.MONTHLY:
                    start_date = end_date - timedelta(days=30)
                else:  # YEARLY
                    start_date = end_date - timedelta(days=365)
            
            url = f"{self.base_url}/user/{user_id}/project/{project_id}/analytics"
            params = {
                "period": period.value,
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat()
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            analytics = SpendingAnalytics(
                user_id=user_id,
                project_id=project_id,
                period=period,
                start_date=start_date,
                end_date=end_date,
                total_spent=data.get("total_spent", 0.0),
                request_count=data.get("request_count", 0),
                average_per_request=data.get("average_per_request", 0.0),
                spending_by_provider=data.get("spending_by_provider", {}),
                requests_by_provider=data.get("requests_by_provider", {}),
                spending_by_model=data.get("spending_by_model", {}),
                requests_by_model=data.get("requests_by_model", {}),
                spending_trend=data.get("spending_trend", "stable"),
                anomaly_detected=data.get("anomaly_detected", False),
                anomaly_details=data.get("anomaly_details")
            )
            
            logger.info(f"Analytics for {user_id}/{project_id}: {analytics.request_count} requests, ${analytics.total_spent:.4f} spent")
            return analytics
            
        except requests.RequestException as e:
            logger.error(f"Failed to fetch analytics: {e}")
            raise
    
    async def check_against_policy(
        self, 
        user_id: str, 
        project_id: str,
        requested_amount: float,
        policy: BudgetPolicy
    ) -> BudgetCheckModel:
        """
        Check request against budget policy limits.
        
        Args:
            user_id: User identifier
            project_id: Project identifier
            requested_amount: Requested spending amount
            policy: Budget policy to check against
            
        Returns:
            BudgetCheckModel with validation results
        """
        try:
            # Get current status
            status = await self.get_budget_status(user_id, project_id)
            
            violations = []
            
            # Check available balance
            if requested_amount > status.available_balance:
                violations.append(
                    f"Insufficient balance: need ${requested_amount:.4f}, have ${status.available_balance:.4f}"
                )
            
            # Check per-request limit
            if policy.per_request_limit and requested_amount > policy.per_request_limit:
                violations.append(
                    f"Exceeds per-request limit: ${requested_amount:.4f} > ${policy.per_request_limit:.4f}"
                )
            
            # Check daily limit
            if policy.daily_limit:
                projected_daily = status.spent_today + requested_amount
                if projected_daily > policy.daily_limit:
                    violations.append(
                        f"Would exceed daily limit: ${projected_daily:.4f} > ${policy.daily_limit:.4f}"
                    )
            
            # Check monthly limit
            if policy.monthly_limit:
                projected_monthly = status.spent_this_month + requested_amount
                if projected_monthly > policy.monthly_limit:
                    violations.append(
                        f"Would exceed monthly limit: ${projected_monthly:.4f} > ${policy.monthly_limit:.4f}"
                    )
            
            return BudgetCheckModel(
                available=len(violations) == 0,
                current_balance=status.available_balance,
                estimated_cost=requested_amount,
                remaining_budget=status.available_balance - requested_amount if len(violations) == 0 else 0.0,
                violations=violations,
                checked_at=datetime.utcnow()
            )
            
        except Exception as e:
            logger.error(f"Policy check failed: {e}")
            return BudgetCheckModel(
                available=False,
                current_balance=0.0,
                estimated_cost=requested_amount,
                remaining_budget=0.0,
                violations=[f"Budget policy check error: {str(e)}"],
                checked_at=datetime.utcnow()
            )
    
    def clear_cache(self, user_id: Optional[str] = None, project_id: Optional[str] = None):
        """
        Clear budget status cache.
        
        Args:
            user_id: Optional user to clear (clears all if None)
            project_id: Optional project to clear (clears user if None)
        """
        if user_id and project_id:
            cache_key = f"{user_id}:{project_id}"
            self._cache.pop(cache_key, None)
            logger.debug(f"Cleared cache for {cache_key}")
        elif user_id:
            # Clear all entries for this user
            keys_to_remove = [k for k in self._cache.keys() if k.startswith(f"{user_id}:")]
            for key in keys_to_remove:
                self._cache.pop(key)
            logger.debug(f"Cleared cache for user {user_id}")
        else:
            # Clear entire cache
            self._cache.clear()
            logger.debug("Cleared entire budget cache")
