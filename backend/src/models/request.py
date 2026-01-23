"""Request model - SQLAlchemy ORM."""

from sqlalchemy import Column, String, Float, DateTime, JSON, Enum
from sqlalchemy.sql import func
import enum
from src.database.base import Base


class RequestStatus(str, enum.Enum):
    """Request status enum."""
    PENDING = "pending"
    VALIDATING = "validating"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXECUTING = "executing"
    EXECUTED = "executed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class APIRequest(Base):
    """API request model."""
    __tablename__ = "requests"
    
    request_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, nullable=False, index=True)
    project_id = Column(String, nullable=False, index=True)
    agent_id = Column(String, nullable=True, index=True)
    api_provider = Column(String, nullable=False)
    model_name = Column(String, nullable=False)
    endpoint = Column(String, nullable=False)
    parameters = Column(JSON, default=dict)
    status = Column(Enum(RequestStatus), default=RequestStatus.PENDING)
    estimated_cost = Column(Float, default=0.0)
    actual_cost = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "request_id": self.request_id,
            "user_id": self.user_id,
            "project_id": self.project_id,
            "agent_id": self.agent_id,
            "api_provider": self.api_provider,
            "model_name": self.model_name,
            "endpoint": self.endpoint,
            "parameters": self.parameters or {},
            "status": self.status.value if self.status else None,
            "estimated_cost": self.estimated_cost,
            "actual_cost": self.actual_cost,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
