"""
Pricing engine for cost estimation and token calculations.

Manages pricing data for AI providers, estimates request costs, converts tokens to costs,
and detects cost anomalies. This system is READ-ONLY - it fetches pricing data and
calculates costs but doesn't persist data.

Key responsibilities:
- Fetch current pricing for providers/models
- Estimate token usage for requests
- Calculate total cost including platform fees
- Compare estimated vs actual costs
- Detect cost anomalies
- Provide pricing history and trends
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional, Dict, List
from enum import Enum
import requests
import logging
import re

from ..config import Config
from ..models.cost import CostEstimate as CostEstimateModel, PricingData as PricingDataModel

# Configure logging
logger = logging.getLogger(__name__)


class PricingModel(str, Enum):
    """Pricing models for different providers."""
    TOKEN_BASED = "token_based"  # OpenAI, Anthropic
    CHAR_BASED = "char_based"    # Some providers charge per character
    REQUEST_BASED = "request_based"  # Flat per request
    TIME_BASED = "time_based"    # Per second of processing


@dataclass
class PricingData:
    """Pricing information for a provider/model."""
    provider: str
    model_name: str
    pricing_model: PricingModel
    
    # Token-based pricing
    input_price_per_1k: Optional[float] = None
    output_price_per_1k: Optional[float] = None
    
    # Alternative pricing
    price_per_request: Optional[float] = None
    price_per_char: Optional[float] = None
    price_per_second: Optional[float] = None
    
    # Metadata
    currency: str = "USD"
    effective_date: datetime = field(default_factory=datetime.utcnow)
    last_updated: datetime = field(default_factory=datetime.utcnow)
    
    # Context limits
    max_input_tokens: Optional[int] = None
    max_output_tokens: Optional[int] = None
    
    def calculate_cost(
        self, 
        input_tokens: int = 0, 
        output_tokens: int = 0,
        chars: int = 0,
        requests: int = 1,
        duration_seconds: float = 0.0
    ) -> float:
        """Calculate cost based on pricing model."""
        if self.pricing_model == PricingModel.TOKEN_BASED:
            input_cost = (input_tokens / 1000) * (self.input_price_per_1k or 0)
            output_cost = (output_tokens / 1000) * (self.output_price_per_1k or 0)
            return input_cost + output_cost
        
        elif self.pricing_model == PricingModel.CHAR_BASED:
            return chars * (self.price_per_char or 0)
        
        elif self.pricing_model == PricingModel.REQUEST_BASED:
            return requests * (self.price_per_request or 0)
        
        elif self.pricing_model == PricingModel.TIME_BASED:
            return duration_seconds * (self.price_per_second or 0)
        
        return 0.0


@dataclass
class TokenEstimate:
    """Token usage estimate for a request."""
    input_tokens: int
    output_tokens: int
    total_tokens: int
    estimation_method: str  # "tiktoken", "char_count", "api_estimate"
    confidence: float = 0.9  # 0.0 to 1.0
    
    def __post_init__(self):
        """Validate token counts."""
        self.total_tokens = self.input_tokens + self.output_tokens


@dataclass
class CostEstimate:
    """Cost estimate for an API request."""
    provider: str
    model_name: str
    
    # Token estimates
    estimated_input_tokens: int
    estimated_output_tokens: int
    estimated_total_tokens: int
    
    # Cost breakdown
    base_cost: float
    platform_fee: float
    total_cost: float
    
    # Metadata
    currency: str = "USD"
    confidence: float = 0.9
    estimated_at: datetime = field(default_factory=datetime.utcnow)
    
    # Pricing details
    pricing_data: Optional[PricingData] = None
    
    def to_usdc(self, exchange_rate: float = 1.0) -> float:
        """Convert total cost to USDC."""
        return self.total_cost * exchange_rate


@dataclass
class CostAnomaly:
    """Detected cost anomaly."""
    request_id: str
    provider: str
    model_name: str
    
    estimated_cost: float
    actual_cost: float
    difference: float
    difference_percent: float
    
    severity: str  # "low", "medium", "high", "critical"
    reason: str
    detected_at: datetime = field(default_factory=datetime.utcnow)
    
    def is_significant(self, threshold_percent: float = 20.0) -> bool:
        """Check if anomaly exceeds threshold."""
        return abs(self.difference_percent) > threshold_percent


class PricingEngine:
    """
    Pricing engine for cost estimation and analysis.
    
    This system operates in READ-ONLY mode:
    - Fetches pricing data from backend
    - Calculates cost estimates locally
    - Detects anomalies without persisting
    - Returns analysis without storing data
    """
    
    def __init__(self):
        """Initialize pricing engine."""
        self.config = Config()
        self.base_url = self.config.get_endpoint("pricing")
        self._pricing_cache: Dict[str, tuple[PricingData, datetime]] = {}
        self._cache_ttl = 300  # Cache pricing for 5 minutes
        
        # Platform fee (configurable)
        self.platform_fee_percent = 0.05  # 5% platform fee
    
    async def get_provider_pricing(
        self, 
        provider: str, 
        model: str,
        use_cache: bool = True
    ) -> PricingData:
        """
        Get current pricing for provider/model from backend.
        
        Args:
            provider: Provider name (e.g., "openai", "anthropic")
            model: Model name (e.g., "gpt-4", "claude-3-opus")
            use_cache: Whether to use cached pricing
            
        Returns:
            PricingData for the provider/model
        """
        cache_key = f"{provider}:{model}"
        
        # Check cache
        if use_cache and cache_key in self._pricing_cache:
            cached_pricing, cached_at = self._pricing_cache[cache_key]
            if (datetime.utcnow() - cached_at).seconds < self._cache_ttl:
                logger.debug(f"Using cached pricing for {cache_key}")
                return cached_pricing
        
        try:
            url = f"{self.base_url}/provider/{provider}/model/{model}"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            
            pricing = PricingData(
                provider=provider,
                model_name=model,
                pricing_model=PricingModel(data.get("pricing_model", "token_based")),
                input_price_per_1k=data.get("input_price_per_1k"),
                output_price_per_1k=data.get("output_price_per_1k"),
                price_per_request=data.get("price_per_request"),
                price_per_char=data.get("price_per_char"),
                price_per_second=data.get("price_per_second"),
                max_input_tokens=data.get("max_input_tokens"),
                max_output_tokens=data.get("max_output_tokens"),
                effective_date=datetime.fromisoformat(data.get("effective_date", datetime.utcnow().isoformat())),
                last_updated=datetime.fromisoformat(data.get("last_updated", datetime.utcnow().isoformat()))
            )
            
            # Update cache
            self._pricing_cache[cache_key] = (pricing, datetime.utcnow())
            
            logger.info(f"Fetched pricing for {provider}/{model}")
            return pricing
            
        except requests.RequestException as e:
            logger.error(f"Failed to fetch pricing: {e}")
            raise
    
    async def estimate_tokens(
        self, 
        text: str, 
        model: str,
        is_input: bool = True
    ) -> TokenEstimate:
        """
        Estimate token count for text.
        
        Args:
            text: Text to estimate tokens for
            model: Model name for tokenization
            is_input: Whether this is input (True) or output (False)
            
        Returns:
            TokenEstimate with token count
        """
        # Simple estimation: ~4 chars per token (rough average)
        # In production, use tiktoken or provider-specific tokenizers
        
        char_count = len(text)
        estimated_tokens = int(char_count / 4)
        
        # Add some buffer for special tokens
        estimated_tokens = int(estimated_tokens * 1.1)
        
        if is_input:
            return TokenEstimate(
                input_tokens=estimated_tokens,
                output_tokens=0,
                total_tokens=estimated_tokens,
                estimation_method="char_count",
                confidence=0.8
            )
        else:
            return TokenEstimate(
                input_tokens=0,
                output_tokens=estimated_tokens,
                total_tokens=estimated_tokens,
                estimation_method="char_count",
                confidence=0.8
            )
    
    async def estimate_cost(
        self, 
        provider: str,
        model: str,
        input_text: Optional[str] = None,
        expected_output_tokens: Optional[int] = None,
        input_tokens: Optional[int] = None,
        output_tokens: Optional[int] = None
    ) -> CostEstimate:
        """
        Estimate cost for an API request.
        
        Args:
            provider: Provider name
            model: Model name
            input_text: Input text (if known)
            expected_output_tokens: Expected output token count
            input_tokens: Pre-calculated input tokens
            output_tokens: Pre-calculated output tokens
            
        Returns:
            CostEstimate with breakdown
        """
        try:
            # Get pricing data
            pricing = await self.get_provider_pricing(provider, model)
            
            # Estimate tokens if not provided
            if input_tokens is None and input_text:
                token_est = await self.estimate_tokens(input_text, model, is_input=True)
                input_tokens = token_est.input_tokens
            elif input_tokens is None:
                input_tokens = 0
            
            if output_tokens is None:
                # Use expected or default estimate
                output_tokens = expected_output_tokens or int(input_tokens * 0.5)  # Assume 50% of input
            
            # Calculate base cost
            base_cost = pricing.calculate_cost(
                input_tokens=input_tokens,
                output_tokens=output_tokens
            )
            
            # Calculate platform fee
            platform_fee = base_cost * self.platform_fee_percent
            
            # Total cost
            total_cost = base_cost + platform_fee
            
            estimate = CostEstimate(
                provider=provider,
                model_name=model,
                estimated_input_tokens=input_tokens,
                estimated_output_tokens=output_tokens,
                estimated_total_tokens=input_tokens + output_tokens,
                base_cost=base_cost,
                platform_fee=platform_fee,
                total_cost=total_cost,
                pricing_data=pricing
            )
            
            logger.info(f"Cost estimate for {provider}/{model}: ${total_cost:.6f} ({input_tokens} + {output_tokens} tokens)")
            return estimate
            
        except Exception as e:
            logger.error(f"Cost estimation failed: {e}")
            raise
    
    async def calculate_total_cost(
        self,
        base_cost: float,
        platform_fee_percent: Optional[float] = None
    ) -> float:
        """
        Calculate total cost including platform fee.
        
        Args:
            base_cost: Base API cost
            platform_fee_percent: Optional custom platform fee (uses default if None)
            
        Returns:
            Total cost with fee
        """
        fee_percent = platform_fee_percent or self.platform_fee_percent
        platform_fee = base_cost * fee_percent
        return base_cost + platform_fee
    
    async def detect_cost_anomaly(
        self,
        request_id: str,
        provider: str,
        model: str,
        estimated_cost: float,
        actual_cost: float,
        threshold_percent: float = 20.0
    ) -> Optional[CostAnomaly]:
        """
        Detect if actual cost significantly differs from estimate.
        
        Args:
            request_id: Request identifier
            provider: Provider name
            model: Model name
            estimated_cost: Estimated cost
            actual_cost: Actual cost
            threshold_percent: Threshold for anomaly detection
            
        Returns:
            CostAnomaly if detected, None otherwise
        """
        difference = actual_cost - estimated_cost
        
        if estimated_cost > 0:
            difference_percent = (difference / estimated_cost) * 100
        else:
            difference_percent = 100.0 if actual_cost > 0 else 0.0
        
        # Determine severity
        abs_diff = abs(difference_percent)
        if abs_diff < threshold_percent:
            return None  # Not an anomaly
        
        if abs_diff < 50:
            severity = "low"
            reason = f"Cost differs by {abs_diff:.1f}%"
        elif abs_diff < 100:
            severity = "medium"
            reason = f"Cost differs by {abs_diff:.1f}%, investigate pricing changes"
        elif abs_diff < 200:
            severity = "high"
            reason = f"Cost differs by {abs_diff:.1f}%, possible pricing error or usage spike"
        else:
            severity = "critical"
            reason = f"Cost differs by {abs_diff:.1f}%, likely estimation failure or fraud"
        
        anomaly = CostAnomaly(
            request_id=request_id,
            provider=provider,
            model_name=model,
            estimated_cost=estimated_cost,
            actual_cost=actual_cost,
            difference=difference,
            difference_percent=difference_percent,
            severity=severity,
            reason=reason
        )
        
        logger.warning(f"Cost anomaly detected: {anomaly.reason}")
        return anomaly
    
    async def get_price_history(
        self,
        provider: str,
        model: str,
        days: int = 30
    ) -> List[PricingDataModel]:
        """
        Get pricing history for provider/model.
        
        Args:
            provider: Provider name
            model: Model name
            days: Number of days of history
            
        Returns:
            List of historical pricing data
        """
        try:
            url = f"{self.base_url}/provider/{provider}/model/{model}/history"
            params = {"days": days}
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            history = []
            
            for item in data.get("pricing_history", []):
                pricing = PricingDataModel(
                    provider=provider,
                    model_name=model,
                    input_cost_per_token=item.get("input_price_per_1k", 0) / 1000,
                    output_cost_per_token=item.get("output_price_per_1k", 0) / 1000,
                    last_updated=datetime.fromisoformat(item.get("effective_date")),
                    currency=item.get("currency", "USD")
                )
                history.append(pricing)
            
            logger.info(f"Fetched {len(history)} pricing records for {provider}/{model}")
            return history
            
        except requests.RequestException as e:
            logger.error(f"Failed to fetch price history: {e}")
            return []
    
    async def compare_provider_costs(
        self,
        providers: List[tuple[str, str]],  # List of (provider, model) tuples
        input_tokens: int,
        output_tokens: int
    ) -> Dict[str, CostEstimate]:
        """
        Compare costs across multiple providers/models.
        
        Args:
            providers: List of (provider, model) tuples to compare
            input_tokens: Input token count
            output_tokens: Output token count
            
        Returns:
            Dictionary mapping "provider/model" to CostEstimate
        """
        estimates = {}
        
        for provider, model in providers:
            try:
                estimate = await self.estimate_cost(
                    provider=provider,
                    model=model,
                    input_tokens=input_tokens,
                    output_tokens=output_tokens
                )
                key = f"{provider}/{model}"
                estimates[key] = estimate
                
            except Exception as e:
                logger.warning(f"Failed to estimate cost for {provider}/{model}: {e}")
                continue
        
        # Sort by total cost
        sorted_estimates = dict(sorted(estimates.items(), key=lambda x: x[1].total_cost))
        
        logger.info(f"Compared {len(sorted_estimates)} provider/model combinations")
        return sorted_estimates
    
    def clear_cache(self, provider: Optional[str] = None, model: Optional[str] = None):
        """
        Clear pricing cache.
        
        Args:
            provider: Optional provider to clear (clears all if None)
            model: Optional model to clear (clears provider if None)
        """
        if provider and model:
            cache_key = f"{provider}:{model}"
            self._pricing_cache.pop(cache_key, None)
            logger.debug(f"Cleared pricing cache for {cache_key}")
        elif provider:
            # Clear all entries for this provider
            keys_to_remove = [k for k in self._pricing_cache.keys() if k.startswith(f"{provider}:")]
            for key in keys_to_remove:
                self._pricing_cache.pop(key)
            logger.debug(f"Cleared pricing cache for provider {provider}")
        else:
            # Clear entire cache
            self._pricing_cache.clear()
            logger.debug("Cleared entire pricing cache")
