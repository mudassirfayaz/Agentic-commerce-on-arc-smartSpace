"""
Model resolver service for parsing and validating model names.

Supports model names in the format: {provider}/{model}
Examples: openai/tts-1, anthropic/claude-3, ollama/qalb-urdu
"""

import logging
from typing import Dict, Optional, Tuple
from src.utils.exceptions import ValidationError

logger = logging.getLogger(__name__)


class ModelResolver:
    """Service for resolving model names to provider and model components."""
    
    # Provider/model registry
    # This can be extended or moved to a configuration file/database
    PROVIDER_MODELS = {
        "ollama": [
            "qalb-urdu",
            "deepseek-r1",
            "llama2",
            "llama2:7b",
            "llama2:13b",
            "llama2:70b",
        ],
        "openai": [
            "gpt-4",
            "gpt-4-turbo",
            "gpt-3.5-turbo",
            "gpt-3.5-turbo-16k",
            "tts-1",
            "tts-1-hd",
            "dall-e-2",
            "dall-e-3",
            "text-embedding-ada-002",
            "gpt-4-vision",
        ],
        "anthropic": [
            "claude-3",
            "claude-3-opus",
            "claude-3-sonnet",
            "claude-3-haiku",
            "claude-3-opus-vision",
            "claude-3-sonnet-vision",
        ],
        "google": [
            "gemini-pro",
            "gemini-pro-vision",
        ],
        "cohere": [
            "command",
            "command-light",
        ],
    }
    
    def __init__(self):
        """Initialize model resolver."""
        self.supported_providers = set(self.PROVIDER_MODELS.keys())
    
    def resolve_model(self, model_name: str) -> Dict[str, str]:
        """
        Resolve a model name to provider and model components.
        
        Args:
            model_name: Model name in format "{provider}/{model}"
            
        Returns:
            Dictionary with 'provider' and 'model' keys
            
        Raises:
            ValidationError: If model name format is invalid or provider/model not supported
        """
        if not model_name:
            raise ValidationError("Model name is required")
        
        # Parse model name
        parts = model_name.split("/", 1)
        if len(parts) != 2:
            raise ValidationError(
                f"Invalid model name format: '{model_name}'. Expected format: '{{provider}}/{{model}}'"
            )
        
        provider, model = parts[0].strip().lower(), parts[1].strip()
        
        # Validate provider
        if provider not in self.supported_providers:
            supported = ", ".join(sorted(self.supported_providers))
            raise ValidationError(
                f"Unsupported provider: '{provider}'. Supported providers: {supported}"
            )
        
        # Validate model
        supported_models = self.PROVIDER_MODELS.get(provider, [])
        if model not in supported_models:
            # Allow partial matches for flexibility (e.g., "gpt-4" matches "gpt-4-turbo")
            # But require at least a prefix match
            model_lower = model.lower()
            matching_models = [m for m in supported_models if m.lower().startswith(model_lower) or model_lower in m.lower()]
            
            if not matching_models:
                supported = ", ".join(supported_models[:5])  # Show first 5
                if len(supported_models) > 5:
                    supported += f" (and {len(supported_models) - 5} more)"
                raise ValidationError(
                    f"Unsupported model '{model}' for provider '{provider}'. "
                    f"Supported models: {supported}"
                )
            # Use the first matching model (or exact match if available)
            exact_match = next((m for m in supported_models if m.lower() == model_lower), None)
            model = exact_match if exact_match else matching_models[0]
        
        logger.debug(f"Resolved model '{model_name}' to provider='{provider}', model='{model}'")
        
        return {
            "provider": provider,
            "model": model,
            "original_model_name": model_name
        }
    
    def is_provider_supported(self, provider: str) -> bool:
        """Check if a provider is supported."""
        return provider.lower() in self.supported_providers
    
    def get_supported_models(self, provider: str) -> list:
        """Get list of supported models for a provider."""
        return self.PROVIDER_MODELS.get(provider.lower(), [])
    
    def get_all_providers(self) -> list:
        """Get list of all supported providers."""
        return sorted(self.supported_providers)

