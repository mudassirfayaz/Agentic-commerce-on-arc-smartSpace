"""User model - SQLAlchemy ORM."""

from sqlalchemy import Column, String, Float, Integer, DateTime, Enum
from sqlalchemy.sql import func
from datetime import datetime
import enum
from src.database.base import Base


class AccountStatus(str, enum.Enum):
    """Account status enum."""
    ACTIVE = "active"
    SUSPENDED = "suspended"
    INACTIVE = "inactive"


class UserTier(str, enum.Enum):
    """User tier enum."""
    FREE = "free"
    PRO = "pro"
    ENTERPRISE = "enterprise"


class User(Base):
    """User model."""
    __tablename__ = "users"
    
    user_id = Column(String, primary_key=True, index=True)
    account_status = Column(Enum(AccountStatus), default=AccountStatus.ACTIVE)
    tier = Column(Enum(UserTier), default=UserTier.FREE)
    total_spending = Column(Float, default=0.0)
    available_balance = Column(Float, default=0.0)
    total_requests = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_request_at = Column(DateTime(timezone=True), nullable=True)
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "user_id": self.user_id,
            "account_status": self.account_status.value if self.account_status else None,
            "tier": self.tier.value if self.tier else None,
            "total_spending": self.total_spending,
            "available_balance": self.available_balance,
            "total_requests": self.total_requests,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_request_at": self.last_request_at.isoformat() if self.last_request_at else None
        }
