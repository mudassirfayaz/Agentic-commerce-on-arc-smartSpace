"""
OpenAI API adapter.

Handles API calls to OpenAI (GPT-4, GPT-3.5, etc.).
"""

import time
import logging
from typing import Dict, Any, Optional
import requests

from .base import ProviderAdapter, ProviderResponse

logger = logging.getLogger(__name__)


class OpenAIAdapter(ProviderAdapter):
    """Adapter for OpenAI API."""
    
    # Pricing per 1M tokens (as of 2026)
    PRICING = {
        "gpt-4": {"input": 30.0, "output": 60.0},
        "gpt-4-turbo": {"input": 10.0, "output": 30.0},
        "gpt-3.5-turbo": {"input": 0.5, "output": 1.5},
        "gpt-4o": {"input": 5.0, "output": 15.0},
        "gpt-4o-mini": {"input": 0.15, "output": 0.6},
    }
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize OpenAI adapter."""
        super().__init__(api_key)
        self.provider_name = "openai"
        self.base_url = "https://api.openai.com/v1"
    
    async def call_api(
        self,
        endpoint: str,
        model: str,
        parameters: Dict[str, Any],
        timeout: int = 30
    ) -> ProviderResponse:
        """
        Call OpenAI API.
        
        Args:
            endpoint: API endpoint (e.g., "/chat/completions")
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
                "Authorization": f"Bearer {self.api_key}",
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
            logger.error(f"OpenAI API call failed: {e}")
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
        """Parse OpenAI response."""
        usage = raw_response.get('usage', {})
        input_tokens = usage.get('prompt_tokens', 0)
        output_tokens = usage.get('completion_tokens', 0)
        total_tokens = usage.get('total_tokens', input_tokens + output_tokens)
        
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
        """Estimate cost for OpenAI request."""
        # Get pricing for model (default to gpt-4 pricing if unknown)
        pricing = self.PRICING.get(model, self.PRICING['gpt-4'])
        
        # Calculate cost (pricing is per 1M tokens)
        input_cost = (input_tokens / 1_000_000) * pricing['input']
        output_cost = (output_tokens / 1_000_000) * pricing['output']
        
        return input_cost + output_cost
