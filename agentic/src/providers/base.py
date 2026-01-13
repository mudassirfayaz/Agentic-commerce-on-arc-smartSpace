"""
Base provider adapter interface.

Defines the common interface that all provider adapters must implement.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from datetime import datetime


@dataclass
class ProviderResponse:
    """Standardized response from any provider."""
    
    # Status
    success: bool
    status_code: int = 200
    
    # Response data
    data: Dict[str, Any] = field(default_factory=dict)
    raw_response: Optional[Dict[str, Any]] = None
    
    # Usage metrics
    tokens_used: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    
    # Cost (calculated)
    cost: float = 0.0
    
    # Timing
    latency_ms: float = 0.0
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    # Error info
    error: Optional[str] = None
    error_type: Optional[str] = None
    
    # Metadata
    provider: str = ""
    model: str = ""
    request_id: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "success": self.success,
            "status_code": self.status_code,
            "data": self.data,
            "tokens_used": self.tokens_used,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "cost": self.cost,
            "latency_ms": self.latency_ms,
            "timestamp": self.timestamp.isoformat(),
            "error": self.error,
            "error_type": self.error_type,
            "provider": self.provider,
            "model": self.model,
            "request_id": self.request_id,
        }


class ProviderAdapter(ABC):
    """
    Base class for provider adapters.
    
    All provider-specific adapters must implement this interface
    to ensure consistent behavior across different providers.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize adapter.
        
        Args:
            api_key: Optional API key (can be None if using backend gateway)
        """
        self.api_key = api_key
        self.provider_name = "base"
    
    @abstractmethod
    async def call_api(
        self,
        endpoint: str,
        model: str,
        parameters: Dict[str, Any],
        timeout: int = 30
    ) -> ProviderResponse:
        """
        Call the provider API.
        
        Args:
            endpoint: API endpoint to call
            model: Model name to use
            parameters: Request parameters
            timeout: Request timeout in seconds
            
        Returns:
            ProviderResponse with standardized data
        """
        pass
    
    @abstractmethod
    def estimate_cost(
        self,
        model: str,
        input_tokens: int,
        output_tokens: int
    ) -> float:
        """
        Estimate cost for a request.
        
        Args:
            model: Model name
            input_tokens: Estimated input tokens
            output_tokens: Estimated output tokens
            
        Returns:
            Estimated cost in USD
        """
        pass
    
    @abstractmethod
    def parse_response(
        self,
        raw_response: Dict[str, Any]
    ) -> ProviderResponse:
        """
        Parse provider-specific response into standardized format.
        
        Args:
            raw_response: Raw response from provider
            
        Returns:
            Standardized ProviderResponse
        """
        pass
    
    def get_provider_name(self) -> str:
        """Get provider name."""
        return self.provider_name
