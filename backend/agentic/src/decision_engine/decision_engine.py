"""
Autonomous Payment Decision Engine

The core decision engine that orchestrates all components to make
intelligent, policy-compliant decisions about API requests.

This engine:
1. Validates request structure
2. Loads user context & policies
3. Validates provider/model whitelist
4. Estimates costs
5. Checks budget availability
6. Validates against policies
7. Assesses risk
8. Routes to appropriate agent tier
9. Gets AI decision
10. Logs everything
11. Executes payment if approved
12. Returns decision with receipt
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, Optional

from models.request import APIRequest
from models.decision import Decision, DecisionOutcome
from models.user import UserContext
from policies.policy_manager import PolicyManager
from budgets.budget_tracker import BudgetTracker
from pricing.pricing_engine import PricingEngine
from risk.risk_detector import RiskDetector
from risk.baseline_tracker import BaselineTracker
from payments.payment_executor import PaymentExecutor
from audit_logging.audit_logger import AuditLogger
from evaluators.flash_evaluator import FlashEvaluator
from evaluators.pro_evaluator import ProEvaluator

logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Result of request validation"""
    valid: bool
    error: Optional[str] = None


@dataclass
class ProviderModelValidation:
    """Result of provider/model whitelist validation"""
    valid: bool
    reason: Optional[str] = None
    rejection_type: Optional[str] = None


@dataclass
class RequestContext:
    """Complete context for decision making"""
    user_context: UserContext
    policies: Dict[str, Any]
    cost_estimate: float
    budget_check: Dict[str, Any]
    policy_check: Dict[str, Any]
    risk_assessment: Any
    provider_model_check: ProviderModelValidation


