"""
API Request Models

Defines the structure of incoming API requests from users/agents.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, Optional, Any
import uuid
import requests
import logging

from ..config import config

logger = logging.getLogger(__name__)


class RequestStatus(Enum):
    """Status of an API request throughout its lifecycle"""
    PENDING = "pending"
    VALIDATING = "validating"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXECUTING = "executing"
    EXECUTED = "executed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class APIRequest:
    """
    Represents an API request from a user or agent.
    
    Example (Medical Store Chatbot):
        request = APIRequest(
            user_id="medical_store_001",
            project_id="chatbot_24_7",
            api_provider="openai",
            model_name="gpt-3.5-turbo",
            operation_type="chat",
            request_params={"prompt": "What are side effects of Ibuprofen?", "max_tokens": 150},
            estimated_cost=0.002
        )
    """
    
    # Identifiers
    user_id: str
    project_id: str
    request_id: str = field(default_factory=lambda: f"req_{uuid.uuid4().hex[:16]}")
    
    # Agent info (optional if request comes from user directly)
    agent_id: Optional[str] = None
    
    # API details (MUST be validated against user's whitelist)
    api_provider: str  # e.g., "openai", "anthropic", "google"
    model_name: str    # e.g., "gpt-4", "claude-3-opus", "gemini-pro"
    operation_type: str  # e.g., "chat", "vision", "code", "embedding"
    
    # Request parameters (passed to the API)
    request_params: Dict[str, Any] = field(default_factory=dict)
    
    # Cost information
    estimated_cost: float = 0.0  # USDC
    actual_cost: Optional[float] = None  # Set after execution
    
    # Metadata
    timestamp: datetime = field(default_factory=datetime.utcnow)
    status: RequestStatus = RequestStatus.PENDING
    
    # Validation flags (set during policy check)
    provider_whitelist_verified: bool = False
    model_whitelist_verified: bool = False
    
    # Additional context
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert request to dictionary for serialization"""
        return {
            "request_id": self.request_id,
            "user_id": self.user_id,
            "project_id": self.project_id,
            "agent_id": self.agent_id,
            "api_provider": self.api_provider,
            "model_name": self.model_name,
            "operation_type": self.operation_type,
            "request_params": self.request_params,
            "estimated_cost": self.estimated_cost,
            "actual_cost": self.actual_cost,
            "timestamp": self.timestamp.isoformat(),
            "status": self.status.value,
            "provider_whitelist_verified": self.provider_whitelist_verified,
            "model_whitelist_verified": self.model_whitelist_verified,
            "metadata": self.metadata,
        }
    
    def get_fingerprint(self) -> str:
        """
        Generate a unique fingerprint for this request.
        Used for deterministic decision-making and caching.
        """
        import hashlib
        
        components = [
            self.user_id,
            self.project_id,
            self.api_provider,
            self.model_name,
            self.operation_type,
            str(self.estimated_cost),
            str(sorted(self.request_params.items())),
        ]
        
        fingerprint_str = "|".join(components)
        return hashlib.sha256(fingerprint_str.encode()).hexdigest()[:16]
    
    def save_to_backend(self) -> str:
        """
        Save this request to backend.
        
        Returns:
            Request ID
        """
        try:
            url = config.get_endpoint('requests', 'create_request')
            response = requests.post(url, json=self.to_dict(), timeout=config.API_TIMEOUT)
            response.raise_for_status()
            request_id = response.json().get('request_id')
            logger.info(f"Saved request: {request_id}")
            return request_id
        except Exception as e:
            logger.error(f"Failed to save request to backend: {e}")
            raise
    
    @classmethod
    def fetch_from_backend(cls, request_id: str) -> Optional['APIRequest']:
        """
        Fetch request from backend.
        
        Args:
            request_id: Request identifier
            
        Returns:
            APIRequest object or None if not found
        """
        try:
            url = config.get_endpoint('requests', 'get_request', request_id=request_id)
            response = requests.get(url, timeout=config.API_TIMEOUT)
            response.raise_for_status()
            data = response.json()
            
            status = RequestStatus(data.get('status', 'pending'))
            
            return cls(
                request_id=data['request_id'],
                user_id=data['user_id'],
                project_id=data['project_id'],
                agent_id=data.get('agent_id'),
                api_provider=data['api_provider'],
                model_name=data['model_name'],
                operation_type=data['operation_type'],
                request_params=data.get('request_params', {}),
                estimated_cost=data.get('estimated_cost', 0.0),
                actual_cost=data.get('actual_cost'),
                status=status,
                provider_whitelist_verified=data.get('provider_whitelist_verified', False),
                model_whitelist_verified=data.get('model_whitelist_verified', False),
                metadata=data.get('metadata', {}),
            )
        except Exception as e:
            logger.error(f"Failed to fetch request from backend: {e}")
            return None

