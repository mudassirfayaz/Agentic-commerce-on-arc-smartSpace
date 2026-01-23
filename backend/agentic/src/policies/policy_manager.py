"""
Policy Manager

Central system for loading and enforcing both user-defined and system-defined policies.
Fetches policies from backend and validates requests against them.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import logging
import requests

# Assuming these models exist in your project structure
from models.user import UserPolicy
from models.request import APIRequest
from config import Config

logger = logging.getLogger(__name__)


@dataclass
class SystemPolicy:
    """
    System-wide policies defined by the platform.
    These are enforced on all requests regardless of user settings.
    """
    policy_id: str
    name: str
    description: str
    
    # System-level restrictions
    blocked_providers: List[str] = field(default_factory=list)  # Platform blocks
    blocked_models: List[str] = field(default_factory=list)
    blocked_operations: List[str] = field(default_factory=list)
    
    # System limits (cannot be exceeded by users)
    max_per_request_limit: float = 100.0  # Max USDC per request (hard limit)
    max_daily_limit: float = 10000.0
    max_rate_per_minute: int = 100
    
    # Security policies
    require_verification: bool = True
    require_2fa_above: float = 10.0  # Require 2FA for requests > $10
    
    # Compliance requirements
    audit_all_requests: bool = True
    retention_days: int = 365
    
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


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
    compliant: bool = True  # Default to True so empty initialization works
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
    
    Loads and enforces BOTH:
    1. System policies - Platform-wide rules (from backend)
    2. User policies - User-specific configurations (from backend)
    
    System policies are enforced first and cannot be overridden.
    """
    
    def __init__(self):
        self.config = Config()
        self.user_policy_cache: Dict[str, UserPolicy] = {}
        self.system_policy_cache: Optional[SystemPolicy] = None
        self.system_policy_loaded_at: Optional[datetime] = None
        self.system_policy_ttl = 300  # Cache system policy for 5 minutes
    
    async def load_system_policy(self) -> SystemPolicy:
        """
        Load system-wide policy from backend.
        These are platform rules that apply to all users.
        
        Returns:
            SystemPolicy object
        """
        # Check cache
        if self.system_policy_cache and self.system_policy_loaded_at:
            age = (datetime.utcnow() - self.system_policy_loaded_at).seconds
            if age < self.system_policy_ttl:
                logger.debug("System policy cache hit")
                return self.system_policy_cache
        
        # Fetch from backend
        try:
            url = f"{self.config.BACKEND_API_URL}/policies/system"
            response = requests.get(url, timeout=self.config.API_TIMEOUT)
            response.raise_for_status()
            data = response.json()
            
            system_policy = SystemPolicy(
                policy_id=data.get('policy_id', 'sys_default'),
                name=data.get('name', 'System Policy'),
                description=data.get('description', 'Platform-wide policies'),
                blocked_providers=data.get('blocked_providers', []),
                blocked_models=data.get('blocked_models', []),
                blocked_operations=data.get('blocked_operations', []),
                max_per_request_limit=data.get('max_per_request_limit', 100.0),
                max_daily_limit=data.get('max_daily_limit', 10000.0),
                max_rate_per_minute=data.get('max_rate_per_minute', 100),
                require_verification=data.get('require_verification', True),
                require_2fa_above=data.get('require_2fa_above', 10.0),
                audit_all_requests=data.get('audit_all_requests', True),
                retention_days=data.get('retention_days', 365),
                is_active=data.get('is_active', True)
            )
            
            # Update cache
            self.system_policy_cache = system_policy
            self.system_policy_loaded_at = datetime.utcnow()
            
            logger.info("Loaded system policy from backend")
            return system_policy
            
        except Exception as e:
            logger.warning(f"Failed to load system policy, using defaults: {e}")
            # Return default system policy
            return SystemPolicy(
                policy_id="sys_default",
                name="Default System Policy",
                description="Default platform policies"
            )
    
    async def load_user_policy(self, user_id: str, project_id: str) -> UserPolicy:
        """
        Load user-specific policy from backend.
        
        Args:
            user_id: User identifier
            project_id: Project identifier
            
        Returns:
            UserPolicy object
        """
        cache_key = f"{user_id}:{project_id}"
        
        # Check cache first
        if cache_key in self.user_policy_cache:
            logger.debug(f"User policy cache hit for {cache_key}")
            return self.user_policy_cache[cache_key]
        
        # Fetch from backend
        try:
            policy = UserPolicy.fetch_from_backend(user_id, project_id)
            self.user_policy_cache[cache_key] = policy
            logger.info(f"Loaded user policy for {user_id}/{project_id}")
            return policy
        except Exception as e:
            logger.error(f"Failed to load user policy: {e}")
            raise
    
    async def check_compliance(
        self,
        request: APIRequest,
        user_policy: UserPolicy,
        system_policy: Optional[SystemPolicy] = None
    ) -> ComplianceResult:
        """
        Check if request complies with ALL policies.
        
        Enforces BOTH system and user policies:
        1. System policies (platform-wide) - checked first, cannot be overridden
        2. User policies (user-specific) - checked second
        
        Args:
            request: The API request to validate
            user_policy: User's policy configuration
            system_policy: System policy (loaded automatically if not provided)
            
        Returns:
            ComplianceResult with violations if any
        """
        result = ComplianceResult()
        
        # Load system policy if not provided
        if system_policy is None:
            system_policy = await self.load_system_policy()
        
        # STEP 1: Check SYSTEM policies first (cannot be overridden)
        result.policies_checked.append("system_policy")
        
        # 1a. Check system blocked providers
        if request.api_provider in system_policy.blocked_providers:
            result.add_violation(
                "system_policy",
                "blocked_provider",
                f"Provider '{request.api_provider}' is blocked by platform policy",
                "critical"
            )
            return result  # Early exit
        
        # 1b. Check system blocked models
        model_key = f"{request.api_provider}/{request.model_name}"
        if model_key in system_policy.blocked_models:
            result.add_violation(
                "system_policy",
                "blocked_model",
                f"Model '{model_key}' is blocked by platform policy",
                "critical"
            )
            return result  # Early exit
        
        # 1c. Check system max limits (hard caps)
        if request.estimated_cost > system_policy.max_per_request_limit:
            result.add_violation(
                "system_policy",
                "exceeds_system_limit",
                f"Request cost ${request.estimated_cost:.2f} exceeds platform limit ${system_policy.max_per_request_limit:.2f}",
                "critical"
            )
            return result  # Early exit
        
        # STEP 2: Check USER policies
        result.policies_checked.append("user_policy")
        
        # 2a. CRITICAL: Validate provider whitelist
        if not self._validate_provider(request.api_provider, user_policy, result):
            return result  # Early exit on provider violation
        
        # 2b. CRITICAL: Validate model whitelist
        if not self._validate_model(request.model_name, request.api_provider, user_policy, result):
            return result  # Early exit on model violation
        
        # 2c. Check per-request cost limit
        if not self._validate_per_request_limit(request.estimated_cost, user_policy, result):
            pass  # Continue checking other policies
        
        # 2d. Check if policy is active
        if not user_policy.is_active:
            result.add_violation(
                "user_policy",
                "inactive_policy",
                f"Policy for user {request.user_id} is inactive",
                "critical"
            )
            return result
        
        # 2e. Check forbidden operations
        operation_key = f"{request.api_provider}.{request.model_name}.{request.operation_type}"
        if operation_key in user_policy.forbidden_operations:
            result.add_violation(
                "forbidden_operations",
                "operation_blocked",
                f"Operation {operation_key} is explicitly forbidden",
                "high"
            )
        
        # 2f. Check time-based restrictions
        if not self._validate_time_restrictions(user_policy, result):
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
        # Fixed: Changed from load_policy (undefined) to load_user_policy
        policy = await self.load_user_policy(user_id, project_id)
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
        # Fixed: Changed from load_policy (undefined) to load_user_policy
        policy = await self.load_user_policy(user_id, project_id)
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
            # Fixed: Changed self.cache to self.user_policy_cache
            if cache_key in self.user_policy_cache:
                del self.user_policy_cache[cache_key]
                logger.info(f"Cleared cache for {cache_key}")
        else:
            # Fixed: Changed self.cache to self.user_policy_cache
            self.user_policy_cache.clear()
            logger.info("Cleared entire policy cache")