"""
Request transformers for converting facility-specific formats to agentic brain format.
"""

import logging
from typing import Dict, Any, Optional
from src.utils.exceptions import ValidationError

logger = logging.getLogger(__name__)


class BaseTransformer:
    """Base class for request transformers."""
    
    def __init__(self, operation_type: str):
        """
        Initialize transformer.
        
        Args:
            operation_type: Operation type for agentic brain (e.g., "completion", "audio")
        """
        self.operation_type = operation_type
    
    def transform(self, request_data: Dict[str, Any], user_id: str, provider: str, model: str) -> Dict[str, Any]:
        """
        Transform facility-specific request to agentic brain format.
        
        Args:
            request_data: Facility-specific request data
            user_id: Authenticated user ID
            provider: Resolved provider name
            model: Resolved model name
            
        Returns:
            Transformed request in agentic brain format
        """
        raise NotImplementedError("Subclasses must implement transform method")
    
    def _build_base_request(self, user_id: str, provider: str, model: str, request_params: Dict[str, Any]) -> Dict[str, Any]:
        """Build base agentic brain request structure."""
        return {
            "user_id": user_id,
            "api_provider": provider,
            "model_name": model,
            "operation_type": self.operation_type,
            "request_params": request_params,
            "metadata": {}
        }


class TextCompletionTransformer(BaseTransformer):
    """Transformer for text completion requests."""
    
    def __init__(self):
        super().__init__("completion")
    
    def transform(self, request_data: Dict[str, Any], user_id: str, provider: str, model: str) -> Dict[str, Any]:
        """Transform text completion request."""
        # Extract required fields
        text = request_data.get("text") or request_data.get("prompt")
        if not text:
            raise ValidationError("Either 'text' or 'prompt' field is required for text completion")
        
        # Build request params
        request_params = {
            "text": text,
            "prompt": text,  # Support both field names
        }
        
        # Add optional parameters
        if "max_tokens" in request_data:
            max_tokens = request_data["max_tokens"]
            if isinstance(max_tokens, int) and max_tokens > 0:
                request_params["max_tokens"] = max_tokens
        
        if "temperature" in request_data:
            temperature = request_data["temperature"]
            if isinstance(temperature, (int, float)) and 0 <= temperature <= 2:
                request_params["temperature"] = temperature
        
        if "top_p" in request_data:
            request_params["top_p"] = request_data["top_p"]
        
        if "frequency_penalty" in request_data:
            request_params["frequency_penalty"] = request_data["frequency_penalty"]
        
        if "presence_penalty" in request_data:
            request_params["presence_penalty"] = request_data["presence_penalty"]
        
        # Add any additional metadata
        metadata = request_data.get("metadata", {})
        
        base_request = self._build_base_request(user_id, provider, model, request_params)
        base_request["metadata"] = metadata
        
        return base_request


class AudioSpeechTransformer(BaseTransformer):
    """Transformer for audio/speech requests."""
    
    def __init__(self):
        super().__init__("audio")
    
    def transform(self, request_data: Dict[str, Any], user_id: str, provider: str, model: str) -> Dict[str, Any]:
        """Transform audio/speech request."""
        # Extract required fields
        text = request_data.get("text") or request_data.get("input")
        if not text:
            raise ValidationError("'text' or 'input' field is required for audio/speech")
        
        # Build request params
        request_params = {
            "text": text,
            "input": text,  # Support both field names
        }
        
        # Add voice parameter if provided
        if "voice" in request_data:
            request_params["voice"] = request_data["voice"]
        
        if "speed" in request_data:
            request_params["speed"] = request_data["speed"]
        
        if "response_format" in request_data:
            request_params["response_format"] = request_data["response_format"]
        
        # Add metadata
        metadata = request_data.get("metadata", {})
        
        base_request = self._build_base_request(user_id, provider, model, request_params)
        base_request["metadata"] = metadata
        
        return base_request


