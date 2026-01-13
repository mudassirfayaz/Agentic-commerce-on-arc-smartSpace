"""
Risk Assessment Models

Defines risk scoring and anomaly detection structures.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any
import requests
import logging

from ..config import config

logger = logging.getLogger(__name__)


class RiskScore(Enum):
    """Risk score categories (1-10 scale)"""
    VERY_LOW = "very_low"  # 1-2
    LOW = "low"  # 3-4
    MEDIUM = "medium"  # 5-6
    HIGH = "high"  # 7-8
    CRITICAL = "critical"  # 9-10


class RiskFactor(Enum):
    """Types of risk factors that can be detected"""
    # Volume-based
    UNUSUAL_VOLUME = "unusual_volume"
    SPIKE_IN_REQUESTS = "spike_in_requests"
    
    # Cost-based
    UNUSUALLY_HIGH_COST = "unusually_high_cost"
    COST_SPIKE = "cost_spike"
    
    # Pattern-based
    UNUSUAL_TIME = "unusual_time"
    UNUSUAL_PROVIDER = "unusual_provider"
    NEW_AGENT = "new_agent"
    UNKNOWN_AGENT = "unknown_agent"
    
    # Behavior-based
    REPEATED_REJECTIONS = "repeated_rejections"
    RAPID_RETRIES = "rapid_retries"
    PARAMETER_TAMPERING = "parameter_tampering"
    
    # Geographic
    UNUSUAL_LOCATION = "unusual_location"
    IMPOSSIBLE_TRAVEL = "impossible_travel"
    
    # Fraud indicators
    SUSPECTED_FRAUD = "suspected_fraud"
    COORDINATED_ATTACK = "coordinated_attack"
    ACCOUNT_COMPROMISE = "account_compromise"


@dataclass
class RiskAssessment:
    """
    Complete risk assessment for an API request.
    
    Example (Low Risk):
        assessment = RiskAssessment(
            request_id="req_abc123",
            score=2.0,
            category=RiskScore.VERY_LOW,
            factors=[],
            confidence=0.95,
            reasoning="Routine request from established user with normal patterns"
        )
    
    Example (High Risk):
        assessment = RiskAssessment(
            request_id="req_xyz789",
            score=8.0,
            category=RiskScore.HIGH,
            factors=[RiskFactor.COST_SPIKE, RiskFactor.UNUSUAL_PROVIDER],
            confidence=0.88,
            reasoning="Request cost 50x higher than baseline, using new provider"
        )
    """
    
    # Identifiers
    request_id: str
    assessment_id: str = field(default_factory=lambda: f"risk_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}")
    
    # Risk score (1-10)
    score: float = 0.0
    category: RiskScore = RiskScore.VERY_LOW
    
    # Risk factors detected
    factors: List[RiskFactor] = field(default_factory=list)
    factor_details: Dict[str, Any] = field(default_factory=dict)
    
    # Confidence in assessment (0-1)
    confidence: float = 1.0
    
    # Reasoning
    reasoning: str = ""
    recommendations: List[str] = field(default_factory=list)
    
    # Anomaly flags
    is_anomaly: bool = False
    anomaly_type: Optional[str] = None
    anomaly_severity: Optional[str] = None
    
    # Comparison with baseline
    baseline_comparison: Dict[str, Any] = field(default_factory=dict)
    
    # Timestamp
    assessed_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        """Set category based on score"""
        if self.score <= 2:
            self.category = RiskScore.VERY_LOW
        elif self.score <= 4:
            self.category = RiskScore.LOW
        elif self.score <= 6:
            self.category = RiskScore.MEDIUM
        elif self.score <= 8:
            self.category = RiskScore.HIGH
        else:
            self.category = RiskScore.CRITICAL
    
    def add_factor(self, factor: RiskFactor, details: Dict[str, Any]) -> None:
        """Add a risk factor with details"""
        if factor not in self.factors:
            self.factors.append(factor)
            self.factor_details[factor.value] = details
    
    def is_high_risk(self) -> bool:
        """Check if risk is high or critical"""
        return self.score >= 7
    
    def requires_escalation(self) -> bool:
        """Check if risk requires human escalation"""
        return self.score >= 7 or RiskFactor.SUSPECTED_FRAUD in self.factors
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "request_id": self.request_id,
            "assessment_id": self.assessment_id,
            "score": self.score,
            "category": self.category.value,
            "factors": [f.value for f in self.factors],
            "factor_details": self.factor_details,
            "confidence": self.confidence,
            "reasoning": self.reasoning,
            "recommendations": self.recommendations,
            "is_anomaly": self.is_anomaly,
            "anomaly_type": self.anomaly_type,
            "anomaly_severity": self.anomaly_severity,
            "baseline_comparison": self.baseline_comparison,
            "assessed_at": self.assessed_at.isoformat(),
        }
    
    @classmethod
    def assess_from_backend(cls, request_id: str, user_id: str, project_id: str, request_data: Dict[str, Any]) -> 'RiskAssessment':
        """
        Perform risk assessment via backend API.
        
        Args:
            request_id: Request identifier
            user_id: User identifier
            project_id: Project identifier
            request_data: Request details for analysis
            
        Returns:
            RiskAssessment object
        """
        try:
            url = config.get_endpoint('risk', 'assess_risk')
            data = {
                'request_id': request_id,
                'user_id': user_id,
                'project_id': project_id,
                'request_data': request_data
            }
            response = requests.post(url, json=data, timeout=config.API_TIMEOUT)
            response.raise_for_status()
            result = response.json()
            
            factors = []
            for factor_value in result.get('factors', []):
                try:
                    factors.append(RiskFactor(factor_value))
                except ValueError:
                    logger.warning(f"Unknown risk factor: {factor_value}")
            
            category_value = result.get('category', 'very_low')
            try:
                category = RiskScore(category_value)
            except ValueError:
                category = RiskScore.VERY_LOW
            
            return cls(
                request_id=request_id,
                assessment_id=result.get('assessment_id', ''),
                score=result.get('score', 0.0),
                category=category,
                factors=factors,
                factor_details=result.get('factor_details', {}),
                confidence=result.get('confidence', 1.0),
                reasoning=result.get('reasoning', ''),
                recommendations=result.get('recommendations', []),
                is_anomaly=result.get('is_anomaly', False),
                anomaly_type=result.get('anomaly_type'),
                anomaly_severity=result.get('anomaly_severity'),
                baseline_comparison=result.get('baseline_comparison', {}),
            )
        except Exception as e:
            logger.error(f"Failed to assess risk from backend: {e}")
            raise


@dataclass
class UserBaseline:
    """
    Baseline behavioral patterns for a user (for anomaly detection).
    """
    
    user_id: str
    project_id: str
    
    # Cost patterns
    average_request_cost: float = 0.0
    median_request_cost: float = 0.0
            "sample_size": self.sample_size,
            "last_updated": self.last_updated.isoformat(),
        }
    
    @classmethod
    def fetch_from_backend(cls, user_id: str, project_id: str) -> 'UserBaseline':
        """
        Fetch user behavioral baseline from backend.
        
        Args:
            user_id: User identifier
            project_id: Project identifier
            
        Returns:
            UserBaseline object
        """
        try:
            url = config.get_endpoint('risk', 'get_baseline', user_id=user_id, project_id=project_id)
            response = requests.get(url, timeout=config.API_TIMEOUT)
            response.raise_for_status()
            data = response.json()
            
            return cls(
                user_id=data['user_id'],
                project_id=data['project_id'],
                average_request_cost=data.get('average_request_cost', 0.0),
                median_request_cost=data.get('median_request_cost', 0.0),
                max_request_cost=data.get('max_request_cost', 0.0),
                cost_std_dev=data.get('cost_std_dev', 0.0),
                average_requests_per_day=data.get('average_requests_per_day', 0.0),
                average_requests_per_hour=data.get('average_requests_per_hour', 0.0),
                peak_request_times=data.get('peak_request_times', []),
                typical_providers=data.get('typical_providers', []),
                provider_distribution=data.get('provider_distribution', {}),
                typical_models=data.get('typical_models', []),
                model_distribution=data.get('model_distribution', {}),
                typical_days=data.get('typical_days', []),
                typical_hours=data.get('typical_hours', []),
                sample_size=data.get('sample_size', 0),
            )
        except Exception as e:
            logger.error(f"Failed to fetch baseline from backend: {e}")
            raise

    # Volume patterns
    average_requests_per_day: float = 0.0
    average_requests_per_hour: float = 0.0
    peak_request_times: List[int] = field(default_factory=list)  # Hours
    
    # Provider patterns
    typical_providers: List[str] = field(default_factory=list)
    provider_distribution: Dict[str, float] = field(default_factory=dict)
    
    # Model patterns
    typical_models: List[str] = field(default_factory=list)
    model_distribution: Dict[str, float] = field(default_factory=dict)
    
    # Time patterns
    typical_days: List[int] = field(default_factory=list)  # Days of week
    typical_hours: List[int] = field(default_factory=list)  # Hours of day
    
    # Metadata
    baseline_period_start: datetime = field(default_factory=datetime.utcnow)
    baseline_period_end: datetime = field(default_factory=datetime.utcnow)
    sample_size: int = 0
    last_updated: datetime = field(default_factory=datetime.utcnow)
    
    def is_cost_anomaly(self, cost: float, threshold_multiplier: float = 3.0) -> bool:
        """Check if cost is anomalous (> threshold * std_dev from mean)"""
        if self.cost_std_dev == 0:
            return cost > (self.average_request_cost * threshold_multiplier)
        
        deviation = abs(cost - self.average_request_cost)
        return deviation > (threshold_multiplier * self.cost_std_dev)
    
    def is_volume_anomaly(self, current_rate: float, threshold_multiplier: float = 2.0) -> bool:
        """Check if request volume is anomalous"""
        return current_rate > (self.average_requests_per_hour * threshold_multiplier)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "user_id": self.user_id,
            "project_id": self.project_id,
            "average_request_cost": self.average_request_cost,
            "median_request_cost": self.median_request_cost,
            "max_request_cost": self.max_request_cost,
            "cost_std_dev": self.cost_std_dev,
            "average_requests_per_day": self.average_requests_per_day,
            "average_requests_per_hour": self.average_requests_per_hour,
            "peak_request_times": self.peak_request_times,
            "typical_providers": self.typical_providers,
            "provider_distribution": self.provider_distribution,
            "typical_models": self.typical_models,
            "model_distribution": self.model_distribution,
            "typical_days": self.typical_days,
            "typical_hours": self.typical_hours,
            "baseline_period_start": self.baseline_period_start.isoformat(),
            "baseline_period_end": self.baseline_period_end.isoformat(),
            "sample_size": self.sample_size,
            "last_updated": self.last_updated.isoformat(),
        }
