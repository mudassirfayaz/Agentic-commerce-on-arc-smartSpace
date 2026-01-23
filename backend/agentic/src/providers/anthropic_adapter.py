"""
Anthropic API adapter.

Handles API calls to Anthropic (Claude models).
"""

import time
import logging
from typing import Dict, Any, Optional
import requests

from .base import ProviderAdapter, ProviderResponse

logger = logging.getLogger(__name__)


class AnthropicAdapter(ProviderAdapter):
    """Adapter for Anthropic API."""
    
    # Pricing per 1M tokens (as of 2026)
    PRICING = {
        "claude-3-opus": {"input": 15.0, "output": 75.0},
        "claude-3-sonnet": {"input": 3.0, "output": 15.0},
        "claude-3-haiku": {"input": 0.25, "output": 1.25},
        "claude-3.5-sonnet": {"input": 3.0, "output": 15.0},
    }
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize Anthropic adapter."""
        super().__init__(api_key)
        self.provider_name = "anthropic"
        self.base_url = "https://api.anthropic.com/v1"
        self.api_version = "2023-06-01"
    
    async def call_api(
        self,
        endpoint: str,
        model: str,
        parameters: Dict[str, Any],
        timeout: int = 30
    ) -> ProviderResponse:
        """
        Call Anthropic API.
        
        Args:
            endpoint: API endpoint (e.g., "/messages")
            model: Model name
            parameters: Request parameters
            timeout: Request timeout
            
        Returns:
            ProviderResponse with results
        """
        start_time = time.time()
        
        try:
            # Build request
            url = f"{self.base_url}{endpoint}"
            headers = {
                "x-api-key": self.api_key,
                "anthropic-version": self.api_version,
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": model,
                **parameters
            }
            
            # Make request
            response = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=timeout
            )
            
            latency_ms = (time.time() - start_time) * 1000
            
            # Parse response
            if response.status_code == 200:
                result = self.parse_response(response.json())
                result.latency_ms = latency_ms
                result.provider = self.provider_name
                result.model = model
                return result
            else:
                # Error response
                error_data = response.json() if response.text else {}
                return ProviderResponse(
                    success=False,
                    status_code=response.status_code,
                    error=error_data.get('error', {}).get('message', 'Unknown error'),
                    error_type=error_data.get('error', {}).get('type', 'api_error'),
                    latency_ms=latency_ms,
                    provider=self.provider_name,
                    model=model
                )
                
        except requests.exceptions.Timeout:
            return ProviderResponse(
                success=False,
                status_code=408,
                error="Request timeout",
                error_type="timeout",
                latency_ms=(time.time() - start_time) * 1000,
                provider=self.provider_name,
                model=model
            )
        except Exception as e:
            logger.error(f"Anthropic API call failed: {e}")
            return ProviderResponse(
                success=False,
                status_code=500,
                error=str(e),
                error_type="internal_error",
                latency_ms=(time.time() - start_time) * 1000,
                provider=self.provider_name,
                model=model
            )
    
    def parse_response(
        self,
        raw_response: Dict[str, Any]
    ) -> ProviderResponse:
        """Parse Anthropic response."""
        usage = raw_response.get('usage', {})
        input_tokens = usage.get('input_tokens', 0)
        output_tokens = usage.get('output_tokens', 0)
        total_tokens = input_tokens + output_tokens
        
        # Calculate cost
        cost = self.estimate_cost(
            raw_response.get('model', ''),
            input_tokens,
            output_tokens
        )
        
        return ProviderResponse(
            success=True,
            status_code=200,
            data=raw_response,
            raw_response=raw_response,
            tokens_used=total_tokens,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost=cost,
            provider=self.provider_name,
            model=raw_response.get('model', ''),
            request_id=raw_response.get('id')
        )
    
    def estimate_cost(
        self,
        model: str,
        input_tokens: int,
        output_tokens: int
    ) -> float:
        """Estimate cost for Anthropic request."""
        # Get pricing for model (default to opus pricing if unknown)
        pricing = self.PRICING.get(model, self.PRICING['claude-3-opus'])
        
        # Calculate cost (pricing is per 1M tokens)
        input_cost = (input_tokens / 1_000_000) * pricing['input']
        output_cost = (output_tokens / 1_000_000) * pricing['output']
        
        return input_cost + output_cost