class ImageGenerationTransformer(BaseTransformer):
    """Transformer for image generation requests."""
    
    def __init__(self):
        super().__init__("image")
    
    def transform(self, request_data: Dict[str, Any], user_id: str, provider: str, model: str) -> Dict[str, Any]:
        """Transform image generation request."""
        # Extract required fields
        prompt = request_data.get("prompt")
        if not prompt:
            raise ValidationError("'prompt' field is required for image generation")
        
        # Build request params
        request_params = {
            "prompt": prompt,
        }
        
        # Add optional parameters
        if "size" in request_data:
            request_params["size"] = request_data["size"]
        
        if "n" in request_data:
            request_params["n"] = request_data["n"]
        
        if "quality" in request_data:
            request_params["quality"] = request_data["quality"]
        
        if "style" in request_data:
            request_params["style"] = request_data["style"]
        
        # Add metadata
        metadata = request_data.get("metadata", {})
        
        base_request = self._build_base_request(user_id, provider, model, request_params)
        base_request["metadata"] = metadata
        
        return base_request


class EmbeddingsTransformer(BaseTransformer):
    """Transformer for embeddings requests."""
    
    def __init__(self):
        super().__init__("embedding")
    
    def transform(self, request_data: Dict[str, Any], user_id: str, provider: str, model: str) -> Dict[str, Any]:
        """Transform embeddings request."""
        # Extract required fields
        input_text = request_data.get("input")
        if not input_text:
            raise ValidationError("'input' field is required for embeddings")
        
        # Build request params
        request_params = {
            "input": input_text,
        }
        
        # Handle both string and list inputs
        if isinstance(input_text, list):
            request_params["input"] = input_text
        else:
            request_params["input"] = [input_text] if isinstance(input_text, str) else input_text
        
        # Add metadata
        metadata = request_data.get("metadata", {})
        
        base_request = self._build_base_request(user_id, provider, model, request_params)
        base_request["metadata"] = metadata
        
        return base_request


class VisionTransformer(BaseTransformer):
    """Transformer for vision/image analysis requests."""
    
    def __init__(self):
        super().__init__("vision")
    
    def transform(self, request_data: Dict[str, Any], user_id: str, provider: str, model: str) -> Dict[str, Any]:
        """Transform vision request."""
        # Extract required fields
        image = request_data.get("image")
        prompt = request_data.get("prompt") or request_data.get("text")
        
        if not image:
            raise ValidationError("'image' field is required for vision analysis")
        if not prompt:
            raise ValidationError("'prompt' or 'text' field is required for vision analysis")
        
        # Build request params
        request_params = {
            "image": image,
            "prompt": prompt,
            "text": prompt,  # Support both field names
        }
        
        # Add optional parameters
        if "max_tokens" in request_data:
            request_params["max_tokens"] = request_data["max_tokens"]
        
        if "temperature" in request_data:
            request_params["temperature"] = request_data["temperature"]
        
        # Add metadata
        metadata = request_data.get("metadata", {})
        
        base_request = self._build_base_request(user_id, provider, model, request_params)
        base_request["metadata"] = metadata
        
        return base_request


# Transformer registry
TRANSFORMERS = {
    "text": TextCompletionTransformer(),
    "completion": TextCompletionTransformer(),
    "audio": AudioSpeechTransformer(),
    "speech": AudioSpeechTransformer(),
    "image": ImageGenerationTransformer(),
    "images": ImageGenerationTransformer(),
    "embedding": EmbeddingsTransformer(),
    "embeddings": EmbeddingsTransformer(),
    "vision": VisionTransformer(),
}


def get_transformer(facility: str) -> BaseTransformer:
    """
    Get transformer for a facility type.
    
    Args:
        facility: Facility type (e.g., "text", "audio", "image")
        
    Returns:
        Transformer instance
        
    Raises:
        ValidationError: If facility type is not supported
    """
    facility_lower = facility.lower()
    transformer = TRANSFORMERS.get(facility_lower)
    
    if not transformer:
        supported = ", ".join(sorted(set(TRANSFORMERS.keys())))
        raise ValidationError(
            f"Unsupported facility type: '{facility}'. Supported facilities: {supported}"
        )
    
    return transformer

