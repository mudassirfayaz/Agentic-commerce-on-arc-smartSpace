"""
User baseline tracking and analysis.

Tracks user behavior patterns over time to establish normal usage baselines.
Used by risk detection system to identify anomalies.

Key responsibilities:
- Track request patterns
- Calculate average costs
- Monitor typical providers/models
- Identify usage time patterns
- Build behavior profiles
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional, List, Set, Dict
import logging

from config import Config
from models.risk import UserBaseline

# Configure logging
logger = logging.getLogger(__name__)


class BaselineTracker:
    """
    User baseline behavior tracker.
    
    Analyzes historical data to build baseline profiles for anomaly detection.
    Operates in READ-ONLY mode - fetches and analyzes backend data.
    """
    
    def __init__(self):
        """Initialize baseline tracker."""
        self.config = Config()
    
    def get_baseline(
        self,
        user_id: str,
        project_id: str,
        lookback_days: int = 30
    ) -> Optional[UserBaseline]:
        """
        Get user baseline from backend.
        
        Args:
            user_id: User identifier
            project_id: Project identifier
            lookback_days: Days of history to analyze (default: 30)
            
        Returns:
            UserBaseline or None if insufficient data
        """
        try:
            baseline = UserBaseline.fetch_from_backend(
                user_id=user_id,
                project_id=project_id,
                lookback_days=lookback_days
            )
            
            if baseline:
                logger.info(
                    f"Loaded baseline for {user_id}/{project_id}: "
                    f"{baseline.total_requests} requests, "
                    f"${baseline.average_request_cost:.4f} avg cost"
                )
            else:
                logger.warning(
                    f"No baseline found for {user_id}/{project_id}"
                )
            
            return baseline
            
        except Exception as e:
            logger.error(f"Failed to fetch baseline: {e}")
            return None
    
    def analyze_baseline_quality(
        self,
        baseline: UserBaseline
    ) -> Dict[str, any]:
        """
        Analyze quality and completeness of baseline.
        
        Args:
            baseline: UserBaseline to analyze
            
        Returns:
            Dictionary with quality metrics
        """
        quality = {
            "sufficient_data": baseline.total_requests >= 10,
            "has_cost_data": baseline.average_request_cost > 0,
            "has_provider_patterns": len(baseline.typical_providers) > 0,
            "has_model_patterns": len(baseline.typical_models) > 0,
            "has_time_patterns": len(baseline.typical_hours) > 0,
            "confidence_level": "low"
        }
        
        # Determine confidence level
        if baseline.total_requests >= 100:
            quality["confidence_level"] = "high"
        elif baseline.total_requests >= 30:
            quality["confidence_level"] = "medium"
        elif baseline.total_requests >= 10:
            quality["confidence_level"] = "low"
        else:
            quality["confidence_level"] = "insufficient"
        
        # Calculate completeness score (0-100)
        completeness = 0
        if quality["has_cost_data"]:
            completeness += 25
        if quality["has_provider_patterns"]:
            completeness += 25
        if quality["has_model_patterns"]:
            completeness += 25
        if quality["has_time_patterns"]:
            completeness += 25
        
        quality["completeness_score"] = completeness
        
        return quality
    
    def get_baseline_summary(
        self,
        baseline: UserBaseline
    ) -> str:
        """
        Get human-readable baseline summary.
        
        Args:
            baseline: UserBaseline to summarize
            
        Returns:
            Summary string
        """
        quality = self.analyze_baseline_quality(baseline)
        
        summary_parts = [
            f"Baseline: {baseline.total_requests} requests over {baseline.lookback_days} days",
            f"Avg cost: ${baseline.average_request_cost:.4f}",
            f"Avg requests/day: {baseline.average_requests_per_day:.1f}",
            f"Confidence: {quality['confidence_level']}",
            f"Completeness: {quality['completeness_score']}%"
        ]
        
        if baseline.typical_providers:
            summary_parts.append(
                f"Providers: {', '.join(list(baseline.typical_providers)[:3])}"
            )
        
        if baseline.typical_models:
            summary_parts.append(
                f"Models: {len(baseline.typical_models)} tracked"
            )
        
        return " | ".join(summary_parts)
    
    def compare_to_baseline(
        self,
        current_value: float,
        baseline_average: float,
        metric_name: str = "value"
    ) -> Dict[str, any]:
        """
        Compare current value to baseline average.
        
        Args:
            current_value: Current metric value
            baseline_average: Baseline average for comparison
            metric_name: Name of metric being compared
            
        Returns:
            Dictionary with comparison results
        """
        if baseline_average == 0:
            return {
                "is_anomaly": current_value > 10,  # Absolute threshold
                "deviation": 0,
                "severity": "unknown",
                "message": f"No baseline for {metric_name}"
            }
        
        deviation = (current_value - baseline_average) / baseline_average
        
        # Determine if anomalous
        is_anomaly = abs(deviation) > 2.0  # 2x deviation
        
        # Determine severity
        if abs(deviation) > 5.0:
            severity = "critical"
        elif abs(deviation) > 3.0:
            severity = "high"
        elif abs(deviation) > 2.0:
            severity = "medium"
        elif abs(deviation) > 1.0:
            severity = "low"
        else:
            severity = "normal"
        
        return {
            "is_anomaly": is_anomaly,
            "deviation": deviation,
            "severity": severity,
            "current_value": current_value,
            "baseline_average": baseline_average,
            "message": (
                f"{metric_name}: {current_value:.2f} vs baseline {baseline_average:.2f} "
                f"({deviation:+.1%} deviation)"
            )
        }
