"""
Cost Estimation Models

Defines cost estimation and pricing structures.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Optional, Any
import logging

import requests

from config import config

logger = logging.getLogger(__name__)


@dataclass
class PricingData:
    """
    Pricing information for a specific provider/model.
    
    Example (OpenAI GPT-4):
        pricing = PricingData(
            provider="openai",
            model="gpt-4",
            input_price_per_1k_tokens=0.03,
            output_price_per_1k_tokens=0.06,
            currency="USD"
        )
    """
    
    provider: str
    model: str
    
    # Token-based pricing
    input_price_per_1k_tokens: float = 0.0
    output_price_per_1k_tokens: float = 0.0
    
    # Alternative pricing models
    price_per_request: Optional[float] = None  # Flat fee per request
    price_per_image: Optional[float] = None  # For vision models
    price_per_minute: Optional[float] = None  # For audio/video
    
    # Currency
    currency: str = "USD"
    
    # Metadata
    last_updated: datetime = field(default_factory=datetime.utcnow)
    source: str = "provider_api"  # Where pricing data came from
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "provider": self.provider,
            "model": self.model,
            "input_price_per_1k_tokens": self.input_price_per_1k_tokens,
            "output_price_per_1k_tokens": self.output_price_per_1k_tokens,
            "price_per_request": self.price_per_request,
            "price_per_image": self.price_per_image,
            "price_per_minute": self.price_per_minute,
            "currency": self.currency,
            "last_updated": self.last_updated.isoformat(),
            "source": self.source,
        }
    
    @classmethod
    def fetch_from_backend(cls, provider: str, model: str) -> Optional['PricingData']:
        """
        Fetch pricing data from backend API.
        
        Args:
            provider: Provider name
            model: Model name
            
        Returns:
            PricingData object or None if not found
        """
        try:
            url = config.get_endpoint('costs', 'get_pricing', provider=provider, model=model)
            response = requests.get(url, timeout=config.API_TIMEOUT)
            response.raise_for_status()
            data = response.json()
            
            return cls(
                provider=data['provider'],
                model=data['model'],
                input_price_per_1k_tokens=data.get('input_price_per_1k_tokens', 0.0),
                output_price_per_1k_tokens=data.get('output_price_per_1k_tokens', 0.0),
                price_per_request=data.get('price_per_request'),
                price_per_image=data.get('price_per_image'),
                price_per_minute=data.get('price_per_minute'),
                currency=data.get('currency', 'USD'),
                source=data.get('source', 'provider_api'),
            )
        except Exception as e:
            logger.warning(f"Failed to fetch pricing for {provider}/{model}: {e}")
            return None


@dataclass
class CostEstimate:
    """
    Cost estimate for an API request.
    """
    
    # Identifiers
    request_id: str
    provider: str
    model: str
    
    # Token estimates
    estimated_input_tokens: int = 0
    estimated_output_tokens: int = 0
    total_estimated_tokens: int = 0

    # Costs
    base_cost: float = 0.0
    platform_fee: float = 0.0
    total: float = 0.0
    
    # Associated Data
    pricing_data: Optional[PricingData] = None
    
    # Confidence
    confidence: float = 0.85  # How confident we are in estimate (0-1)
    
    # Timestamp
    estimated_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        """Calculate total tokens"""
        self.total_estimated_tokens = self.estimated_input_tokens + self.estimated_output_tokens
        if self.total == 0.0:
            self.total = self.base_cost + self.platform_fee
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "request_id": self.request_id,
            "provider": self.provider,
            "model": self.model,
            "estimated_input_tokens": self.estimated_input_tokens,
            "estimated_output_tokens": self.estimated_output_tokens,
            "total_estimated_tokens": self.total_estimated_tokens,
            "base_cost": self.base_cost,
            "platform_fee": self.platform_fee,
            "total": self.total,
            "pricing_data": self.pricing_data.to_dict() if self.pricing_data else None,
            "confidence": self.confidence,
            "estimated_at": self.estimated_at.isoformat(),
        }

    @classmethod
    def estimate_from_backend(cls, request_id: str, provider: str, model: str, 
                             estimated_input_tokens: int, estimated_output_tokens: int) -> 'CostEstimate':
        """
        Get cost estimate from backend API.
        
        Args:
            request_id: Request identifier
            provider: Provider name
            model: Model name
            estimated_input_tokens: Estimated input tokens
            estimated_output_tokens: Estimated output tokens
            
        Returns:
            CostEstimate object
        """
        try:
            url = config.get_endpoint('costs', 'estimate_cost')
            data = {
                'request_id': request_id,
                'provider': provider,
                'model': model,
                'estimated_input_tokens': estimated_input_tokens,
                'estimated_output_tokens': estimated_output_tokens
            }
            response = requests.post(url, json=data, timeout=config.API_TIMEOUT)
            response.raise_for_status()
            result = response.json()
            
            pricing = None
            if 'pricing_data' in result:
                pricing = PricingData(
                    provider=result['pricing_data']['provider'],
                    model=result['pricing_data']['model'],
                    input_price_per_1k_tokens=result['pricing_data'].get('input_price_per_1k_tokens', 0.0),
                    output_price_per_1k_tokens=result['pricing_data'].get('output_price_per_1k_tokens', 0.0),
                    currency=result['pricing_data'].get('currency', 'USD'),
                )
            
            return cls(
                request_id=request_id,
                provider=provider,
                model=model,
                estimated_input_tokens=estimated_input_tokens,
                estimated_output_tokens=estimated_output_tokens,
                base_cost=result.get('base_cost', 0.0),
                platform_fee=result.get('platform_fee', 0.0),
                total=result.get('total', 0.0),
                pricing_data=pricing,
                confidence=result.get('confidence', 0.85),
            )
        except Exception as e:
            logger.error(f"Failed to estimate cost from backend: {e}")
            raise


@dataclass
class CostComparison:
    """
    Comparison of costs between different providers/models.
    
    Used for cost optimization and provider selection.
    """
    
    request_id: str
    
    # Original request
    original_provider: str
    original_model: str
    original_cost: float
    
    # Alternatives
    alternatives: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    
    # Best alternative
    recommended_provider: Optional[str] = None
    recommended_model: Optional[str] = None
    recommended_cost: Optional[float] = None
    savings: Optional[float] = None
    
    # Timestamp
    compared_at: datetime = field(default_factory=datetime.utcnow)
    
    def add_alternative(
        self,
        provider: str,
        model: str,
        cost: float,
        quality_score: float = 1.0,
        available: bool = True
    ) -> None:
        """Add an alternative provider/model option"""
        key = f"{provider}/{model}"
        self.alternatives[key] = {
            "provider": provider,
            "model": model,
            "cost": cost,
            "quality_score": quality_score,
            "available": available,
            "savings": self.original_cost - cost,
            "savings_percentage": ((self.original_cost - cost) / self.original_cost * 100) if self.original_cost > 0 else 0,
        }
    
    def find_best_alternative(self, min_quality_score: float = 0.8) -> Optional[Dict[str, Any]]:
        """
        Find the best alternative based on cost and quality.
        Returns the cheapest option that meets minimum quality threshold.
        """
        viable_alternatives = [
            alt for alt in self.alternatives.values()
            if alt["available"] and alt["quality_score"] >= min_quality_score
        ]
        
        if not viable_alternatives:
            return None
        
        # Sort by cost (cheapest first)
        viable_alternatives.sort(key=lambda x: x["cost"])
        
        best = viable_alternatives[0]
        self.recommended_provider = best["provider"]
        self.recommended_model = best["model"]
        self.recommended_cost = best["cost"]
        self.savings = best["savings"]
        
        return best
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "request_id": self.request_id,
            "original_provider": self.original_provider,
            "original_model": self.original_model,
            "original_cost": self.original_cost,
            "alternatives": self.alternatives,
            "recommended_provider": self.recommended_provider,
            "recommended_model": self.recommended_model,
            "recommended_cost": self.recommended_cost,
            "savings": self.savings,
            "compared_at": self.compared_at.isoformat(),
        }