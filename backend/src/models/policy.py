"""Policy model - SQLAlchemy ORM."""

from sqlalchemy import Column, String, JSON, Float, ForeignKey
from sqlalchemy.orm import relationship
from src.database.base import Base


class Policy(Base):
    """Policy model."""
    __tablename__ = "policies"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False, index=True)
    project_id = Column(String, nullable=False, index=True)
    allowed_providers = Column(JSON, default=list)
    allowed_models = Column(JSON, default=dict)
    rate_limits = Column(JSON, default=dict)
    forbidden_operations = Column(JSON, default=list)
    require_approval_above = Column(Float, nullable=True)
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "allowed_providers": self.allowed_providers or [],
            "allowed_models": self.allowed_models or {},
            "rate_limits": self.rate_limits or {},
            "forbidden_operations": self.forbidden_operations or [],
            "require_approval_above": self.require_approval_above
        }
