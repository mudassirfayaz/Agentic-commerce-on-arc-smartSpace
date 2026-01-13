"""
Policy Manager

Central system for loading and enforcing user-defined policies.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import logging

from ..models.user import UserPolicy, UserContext
from ..models.request import APIRequest
from ..config import config

logger = logging.getLogger(__name__)


@dataclass
class PolicyViolation:
    """Represents a policy violation"""
    policy_name: str
    violation_type: str
    details: str
    severity: str  # "low", "medium", "high", "critical"


@dataclass
class ComplianceResult:
    """Result of policy compliance check"""
    compliant: bool
    violations: List[PolicyViolation] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    policies_checked: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    def add_violation(self, policy_name: str, violation_type: str, details: str, severity: str = "high"):
        """Add a policy violation"""
        violation = PolicyViolation(
            policy_name=policy_name,
            violation_type=violation_type,
            details=details,
            severity=severity
        )
        self.violations.append(violation)
        self.compliant = False
    
    def add_warning(self, message: str):
        """Add a warning (non-blocking)"""
        self.warnings.append(message)
    
    def get_rejection_reason(self) -> str:
        """Get human-readable rejection reason"""
        if not self.violations:
            return ""
        
        critical_violations = [v for v in self.violations if v.severity == "critical"]
        if critical_violations:
            return f"Critical violation: {critical_violations[0].details}"
        
        high_violations = [v for v in self.violations if v.severity == "high"]
        if high_violations:
            return f"Policy violation: {high_violations[0].details}"
        
        return f"Policy violation: {self.violations[0].details}"


class PolicyManager:
    """
    Manages policy loading, validation, and enforcement.
    
    This is the gatekeeper - ensures all requests comply with user policies.
    """
    
    def __init__(self):
        self.cache: Dict[str, UserPolicy] = {}
    
    async def load_policy(self, user_id: str, project_id: str) -> UserPolicy:
        """
        Load policy from backend for user/project.
        
        Args:
            user_id: User identifier
            project_id: Project identifier
            
        Returns:
            UserPolicy object
        """
        cache_key = f"{user_id}:{project_id}"
        
        # Check cache first
        if cache_key in self.cache:
            logger.debug(f"Policy cache hit for {cache_key}")
            return self.cache[cache_key]
        
        # Fetch from backend
        try:
            policy = UserPolicy.fetch_from_backend(user_id, project_id)
            self.cache[cache_key] = policy
            logger.info(f"Loaded policy for {user_id}/{project_id}")
            return policy
        except Exception as e:
            logger.error(f"Failed to load policy: {e}")
            raise
    
    async def check_compliance(
        self,
        request: APIRequest,
        policy: UserPolicy
    ) -> ComplianceResult:
        """
        Check if request complies with ALL policies.
        
        This is the main enforcement point - validates everything.
        
        Args:
            request: The API request to validate
            policy: User's policy configuration
            
        Returns:
            ComplianceResult with violations if any
        """
        result = ComplianceResult()
        
        # 1. CRITICAL: Validate provider whitelist
        if not self._validate_provider(request.api_provider, policy, result):
            return result  # Early exit on provider violation
        
        # 2. CRITICAL: Validate model whitelist
        if not self._validate_model(request.model_name, request.api_provider, policy, result):
            return result  # Early exit on model violation
        
        # 3. Check per-request cost limit
        if not self._validate_per_request_limit(request.estimated_cost, policy, result):
            pass  # Continue checking other policies
        
        # 4. Check if policy is active
        if not policy.is_active:
            result.add_violation(
                "policy_status",
                "inactive_policy",
                f"Policy for user {request.user_id} is inactive",
                "critical"
            )
            return result
        
        # 5. Check forbidden operations
        operation_key = f"{request.api_provider}.{request.model_name}.{request.operation_type}"
        if operation_key in policy.forbidden_operations:
            result.add_violation(
                "forbidden_operations",
                "operation_blocked",
                f"Operation {operation_key} is explicitly forbidden",
                "high"
            )
        
        # 6. Check time-based restrictions
        if not self._validate_time_restrictions(policy, result):
            pass
        
        # Mark request as policy-validated
        if result.compliant:
            logger.info(f"Request {request.request_id} passed all policy checks")
        else:
            logger.warning(f"Request {request.request_id} failed policy checks: {result.violations}")
        
        return result
    
    def _validate_provider(
        self,
        provider: str,
        policy: UserPolicy,
        result: ComplianceResult
    ) -> bool:
        """
        Validate provider against whitelist.
        
        THE GOLDEN RULE: Only whitelisted providers allowed.
        """
        result.policies_checked.append("provider_whitelist")
        
        # Check if provider is explicitly forbidden
        if provider in policy.forbidden_providers:
            result.add_violation(
                "provider_whitelist",
                "forbidden_provider",
                f"Provider '{provider}' is explicitly forbidden",
                "critical"
            )
            return False
        
        # Check if provider is in allowed list
        if not policy.allowed_providers:
            result.add_warning("No providers configured in policy")
            return True  # Allow if no restrictions set
        
        if provider not in policy.allowed_providers:
            result.add_violation(
                "provider_whitelist",
                "unauthorized_provider",
                f"Provider '{provider}' not in allowed list. Allowed: {policy.allowed_providers}",
                "critical"
            )
            return False
        
        logger.debug(f"Provider '{provider}' validated against whitelist")
        return True
    
    def _validate_model(
        self,
        model: str,
        provider: str,
        policy: UserPolicy,
        result: ComplianceResult
    ) -> bool:
        """
        Validate model against provider's whitelist.
        
        THE GOLDEN RULE: Only whitelisted models for each provider allowed.
        """
        result.policies_checked.append("model_whitelist")
        
        # Check if models are configured for this provider
        if not policy.allowed_models or provider not in policy.allowed_models:
            result.add_warning(f"No model restrictions for provider '{provider}'")
            return True  # Allow if no restrictions set
        
        allowed_models_for_provider = policy.allowed_models[provider]
        
        if model not in allowed_models_for_provider:
            result.add_violation(
                "model_whitelist",
                "unauthorized_model",
                f"Model '{model}' not allowed for provider '{provider}'. Allowed: {allowed_models_for_provider}",
                "critical"
            )
            return False
        
        logger.debug(f"Model '{model}' validated for provider '{provider}'")
        return True
    
    def _validate_per_request_limit(
        self,
        cost: float,
        policy: UserPolicy,
        result: ComplianceResult
    ) -> bool:
        """Validate cost against per-request limit"""
        result.policies_checked.append("per_request_limit")
        
        if cost > policy.per_request_limit:
            result.add_violation(
                "per_request_limit",
                "cost_exceeded",
                f"Request cost ${cost:.4f} exceeds limit ${policy.per_request_limit}",
                "high"
            )
            return False
        
        return True
    
    def _validate_time_restrictions(
        self,
        policy: UserPolicy,
        result: ComplianceResult
    ) -> bool:
        """Validate time-based spending restrictions"""
        result.policies_checked.append("time_restrictions")
        
        now = datetime.utcnow()
        current_hour = now.hour
        current_day = now.weekday()  # 0=Monday, 6=Sunday
        
        # Check allowed hours
        if policy.allowed_hours and current_hour not in policy.allowed_hours:
            result.add_violation(
                "time_restrictions",
                "outside_allowed_hours",
                f"Requests only allowed during hours: {policy.allowed_hours}. Current hour: {current_hour}",
                "medium"
            )
            return False
        
        # Check allowed days
        if policy.allowed_days and current_day not in policy.allowed_days:
            days_map = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            result.add_violation(
                "time_restrictions",
                "outside_allowed_days",
                f"Requests only allowed on specified days. Current: {days_map[current_day]}",
                "medium"
            )
            return False
        
        return True
    
    async def get_allowed_providers(self, user_id: str, project_id: str) -> List[str]:
        """
        Get list of approved providers for user.
        
        Args:
            user_id: User identifier
            project_id: Project identifier
            
        Returns:
            List of allowed provider names
        """
        policy = await self.load_policy(user_id, project_id)
        return policy.allowed_providers
    
    async def get_allowed_models(
        self,
        user_id: str,
        project_id: str,
        provider: str
    ) -> List[str]:
        """
        Get list of approved models for specific provider.
        
        Args:
            user_id: User identifier
            project_id: Project identifier
            provider: Provider name
            
        Returns:
            List of allowed model names for that provider
        """
        policy = await self.load_policy(user_id, project_id)
        return policy.allowed_models.get(provider, [])
    
    def clear_cache(self, user_id: Optional[str] = None, project_id: Optional[str] = None):
        """
        Clear policy cache.
        
        Args:
            user_id: If provided, clear only this user's cache
            project_id: If provided, clear only this project's cache
        """
        if user_id and project_id:
            cache_key = f"{user_id}:{project_id}"
            if cache_key in self.cache:
                del self.cache[cache_key]
                logger.info(f"Cleared cache for {cache_key}")
        else:
            self.cache.clear()
            logger.info("Cleared entire policy cache")
