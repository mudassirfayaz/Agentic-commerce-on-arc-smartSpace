"""Payment model - SQLAlchemy ORM."""

from sqlalchemy import Column, String, Float, Integer, DateTime, Enum
from sqlalchemy.sql import func
import enum
from src.database.base import Base


class PaymentStatus(str, enum.Enum):
    """Payment status enum."""
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Payment(Base):
    """Payment model."""
    __tablename__ = "payments"
    
    payment_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, nullable=False, index=True)
    request_id = Column(String, nullable=False, index=True)
    amount = Column(Float, nullable=False)
    currency = Column(String, default="USDC")
    network = Column(String, default="arc")
    tx_hash = Column(String, nullable=True, index=True)
    block_number = Column(Integer, nullable=True)
    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "payment_id": self.payment_id,
            "user_id": self.user_id,
            "request_id": self.request_id,
            "amount": self.amount,
            "currency": self.currency,
            "network": self.network,
            "tx_hash": self.tx_hash,
            "block_number": self.block_number,
            "status": self.status.value if self.status else None,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