class AutonomousPaymentDecisionEngine:
    """
    The core decision engine coordinating all components.
    Ensures deterministic, auditable, policy-compliant decisions.
    
    This is the "brain" that makes autonomous decisions about whether
    to approve and pay for API requests based on policies, budgets, and risk.
    """
    
    def __init__(self):
        """Initialize all decision engine components"""
        self.policy_manager = PolicyManager()
        self.budget_tracker = BudgetTracker()
        self.pricing_engine = PricingEngine()
        self.risk_detector = RiskDetector()
        self.baseline_tracker = BaselineTracker()
        self.payment_executor = PaymentExecutor()
        self.audit_logger = AuditLogger(log_dir="audit_logs")
        
        # AI decision agents
        self.flash_agent = FlashEvaluator()
        self.pro_agent = ProEvaluator()
        
        logger.info("🧠 Decision Engine initialized")
    
    async def process_request(
        self,
        request: APIRequest
    ) -> Decision:
        """
        Main decision pipeline - orchestrates all checks and AI reasoning.
        
        This is the complete flow from receiving a request to returning
        a decision (approved or rejected) with full audit trail.
        
        Args:
            request: The API request to process
            
        Returns:
            Decision with outcome, reasoning, and receipt
        """
        start_time = datetime.utcnow()
        
        try:
            # Step 1: Validate request structure
            logger.info(f"📋 Step 1: Validating request structure...")
            validation = await self._validate_request_structure(request)
            if not validation.valid:
                await self.audit_logger.log_error(
                    request_id=request.request_id,
                    user_id=request.user_id,
                    project_id=request.project_id,
                    error=f"Invalid request: {validation.error}",
                    error_details={'validation_error': validation.error}
                )
                return Decision(
                    request_id=request.request_id,
                    outcome=DecisionOutcome.REJECTED,
                    rejection_reason=f"Invalid request: {validation.error}",
                    reasoning="Request validation failed",
                    confidence=1.0,
                    agent_tier="SYSTEM"
                )
            
            # Step 2: Load user context
            logger.info(f"👤 Step 2: Loading user context...")
            user_context = UserContext.fetch_from_backend(
                request.user_id,
                request.project_id
            )
            
            # Step 3: Load policies
            logger.info(f"📜 Step 3: Loading policies...")
            system_policy, user_policy = await self._load_policies(
                request.user_id,
                request.project_id
            )
            
            # Step 4: CRITICAL - Validate provider/model are in user's whitelist
            logger.info(f"🔐 Step 4: Validating provider/model whitelist...")
            provider_model_check = await self._validate_provider_model(
                request,
                user_policy
            )
            
            if not provider_model_check.valid:
                await self.audit_logger.log_policy_check(
                    request_id=request.request_id,
                    user_id=request.user_id,
                    project_id=request.project_id,
                    policies_checked=['provider_whitelist', 'model_whitelist'],
                    results={'validation': provider_model_check.reason},
                    compliant=False
                )
                
                return Decision(
                    request_id=request.request_id,
                    outcome=DecisionOutcome.REJECTED,
                    rejection_reason=provider_model_check.reason,
                    reasoning="Provider or model not in user's whitelist",
                    confidence=1.0,
                    agent_tier="SYSTEM"
                )
            
            # Step 5: Estimate cost
            logger.info(f"💰 Step 5: Estimating cost...")
            cost_estimate = self.pricing_engine.estimate_cost(
                request.api_provider,
                request.model_name,
                request.estimated_tokens
            )
            request.estimated_cost = cost_estimate
            
            # Step 6: Check budget
            logger.info(f"💵 Step 6: Checking budget...")
            budget_check = self.budget_tracker.check_sufficient_budget(
                user_id=request.user_id,
                project_id=request.project_id,
                amount=cost_estimate
            )
            
            if not budget_check['sufficient']:
                await self.audit_logger.log_budget_check(
                    request_id=request.request_id,
                    user_id=request.user_id,
                    project_id=request.project_id,
                    estimated_cost=cost_estimate,
                    available_budget=budget_check.get('available_balance', 0.0),
                    budget_approved=False
                )
                
                return Decision(
                    request_id=request.request_id,
                    outcome=DecisionOutcome.REJECTED,
                    rejection_reason=f"Insufficient budget: ${budget_check.get('available_balance', 0):.2f} available, ${cost_estimate:.2f} required",
                    reasoning="Budget check failed",
                    confidence=1.0,
                    agent_tier="SYSTEM"
                )
            
            # Step 7: Check policy compliance
            logger.info(f"✅ Step 7: Checking policy compliance...")
            policy_check = self.policy_manager.check_compliance(
                request,
                user_policy,
                system_policy
            )
            
            if not policy_check['compliant']:
                await self.audit_logger.log_policy_check(
                    request_id=request.request_id,
                    user_id=request.user_id,
                    project_id=request.project_id,
                    policies_checked=policy_check.get('checks_performed', []),
                    results=policy_check,
                    compliant=False
                )
                
                return Decision(
                    request_id=request.request_id,
                    outcome=DecisionOutcome.REJECTED,
                    rejection_reason=f"Policy violation: {policy_check['violations'][0]}",
                    reasoning="Policy compliance check failed",
                    confidence=1.0,
                    agent_tier="SYSTEM"
                )
            
            # Step 8: Assess risk
            logger.info(f"⚠️ Step 8: Assessing risk...")
            risk_assessment = self.risk_detector.analyze_request(
                request,
                user_context,
                historical_data=self.baseline_tracker.get_user_baseline(request.user_id)
            )
            
            await self.audit_logger.log_risk_assessment(
                request_id=request.request_id,
                user_id=request.user_id,
                project_id=request.project_id,
                risk_score=risk_assessment.risk_score,
                risk_factors=risk_assessment.risk_factors,
                risk_level=risk_assessment.risk_level
            )
            
            # Step 9: Build request context
            request_context = RequestContext(
                user_context=user_context,
                policies={'system': system_policy, 'user': user_policy},
                cost_estimate=cost_estimate,
                budget_check=budget_check,
                policy_check=policy_check,
                risk_assessment=risk_assessment,
                provider_model_check=provider_model_check
            )
            
            # Step 10: Route to appropriate agent tier and get decision
            logger.info(f"🎯 Step 10: Routing to agent tier...")
            decision = await self._route_and_decide(request, request_context)
            
            # Log agent decision
            await self.audit_logger.log_agent_decision(
                request_id=request.request_id,
                user_id=request.user_id,
                project_id=request.project_id,
                agent_id=decision.agent_id or 'system',
                agent_tier=decision.agent_tier,
                decision=decision.outcome.value,
                reasoning=decision.reasoning,
                decision_details={
                    'risk_score': risk_assessment.risk_score,
                    'estimated_cost': cost_estimate,
                    'approval_confidence': decision.confidence
                }
            )
            
            # Calculate processing time
            duration = (datetime.utcnow() - start_time).total_seconds()
            logger.info(f"✅ Decision completed in {duration:.2f}s: {decision.outcome.value}")
            
            return decision
            
        except Exception as e:
            logger.error(f"❌ Error in decision engine: {e}", exc_info=True)
            
            await self.audit_logger.log_error(
                request_id=request.request_id,
                user_id=request.user_id,
                project_id=request.project_id,
                error=str(e),
                error_details={'exception_type': type(e).__name__}
            )
            
            return Decision(
                request_id=request.request_id,
                outcome=DecisionOutcome.ERROR,
                rejection_reason=f"System error: {e}",
                reasoning="Decision engine encountered an error",
                confidence=0.0,
                agent_tier="SYSTEM"
            )
    
    async def _validate_request_structure(
        self,
        request: APIRequest
    ) -> ValidationResult:
        """
        Validate request has all required fields.
        
        Checks:
        - Required fields present
        - Valid data types
        - Valid enum values
        - Reasonable token estimates
        """
        try:
            # Check required fields
            required_fields = [
                'request_id', 'user_id', 'project_id',
                'api_provider', 'model_name', 'endpoint'
            ]
            
            for field in required_fields:
                if not getattr(request, field, None):
                    return ValidationResult(
                        valid=False,
                        error=f"Missing required field: {field}"
                    )
            
            # Validate token estimate is reasonable
            if request.estimated_tokens and request.estimated_tokens < 0:
                return ValidationResult(
                    valid=False,
                    error="Invalid token estimate: must be positive"
                )
            
            if request.estimated_tokens and request.estimated_tokens > 1000000:
                return ValidationResult(
                    valid=False,
                    error="Invalid token estimate: exceeds maximum (1M tokens)"
                )
            
            return ValidationResult(valid=True)
            
        except Exception as e:
            return ValidationResult(
                valid=False,
                error=f"Validation error: {e}"
            )
    
    async def _load_policies(
        self,
        user_id: str,
        project_id: str
    ) -> tuple:
        """Load system and user policies"""
        system_policy = self.policy_manager.load_system_policy()
        user_policy = self.policy_manager.load_user_policy(user_id, project_id)
        return system_policy, user_policy
    
    async def _validate_provider_model(
        self,
        request: APIRequest,
        user_policy: Any
    ) -> ProviderModelValidation:
        """
        CRITICAL: Validate provider and model are in user's whitelist.
        
        This ensures agents ONLY use providers and models that users
        have explicitly configured and approved.
        """
        # Get allowed providers from policy
        allowed_providers = user_policy.allowed_providers if user_policy else []
        
        if not allowed_providers:
            return ProviderModelValidation(
                valid=False,
                reason="No providers configured for this project",
                rejection_type="NO_PROVIDERS_CONFIGURED"
            )
        
        # Check if provider is allowed
        if request.api_provider not in allowed_providers:
            return ProviderModelValidation(
                valid=False,
                reason=f"Provider '{request.api_provider}' not in allowed list: {allowed_providers}",
                rejection_type="UNAUTHORIZED_PROVIDER"
            )
        
        # Get allowed models for this provider
        allowed_models = user_policy.allowed_models.get(request.api_provider, []) if user_policy else []
        
        if not allowed_models:
            return ProviderModelValidation(
                valid=False,
                reason=f"No models configured for provider '{request.api_provider}'",
                rejection_type="NO_MODELS_CONFIGURED"
            )
        
        # Check if model is allowed
        if request.model_name not in allowed_models:
            return ProviderModelValidation(
                valid=False,
                reason=f"Model '{request.model_name}' not in allowed list for '{request.api_provider}': {allowed_models}",
                rejection_type="UNAUTHORIZED_MODEL"
            )
        
        return ProviderModelValidation(valid=True)
    
    async def _route_and_decide(
        self,
        request: APIRequest,
        context: RequestContext
    ) -> Decision:
        """
        Route request to appropriate agent tier and get decision.
        
        Routing logic:
        - Low cost (<$1) + Low risk (<5) → Flash Agent (fast, cheap)
        - High cost (≥$1) OR High risk (≥5) → Pro Agent (thorough, expensive)
        """
        cost = context.cost_estimate
        risk_score = context.risk_assessment.risk_score
        
        # Determine agent tier
        if cost < 1.0 and risk_score < 5.0:
            agent_tier = "FLASH"
            agent = self.flash_agent
            logger.info(f"⚡ Routing to Flash Agent (cost=${cost:.4f}, risk={risk_score:.1f})")
        else:
            agent_tier = "PRO"
            agent = self.pro_agent
            logger.info(f"🎓 Routing to Pro Agent (cost=${cost:.4f}, risk={risk_score:.1f})")
        
        # Get AI decision
        decision = agent.evaluate(request, context)
        decision.agent_tier = agent_tier
        decision.risk_score = risk_score
        
        return decision
