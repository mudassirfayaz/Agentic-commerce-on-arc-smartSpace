"""
Risk detection and anomaly analysis system.

Analyzes requests for fraud patterns, unusual activity, and suspicious behavior.
Provides risk scoring on a 1-10 scale to help make approval decisions.

Key responsibilities:
- Analyze request patterns against user baseline
- Detect spending anomalies
- Identify unusual provider/model usage
- Check for rate limit violations
- Detect geographic anomalies
- Score overall risk level
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional, List, Dict
from enum import Enum
import logging

from config import Config
from models.request import APIRequest
from models.risk import RiskAssessment, UserBaseline
from models.user import UserContext

# Configure logging
logger = logging.getLogger(__name__)


class AnomalyType(str, Enum):
    """Types of anomalies that can be detected."""
    COST_SPIKE = "cost_spike"
    RATE_SPIKE = "rate_spike"
    UNUSUAL_PROVIDER = "unusual_provider"
    UNUSUAL_MODEL = "unusual_model"
    UNUSUAL_TIME = "unusual_time"
    GEOGRAPHIC = "geographic"
    NEW_AGENT = "new_agent"
    REPEATED_REJECTIONS = "repeated_rejections"
    BUDGET_EXHAUSTION = "budget_exhaustion"


@dataclass
class RiskFactor:
    """Individual risk factor contributing to overall score."""
    factor_type: str
    description: str
    risk_contribution: float  # 0.0 to 10.0
    severity: str  # "low", "medium", "high", "critical"
    details: Dict = field(default_factory=dict)


@dataclass
class RiskAssessmentResult:
    """Result of risk assessment with detailed breakdown."""
    request_id: str
    user_id: str
    project_id: str
    
    # Overall risk score (1-10)
    risk_score: float
    risk_level: str  # "very_low", "low", "medium", "high", "critical"
    
    # Risk factors
    risk_factors: List[RiskFactor] = field(default_factory=list)
    anomalies: List[AnomalyType] = field(default_factory=list)
    
    # Recommendation
    recommended_action: str = "approve"  # "approve", "review", "reject"
    confidence: float = 0.9  # 0.0 to 1.0
    
    # Metadata
    assessed_at: datetime = field(default_factory=datetime.utcnow)
    baseline_used: bool = False
    
    def __post_init__(self):
        """Determine risk level and recommendation from score."""
        if self.risk_score <= 2.0:
            self.risk_level = "very_low"
            self.recommended_action = "approve"
        elif self.risk_score <= 4.0:
            self.risk_level = "low"
            self.recommended_action = "approve"
        elif self.risk_score <= 6.0:
            self.risk_level = "medium"
            self.recommended_action = "approve"
        elif self.risk_score <= 8.0:
            self.risk_level = "high"
            self.recommended_action = "review"
        else:
            self.risk_level = "critical"
            self.recommended_action = "reject"
    
    def get_summary(self) -> str:
        """Get human-readable summary."""
        return f"Risk: {self.risk_level} ({self.risk_score:.1f}/10) - {self.recommended_action}"


class RiskDetector:
    """
    Risk detection and anomaly analysis system.
    
    Analyzes requests against user baselines and detects suspicious patterns.
    Operates in READ-ONLY mode - fetches data and calculates risk scores.
    """
    
    def __init__(self):
        """Initialize risk detector."""
        self.config = Config()
    
    async def assess_risk(
        self,
        request: APIRequest,
        user_context: UserContext
    ) -> RiskAssessmentResult:
        """
        Assess risk for a request.
        
        Args:
            request: The API request to assess
            user_context: User's context and baseline
            
        Returns:
            RiskAssessmentResult with score and factors
        """
        result = RiskAssessmentResult(
            request_id=request.request_id,
            user_id=request.user_id,
            project_id=request.project_id
        )
        
        # Fetch user baseline from backend
        baseline = await self._fetch_baseline(request.user_id, request.project_id)
        result.baseline_used = baseline is not None
        
        # Calculate risk factors
        risk_score = 1.0  # Start with baseline low risk
        
        # 1. Check cost anomalies
        cost_risk = await self._check_cost_anomaly(request, user_context, baseline)
        if cost_risk:
            result.risk_factors.append(cost_risk)
            risk_score += cost_risk.risk_contribution
            result.anomalies.append(AnomalyType.COST_SPIKE)
        
        # 2. Check rate anomalies
        rate_risk = await self._check_rate_anomaly(request, user_context, baseline)
        if rate_risk:
            result.risk_factors.append(rate_risk)
            risk_score += rate_risk.risk_contribution
            result.anomalies.append(AnomalyType.RATE_SPIKE)
        
        # 3. Check unusual provider
        provider_risk = await self._check_unusual_provider(request, user_context, baseline)
        if provider_risk:
            result.risk_factors.append(provider_risk)
            risk_score += provider_risk.risk_contribution
            result.anomalies.append(AnomalyType.UNUSUAL_PROVIDER)
        
        # 4. Check unusual model
        model_risk = await self._check_unusual_model(request, user_context, baseline)
        if model_risk:
            result.risk_factors.append(model_risk)
            risk_score += model_risk.risk_contribution
            result.anomalies.append(AnomalyType.UNUSUAL_MODEL)
        
        # 5. Check unusual time
        time_risk = await self._check_unusual_time(request, user_context, baseline)
        if time_risk:
            result.risk_factors.append(time_risk)
            risk_score += time_risk.risk_contribution
            result.anomalies.append(AnomalyType.UNUSUAL_TIME)
        
        # 6. Check new agent
        agent_risk = await self._check_new_agent(request, user_context)
        if agent_risk:
            result.risk_factors.append(agent_risk)
            risk_score += agent_risk.risk_contribution
            result.anomalies.append(AnomalyType.NEW_AGENT)
        
        # 7. Check repeated rejections
        rejection_risk = await self._check_repeated_rejections(user_context)
        if rejection_risk:
            result.risk_factors.append(rejection_risk)
            risk_score += rejection_risk.risk_contribution
            result.anomalies.append(AnomalyType.REPEATED_REJECTIONS)
        
        # 8. Check budget exhaustion pattern
        budget_risk = await self._check_budget_exhaustion(request, user_context)
        if budget_risk:
            result.risk_factors.append(budget_risk)
            risk_score += budget_risk.risk_contribution
            result.anomalies.append(AnomalyType.BUDGET_EXHAUSTION)
        
        # Cap risk score at 10.0
        result.risk_score = min(risk_score, 10.0)
        
        logger.info(f"Risk assessment: {result.get_summary()}")
        return result
    
    async def _fetch_baseline(
        self, 
        user_id: str, 
        project_id: str
    ) -> Optional[UserBaseline]:
        """
        Fetch user baseline from backend.
        
        Args:
            user_id: User identifier
            project_id: Project identifier
            
        Returns:
            UserBaseline or None if not found
        """
        try:
            baseline = UserBaseline.fetch_from_backend(user_id, project_id)
            return baseline
        except Exception as e:
            logger.warning(f"Could not fetch baseline: {e}")
            return None
    
    async def _check_cost_anomaly(
        self,
        request: APIRequest,
        user_context: UserContext,
        baseline: Optional[UserBaseline]
    ) -> Optional[RiskFactor]:
        """Check if request cost is anomalous."""
        if not baseline or baseline.average_request_cost == 0:
            # No baseline - check against absolute thresholds
            if request.estimated_cost > 10.0:
                return RiskFactor(
                    factor_type="high_cost",
                    description="High cost request without baseline",
                    risk_contribution=2.0,
                    severity="medium",
                    details={"cost": request.estimated_cost}
                )
            return None
        
        # Compare to user's average
        deviation = (request.estimated_cost - baseline.average_request_cost) / baseline.average_request_cost
        
        if deviation > 3.0:  # More than 3x average
            return RiskFactor(
                factor_type="cost_spike",
                description=f"Cost is {deviation:.1f}x higher than user average",
                risk_contribution=min(3.0, deviation),
                severity="high",
                details={
                    "request_cost": request.estimated_cost,
                    "average_cost": baseline.average_request_cost,
                    "deviation": deviation
                }
            )
        elif deviation > 2.0:  # More than 2x average
            return RiskFactor(
                factor_type="cost_spike",
                description=f"Cost is {deviation:.1f}x higher than user average",
                risk_contribution=1.5,
                severity="medium",
                details={
                    "request_cost": request.estimated_cost,
                    "average_cost": baseline.average_request_cost,
                    "deviation": deviation
                }
            )
        
        return None
    
    async def _check_rate_anomaly(
        self,
        request: APIRequest,
        user_context: UserContext,
        baseline: Optional[UserBaseline]
    ) -> Optional[RiskFactor]:
        """Check if request rate is anomalous."""
        # Check today's request count
        if user_context.total_requests_today > 100:
            if not baseline or user_context.total_requests_today > baseline.average_requests_per_day * 3:
                return RiskFactor(
                    factor_type="rate_spike",
                    description="Unusual spike in request volume",
                    risk_contribution=2.0,
                    severity="high",
                    details={
                        "requests_today": user_context.total_requests_today,
                        "average_per_day": baseline.average_requests_per_day if baseline else 0
                    }
                )
        
        return None
    
    async def _check_unusual_provider(
        self,
        request: APIRequest,
        user_context: UserContext,
        baseline: Optional[UserBaseline]
    ) -> Optional[RiskFactor]:
        """Check if provider is unusual for this user."""
        if not baseline or not baseline.typical_providers:
            return None
        
        if request.api_provider not in baseline.typical_providers:
            return RiskFactor(
                factor_type="unusual_provider",
                description=f"Provider '{request.api_provider}' not in user's typical usage",
                risk_contribution=1.0,
                severity="low",
                details={
                    "requested_provider": request.api_provider,
                    "typical_providers": baseline.typical_providers
                }
            )
        
        return None
    
    async def _check_unusual_model(
        self,
        request: APIRequest,
        user_context: UserContext,
        baseline: Optional[UserBaseline]
    ) -> Optional[RiskFactor]:
        """Check if model is unusual for this user."""
        if not baseline or not baseline.typical_models:
            return None
        
        model_key = f"{request.api_provider}/{request.model_name}"
        if model_key not in baseline.typical_models:
            return RiskFactor(
                factor_type="unusual_model",
                description=f"Model '{model_key}' not in user's typical usage",
                risk_contribution=0.5,
                severity="low",
                details={
                    "requested_model": model_key,
                    "typical_models": baseline.typical_models
                }
            )
        
        return None
    
    async def _check_unusual_time(
        self,
        request: APIRequest,
        user_context: UserContext,
        baseline: Optional[UserBaseline]
    ) -> Optional[RiskFactor]:
        """Check if request time is unusual for this user."""
        if not baseline or not baseline.typical_hours:
            return None
        
        current_hour = datetime.utcnow().hour
        
        if current_hour not in baseline.typical_hours:
            return RiskFactor(
                factor_type="unusual_time",
                description=f"Request at unusual hour ({current_hour}:00) for this user",
                risk_contribution=0.5,
                severity="low",
                details={
                    "current_hour": current_hour,
                    "typical_hours": baseline.typical_hours
                }
            )
        
        return None
    
    async def _check_new_agent(
        self,
        request: APIRequest,
        user_context: UserContext
    ) -> Optional[RiskFactor]:
        """Check if request is from a new/unknown agent."""
        if request.agent_id and request.agent_id not in user_context.agents:
            return RiskFactor(
                factor_type="new_agent",
                description=f"Request from new agent: {request.agent_id}",
                risk_contribution=1.5,
                severity="medium",
                details={
                    "agent_id": request.agent_id,
                    "known_agents": user_context.agents
                }
            )
        
        return None
    
    async def _check_repeated_rejections(
        self,
        user_context: UserContext
    ) -> Optional[RiskFactor]:
        """Check for pattern of repeated rejections."""
        if user_context.recent_rejections >= 5:
            return RiskFactor(
                factor_type="repeated_rejections",
                description="Multiple recent rejections detected",
                risk_contribution=2.0,
                severity="high",
                details={
                    "recent_rejections": user_context.recent_rejections
                }
            )
        elif user_context.recent_rejections >= 3:
            return RiskFactor(
                factor_type="repeated_rejections",
                description="Several recent rejections detected",
                risk_contribution=1.0,
                severity="medium",
                details={
                    "recent_rejections": user_context.recent_rejections
                }
            )
        
        return None
    
    async def _check_budget_exhaustion(
        self,
        request: APIRequest,
        user_context: UserContext
    ) -> Optional[RiskFactor]:
        """Check if user is trying to exhaust budget quickly."""
        if not user_context.policy:
            return None
        
        # Check if user is spending close to daily limit
        remaining_daily = user_context.get_remaining_daily_budget()
        daily_limit = user_context.policy.daily_budget
        
        if daily_limit > 0:
            usage_percent = ((daily_limit - remaining_daily) / daily_limit) * 100
            
            if usage_percent > 90 and user_context.total_requests_today > 50:
                return RiskFactor(
                    factor_type="budget_exhaustion",
                    description=f"Rapid budget consumption ({usage_percent:.0f}% used)",
                    risk_contribution=1.5,
                    severity="medium",
                    details={
                        "usage_percent": usage_percent,
                        "requests_today": user_context.total_requests_today
                    }
                )
        
        return None
