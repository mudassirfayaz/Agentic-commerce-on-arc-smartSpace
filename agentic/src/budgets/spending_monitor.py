"""
Spending monitor for alerts and threshold management.

Monitors spending patterns, triggers alerts when thresholds are reached,
and provides real-time spending notifications.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Callable
from enum import Enum
import logging

from ..budgets.budget_tracker import BudgetTracker, SpendingPeriod, BudgetStatus
from ..pricing.pricing_engine import PricingEngine

# Configure logging
logger = logging.getLogger(__name__)


class AlertLevel(str, Enum):
    """Alert severity levels."""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


class AlertType(str, Enum):
    """Types of spending alerts."""
    LOW_BALANCE = "low_balance"
    THRESHOLD_REACHED = "threshold_reached"
    DAILY_LIMIT = "daily_limit"
    MONTHLY_LIMIT = "monthly_limit"
    RATE_LIMIT = "rate_limit"
    ANOMALY = "anomaly"
    COST_SPIKE = "cost_spike"


@dataclass
class SpendingAlert:
    """Spending alert notification."""
    alert_id: str
    alert_type: AlertType
    level: AlertLevel
    user_id: str
    project_id: str
    
    title: str
    message: str
    current_value: float
    threshold_value: Optional[float] = None
    
    triggered_at: datetime = field(default_factory=datetime.utcnow)
    acknowledged: bool = False
    
    # Additional context
    metadata: Dict = field(default_factory=dict)
    
    def to_notification(self) -> Dict:
        """Convert to notification format."""
        return {
            "alert_id": self.alert_id,
            "type": self.alert_type.value,
            "level": self.level.value,
            "user_id": self.user_id,
            "project_id": self.project_id,
            "title": self.title,
            "message": self.message,
            "current_value": self.current_value,
            "threshold_value": self.threshold_value,
            "triggered_at": self.triggered_at.isoformat(),
            "metadata": self.metadata
        }


@dataclass
class SpendingThreshold:
    """Spending threshold configuration."""
    threshold_id: str
    user_id: str
    project_id: str
    
    threshold_type: str  # "balance", "daily", "monthly", "rate"
    threshold_value: float
    alert_level: AlertLevel
    
    # Notification settings
    notify_at_percent: List[float] = field(default_factory=lambda: [75.0, 90.0, 100.0])
    enabled: bool = True
    
    # Tracking
    last_triggered: Optional[datetime] = None
    trigger_count: int = 0


class SpendingMonitor:
    """
    Real-time spending monitor with alerts and thresholds.
    
    Monitors spending patterns, detects anomalies, and triggers alerts
    when thresholds are reached. Operates in READ-ONLY mode.
    """
    
    def __init__(self):
        """Initialize spending monitor."""
        self.budget_tracker = BudgetTracker()
        self.pricing_engine = PricingEngine()
        
        # Alert handlers (can be registered by external systems)
        self._alert_handlers: List[Callable[[SpendingAlert], None]] = []
        
        # Threshold cache
        self._thresholds: Dict[str, List[SpendingThreshold]] = {}
    
    def register_alert_handler(self, handler: Callable[[SpendingAlert], None]):
        """
        Register a callback for alert notifications.
        
        Args:
            handler: Function that receives SpendingAlert objects
        """
        self._alert_handlers.append(handler)
        logger.info(f"Registered alert handler: {handler.__name__}")
    
    async def check_spending_status(
        self, 
        user_id: str, 
        project_id: str
    ) -> List[SpendingAlert]:
        """
        Check current spending status and generate alerts if needed.
        
        Args:
            user_id: User identifier
            project_id: Project identifier
            
        Returns:
            List of triggered alerts
        """
        alerts = []
        
        try:
            # Get current budget status
            status = await self.budget_tracker.get_budget_status(user_id, project_id)
            
            # Check low balance
            if status.low_balance_warning:
                alert = SpendingAlert(
                    alert_id=f"alert_{user_id}_{int(datetime.utcnow().timestamp())}",
                    alert_type=AlertType.LOW_BALANCE,
                    level=AlertLevel.WARNING,
                    user_id=user_id,
                    project_id=project_id,
                    title="Low Balance Warning",
                    message=f"Available balance is low: ${status.available_balance:.2f} remaining",
                    current_value=status.available_balance,
                    threshold_value=status.total_balance * 0.2,
                    metadata={
                        "total_balance": status.total_balance,
                        "reserved_amount": status.reserved_amount,
                        "usage_percent": ((status.total_balance - status.available_balance) / status.total_balance * 100) if status.total_balance > 0 else 0
                    }
                )
                alerts.append(alert)
            
            # Check daily limit
            if status.daily_limit_reached:
                alert = SpendingAlert(
                    alert_id=f"alert_{user_id}_daily_{int(datetime.utcnow().timestamp())}",
                    alert_type=AlertType.DAILY_LIMIT,
                    level=AlertLevel.CRITICAL,
                    user_id=user_id,
                    project_id=project_id,
                    title="Daily Limit Reached",
                    message=f"Daily spending limit reached: ${status.spent_today:.2f} / ${status.daily_limit:.2f}",
                    current_value=status.spent_today,
                    threshold_value=status.daily_limit,
                    metadata={
                        "remaining_today": status.get_remaining_today()
                    }
                )
                alerts.append(alert)
            
            # Check monthly limit
            if status.monthly_limit_reached:
                alert = SpendingAlert(
                    alert_id=f"alert_{user_id}_monthly_{int(datetime.utcnow().timestamp())}",
                    alert_type=AlertType.MONTHLY_LIMIT,
                    level=AlertLevel.CRITICAL,
                    user_id=user_id,
                    project_id=project_id,
                    title="Monthly Limit Reached",
                    message=f"Monthly spending limit reached: ${status.spent_this_month:.2f} / ${status.monthly_limit:.2f}",
                    current_value=status.spent_this_month,
                    threshold_value=status.monthly_limit,
                    metadata={
                        "remaining_monthly": status.get_remaining_monthly()
                    }
                )
                alerts.append(alert)
            
            # Trigger alert handlers
            for alert in alerts:
                self._trigger_alert(alert)
            
            return alerts
            
        except Exception as e:
            logger.error(f"Failed to check spending status: {e}")
            return []
    
    async def check_threshold(
        self,
        user_id: str,
        project_id: str,
        threshold: SpendingThreshold
    ) -> Optional[SpendingAlert]:
        """
        Check if a specific threshold has been reached.
        
        Args:
            user_id: User identifier
            project_id: Project identifier
            threshold: Threshold to check
            
        Returns:
            SpendingAlert if threshold reached, None otherwise
        """
        if not threshold.enabled:
            return None
        
        try:
            status = await self.budget_tracker.get_budget_status(user_id, project_id)
            
            # Determine current value based on threshold type
            if threshold.threshold_type == "balance":
                current = status.total_balance - status.available_balance
                limit = status.total_balance
            elif threshold.threshold_type == "daily":
                current = status.spent_today
                limit = status.daily_limit or float('inf')
            elif threshold.threshold_type == "monthly":
                current = status.spent_this_month
                limit = status.monthly_limit or float('inf')
            else:
                return None
            
            # Check each notification percentage
            if limit > 0:
                percent_used = (current / limit) * 100
                
                for notify_percent in threshold.notify_at_percent:
                    if percent_used >= notify_percent:
                        alert = SpendingAlert(
                            alert_id=f"threshold_{threshold.threshold_id}_{int(datetime.utcnow().timestamp())}",
                            alert_type=AlertType.THRESHOLD_REACHED,
                            level=threshold.alert_level,
                            user_id=user_id,
                            project_id=project_id,
                            title=f"Spending Threshold Reached ({notify_percent}%)",
                            message=f"{threshold.threshold_type.title()} spending at {percent_used:.1f}% of limit: ${current:.2f} / ${limit:.2f}",
                            current_value=current,
                            threshold_value=limit,
                            metadata={
                                "threshold_id": threshold.threshold_id,
                                "threshold_type": threshold.threshold_type,
                                "percent_used": percent_used,
                                "notify_percent": notify_percent
                            }
                        )
                        
                        # Update threshold tracking
                        threshold.last_triggered = datetime.utcnow()
                        threshold.trigger_count += 1
                        
                        return alert
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to check threshold: {e}")
            return None
    
    async def detect_spending_anomaly(
        self,
        user_id: str,
        project_id: str,
        lookback_days: int = 7
    ) -> Optional[SpendingAlert]:
        """
        Detect unusual spending patterns.
        
        Args:
            user_id: User identifier
            project_id: Project identifier
            lookback_days: Number of days to analyze
            
        Returns:
            SpendingAlert if anomaly detected, None otherwise
        """
        try:
            # Get recent spending analytics
            analytics = await self.budget_tracker.get_spending_analytics(
                user_id=user_id,
                project_id=project_id,
                period=SpendingPeriod.DAILY
            )
            
            # Check for anomalies
            if analytics.anomaly_detected:
                alert = SpendingAlert(
                    alert_id=f"anomaly_{user_id}_{int(datetime.utcnow().timestamp())}",
                    alert_type=AlertType.ANOMALY,
                    level=AlertLevel.WARNING,
                    user_id=user_id,
                    project_id=project_id,
                    title="Spending Anomaly Detected",
                    message=analytics.anomaly_details or "Unusual spending pattern detected",
                    current_value=analytics.total_spent,
                    metadata={
                        "trend": analytics.spending_trend,
                        "request_count": analytics.request_count,
                        "average_per_request": analytics.average_per_request,
                        "period": analytics.period.value
                    }
                )
                
                self._trigger_alert(alert)
                return alert
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to detect anomaly: {e}")
            return None
    
    async def detect_cost_spike(
        self,
        user_id: str,
        project_id: str,
        spike_threshold_percent: float = 50.0
    ) -> Optional[SpendingAlert]:
        """
        Detect sudden cost spikes compared to baseline.
        
        Args:
            user_id: User identifier
            project_id: Project identifier
            spike_threshold_percent: Percentage increase to consider a spike
            
        Returns:
            SpendingAlert if spike detected, None otherwise
        """
        try:
            # Get current hour spending
            current_hour = await self.budget_tracker.get_spending_by_period(
                user_id=user_id,
                project_id=project_id,
                period=SpendingPeriod.HOURLY
            )
            
            # Get recent analytics for baseline
            analytics = await self.budget_tracker.get_spending_analytics(
                user_id=user_id,
                project_id=project_id,
                period=SpendingPeriod.HOURLY,
                start_date=datetime.utcnow() - timedelta(hours=24)
            )
            
            baseline = analytics.average_per_request * (analytics.request_count / 24)  # Avg per hour
            
            if baseline > 0:
                increase_percent = ((current_hour - baseline) / baseline) * 100
                
                if increase_percent > spike_threshold_percent:
                    alert = SpendingAlert(
                        alert_id=f"spike_{user_id}_{int(datetime.utcnow().timestamp())}",
                        alert_type=AlertType.COST_SPIKE,
                        level=AlertLevel.WARNING if increase_percent < 100 else AlertLevel.CRITICAL,
                        user_id=user_id,
                        project_id=project_id,
                        title="Cost Spike Detected",
                        message=f"Spending increased by {increase_percent:.1f}% this hour: ${current_hour:.2f} vs ${baseline:.2f} baseline",
                        current_value=current_hour,
                        threshold_value=baseline,
                        metadata={
                            "increase_percent": increase_percent,
                            "baseline": baseline,
                            "spike_threshold": spike_threshold_percent
                        }
                    )
                    
                    self._trigger_alert(alert)
                    return alert
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to detect cost spike: {e}")
            return None
    
    def _trigger_alert(self, alert: SpendingAlert):
        """
        Trigger all registered alert handlers.
        
        Args:
            alert: Alert to trigger
        """
        logger.warning(f"Alert triggered: {alert.title} - {alert.message}")
        
        for handler in self._alert_handlers:
            try:
                handler(alert)
            except Exception as e:
                logger.error(f"Alert handler failed: {e}")
    
    async def get_active_alerts(
        self,
        user_id: str,
        project_id: str,
        minutes: int = 60
    ) -> List[SpendingAlert]:
        """
        Get all alerts triggered in the last N minutes.
        
        This is a placeholder - in production, alerts would be stored in backend.
        
        Args:
            user_id: User identifier
            project_id: Project identifier
            minutes: Lookback window in minutes
            
        Returns:
            List of recent alerts
        """
        # In production, fetch from backend
        # For now, perform live checks
        return await self.check_spending_status(user_id, project_id)
