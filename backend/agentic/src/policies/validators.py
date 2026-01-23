"""
Policy Validators

Specialized validators for different policy types.
"""

from typing import Optional, List
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging

from models.user import UserPolicy
from models.request import APIRequest

logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Result of a validation check"""
    valid: bool
    reason: Optional[str] = None
    details: Optional[dict] = None


class ProviderValidator:
    """Validates API provider access"""
    
    @staticmethod
    def validate(provider: str, policy: UserPolicy) -> ValidationResult:
        """
        Check if provider is allowed.
        
        Args:
            provider: Provider name (e.g., "openai")
            policy: User policy
            
        Returns:
            ValidationResult
        """
        # Check forbidden list first
        if provider in policy.forbidden_providers:
            return ValidationResult(
                valid=False,
                reason=f"Provider '{provider}' is explicitly forbidden",
                details={"provider": provider, "forbidden_providers": policy.forbidden_providers}
            )
        
        # Check allowed list
        if not policy.allowed_providers:
            # No restrictions - allow all
            return ValidationResult(valid=True)
        
        if provider not in policy.allowed_providers:
            return ValidationResult(
                valid=False,
                reason=f"Provider '{provider}' not in allowed list",
                details={
                    "provider": provider,
                    "allowed_providers": policy.allowed_providers
                }
            )
        
        return ValidationResult(valid=True, details={"provider": provider})


class ModelValidator:
    """Validates model access for specific providers"""
    
    @staticmethod
    def validate(model: str, provider: str, policy: UserPolicy) -> ValidationResult:
        """
        Check if model is allowed for this provider.
        
        Args:
            model: Model name (e.g., "gpt-4")
            provider: Provider name (e.g., "openai")
            policy: User policy
            
        Returns:
            ValidationResult
        """
        # Check if any models configured for this provider
        if not policy.allowed_models or provider not in policy.allowed_models:
            # No restrictions for this provider
            return ValidationResult(valid=True)
        
        allowed_models = policy.allowed_models[provider]
        
        if model not in allowed_models:
            return ValidationResult(
                valid=False,
                reason=f"Model '{model}' not allowed for provider '{provider}'",
                details={
                    "model": model,
                    "provider": provider,
                    "allowed_models": allowed_models
                }
            )
        
        return ValidationResult(
            valid=True,
            details={"model": model, "provider": provider}
        )


class BudgetValidator:
    """Validates budget-related constraints"""
    
    @staticmethod
    def validate_per_request_limit(cost: float, policy: UserPolicy) -> ValidationResult:
        """Check if cost is within per-request limit"""
        if cost > policy.per_request_limit:
            return ValidationResult(
                valid=False,
                reason=f"Cost ${cost:.4f} exceeds per-request limit ${policy.per_request_limit}",
                details={
                    "cost": cost,
                    "limit": policy.per_request_limit,
                    "excess": cost - policy.per_request_limit
                }
            )
        
        return ValidationResult(
            valid=True,
            details={"cost": cost, "limit": policy.per_request_limit}
        )
    
    @staticmethod
    def validate_daily_budget(
        current_spent: float,
        request_cost: float,
        policy: UserPolicy
    ) -> ValidationResult:
        """Check if request would exceed daily budget"""
        total_if_approved = current_spent + request_cost
        
        if total_if_approved > policy.daily_budget:
            return ValidationResult(
                valid=False,
                reason=f"Would exceed daily budget: ${total_if_approved:.2f} > ${policy.daily_budget}",
                details={
                    "current_spent": current_spent,
                    "request_cost": request_cost,
                    "daily_limit": policy.daily_budget,
                    "excess": total_if_approved - policy.daily_budget
                }
            )
        
        return ValidationResult(
            valid=True,
            details={
                "current_spent": current_spent,
                "request_cost": request_cost,
                "daily_limit": policy.daily_budget,
                "remaining": policy.daily_budget - total_if_approved
            }
        )
    
    @staticmethod
    def validate_monthly_budget(
        current_spent: float,
        request_cost: float,
        policy: UserPolicy
    ) -> ValidationResult:
        """Check if request would exceed monthly budget"""
        total_if_approved = current_spent + request_cost
        
        if total_if_approved > policy.monthly_budget:
            return ValidationResult(
                valid=False,
                reason=f"Would exceed monthly budget: ${total_if_approved:.2f} > ${policy.monthly_budget}",
                details={
                    "current_spent": current_spent,
                    "request_cost": request_cost,
                    "monthly_limit": policy.monthly_budget,
                    "excess": total_if_approved - policy.monthly_budget
                }
            )
        
        return ValidationResult(
            valid=True,
            details={
                "current_spent": current_spent,
                "request_cost": request_cost,
                "monthly_limit": policy.monthly_budget,
                "remaining": policy.monthly_budget - total_if_approved
            }
        )


class RateLimitValidator:
    """Validates rate limiting constraints"""
    
    @staticmethod
    def validate_per_minute(
        recent_requests: List[datetime],
        policy: UserPolicy
    ) -> ValidationResult:
        """Check if rate limit per minute would be exceeded"""
        one_minute_ago = datetime.utcnow() - timedelta(minutes=1)
        requests_in_last_minute = sum(1 for req_time in recent_requests if req_time > one_minute_ago)
        
        if requests_in_last_minute >= policy.rate_limit_per_minute:
            return ValidationResult(
                valid=False,
                reason=f"Rate limit exceeded: {requests_in_last_minute} requests in last minute (limit: {policy.rate_limit_per_minute})",
                details={
                    "requests_in_window": requests_in_last_minute,
                    "limit": policy.rate_limit_per_minute,
                    "window": "1 minute"
                }
            )
        
        return ValidationResult(
            valid=True,
            details={
                "requests_in_window": requests_in_last_minute,
                "limit": policy.rate_limit_per_minute,
                "remaining": policy.rate_limit_per_minute - requests_in_last_minute
            }
        )
    
    @staticmethod
    def validate_per_hour(
        recent_requests: List[datetime],
        policy: UserPolicy
    ) -> ValidationResult:
        """Check if rate limit per hour would be exceeded"""
        one_hour_ago = datetime.utcnow() - timedelta(hours=1)
        requests_in_last_hour = sum(1 for req_time in recent_requests if req_time > one_hour_ago)
        
        if requests_in_last_hour >= policy.rate_limit_per_hour:
            return ValidationResult(
                valid=False,
                reason=f"Rate limit exceeded: {requests_in_last_hour} requests in last hour (limit: {policy.rate_limit_per_hour})",
                details={
                    "requests_in_window": requests_in_last_hour,
                    "limit": policy.rate_limit_per_hour,
                    "window": "1 hour"
                }
            )
        
        return ValidationResult(
            valid=True,
            details={
                "requests_in_window": requests_in_last_hour,
                "limit": policy.rate_limit_per_hour,
                "remaining": policy.rate_limit_per_hour - requests_in_last_hour
            }
        )
    
    @staticmethod
    def validate_per_day(
        requests_today: int,
        policy: UserPolicy
    ) -> ValidationResult:
        """Check if rate limit per day would be exceeded"""
        if requests_today >= policy.rate_limit_per_day:
            return ValidationResult(
                valid=False,
                reason=f"Daily request limit exceeded: {requests_today}/{policy.rate_limit_per_day}",
                details={
                    "requests_today": requests_today,
                    "limit": policy.rate_limit_per_day
                }
            )
        
        return ValidationResult(
            valid=True,
            details={
                "requests_today": requests_today,
                "limit": policy.rate_limit_per_day,
                "remaining": policy.rate_limit_per_day - requests_today
            }
        )


class TimeRestrictionValidator:
    """Validates time-based spending restrictions"""
    
    @staticmethod
    def validate_allowed_hours(policy: UserPolicy) -> ValidationResult:
        """Check if current time is within allowed hours"""
        if not policy.allowed_hours:
            return ValidationResult(valid=True)
        
        current_hour = datetime.utcnow().hour
        
        if current_hour not in policy.allowed_hours:
            return ValidationResult(
                valid=False,
                reason=f"Requests only allowed during hours: {policy.allowed_hours}. Current: {current_hour}",
                details={
                    "current_hour": current_hour,
                    "allowed_hours": policy.allowed_hours
                }
            )
        
        return ValidationResult(
            valid=True,
            details={"current_hour": current_hour, "allowed_hours": policy.allowed_hours}
        )
    
    @staticmethod
    def validate_allowed_days(policy: UserPolicy) -> ValidationResult:
        """Check if current day is within allowed days"""
        if not policy.allowed_days:
            return ValidationResult(valid=True)
        
        current_day = datetime.utcnow().weekday()  # 0=Monday, 6=Sunday
        
        if current_day not in policy.allowed_days:
            days_map = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            return ValidationResult(
                valid=False,
                reason=f"Requests only allowed on: {[days_map[d] for d in policy.allowed_days]}. Today: {days_map[current_day]}",
                details={
                    "current_day": current_day,
                    "allowed_days": policy.allowed_days
                }
            )
        
        return ValidationResult(
            valid=True,
            details={"current_day": current_day, "allowed_days": policy.allowed_days}
        )
