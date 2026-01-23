"""Budget model - SQLAlchemy ORM."""

from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from datetime import datetime
from src.database.base import Base


class Budget(Base):
    """Budget model."""
    __tablename__ = "budgets"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False, index=True)
    project_id = Column(String, nullable=False, index=True)
    daily_limit = Column(Float, default=100.0)
    monthly_limit = Column(Float, default=1000.0)
    per_request_limit = Column(Float, default=10.0)
    current_daily_spending = Column(Float, default=0.0)
    current_monthly_spending = Column(Float, default=0.0)
    period_start = Column(DateTime(timezone=True), server_default=func.now())
    period_end = Column(DateTime(timezone=True), nullable=True)
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "daily_limit": self.daily_limit,
            "monthly_limit": self.monthly_limit,
            "per_request_limit": self.per_request_limit,
            "current_daily_spending": self.current_daily_spending,
            "current_monthly_spending": self.current_monthly_spending,
            "period_start": self.period_start.isoformat() if self.period_start else None,
            "period_end": self.period_end.isoformat() if self.period_end else None
        }
