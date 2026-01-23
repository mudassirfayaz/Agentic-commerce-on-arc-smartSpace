"""API Key model - SQLAlchemy ORM."""

from sqlalchemy import Column, String, Integer, DateTime, Enum, ForeignKey, Index
from sqlalchemy.sql import func
from datetime import datetime
import enum
from src.database.base import Base


class ApiKeyStatus(str, enum.Enum):
    """API key status enum."""
    ACTIVE = "active"
    REVOKED = "revoked"


class ApiKey(Base):
    """API Key model."""
    __tablename__ = "api_keys"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False, index=True)
    key_hash = Column(String, nullable=False, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    last_used_at = Column(DateTime(timezone=True), nullable=True)
    usage_count = Column(Integer, default=0, nullable=False)
    status = Column(Enum(ApiKeyStatus), default=ApiKeyStatus.ACTIVE, nullable=False)
    
    # Create indexes for fast lookup
    __table_args__ = (
        Index('idx_api_keys_key_hash', 'key_hash'),
        Index('idx_api_keys_user_id', 'user_id'),
    )
    
    def to_dict(self) -> dict:
        """Convert to dictionary (without key_hash for security)."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_used_at": self.last_used_at.isoformat() if self.last_used_at else None,
            "usage_count": self.usage_count,
            "status": self.status.value if self.status else None
        }
    
    def is_active(self) -> bool:
        """Check if API key is active."""
        return self.status == ApiKeyStatus.ACTIVE
    
    def is_revoked(self) -> bool:
        """Check if API key is revoked."""
        return self.status == ApiKeyStatus.REVOKED

