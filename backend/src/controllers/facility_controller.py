"""
Facility controller for handling facility-specific API requests.
"""

import logging
from typing import Dict, Any, Optional
from src.services.model_resolver import ModelResolver
from src.services.agentic import AgenticService
from src.utils.request_transformers import get_transformer
from src.utils.responses import success_response, error_response
from src.utils.exceptions import ValidationError

logger = logging.getLogger(__name__)


class FacilityController:
    """Controller for facility-specific API requests."""
    
    def __init__(self, agentic_service: AgenticService):
        """
        Initialize facility controller.
        
        Args:
            agentic_service: Agentic service instance
        """
        self.agentic_service = agentic_service
        self.model_resolver = ModelResolver()
    
    async def handle_facility_request(
        self,
        facility: str,
        request_data: Dict[str, Any],
        user_id: str
    ) -> Dict[str, Any]:
        """
        Handle a facility-specific request.
        
        Args:
            facility: Facility type (e.g., "text", "audio", "image")
            request_data: Request data from client
            user_id: Authenticated user ID
            
        Returns:
            Response dictionary
        """
        try:
            # Validate model field
            model_name = request_data.get("model")
            if not model_name:
                raise ValidationError("'model' field is required")
            
            # Resolve model name to provider and model
            logger.info(f"Resolving model: {model_name}")
            model_info = self.model_resolver.resolve_model(model_name)
            provider = model_info["provider"]
            model = model_info["model"]
            
            # Get transformer for facility
            transformer = get_transformer(facility)
            
            # Transform request to agentic brain format
            logger.info(f"Transforming {facility} request to agentic brain format")
            agentic_request = transformer.transform(request_data, user_id, provider, model)
            
            # Process request through agentic brain
            logger.info(f"Processing request through agentic brain: {provider}/{model}")
            result = await self.agentic_service.process_request(agentic_request)
            
            # Check if request was successful
            if not result.get("success", False):
                # Extract error information
                decision = result.get("decision", {})
                rejection_reason = decision.get("rejection_reason") or decision.get("reasoning") or "Request rejected"
                
                error = error_response(
                    message=rejection_reason,
                    details={
                        "decision": decision,
                        "outcome": decision.get("outcome", "REJECTED")
                    }
                )
                error["error"]["status_code"] = 400
                return error
            
            # Extract provider response
            provider_response = result.get("response", {})
            
            # Format response for facility
            response_data = {
                "id": result.get("request_id", "unknown"),
                "model": model_name,
                "created": result.get("created_at"),
                "choices": self._format_choices(provider_response, facility),
                "usage": result.get("usage", {}),
            }
            
            # Add payment information if available
            payment = result.get("payment")
            if payment:
                response_data["payment"] = {
                    "transaction_hash": payment.get("transaction_hash"),
                    "amount_usdc": payment.get("amount_usdc"),
                    "status": payment.get("status"),
                }
            
            return success_response(
                data=response_data,
                message="Request processed successfully"
            )
            
        except ValidationError as e:
            logger.warning(f"Validation error: {e.message}")
            return error_response(
                message=e.message,
                status_code=e.status_code or 400,
                details=e.details
            )
        except Exception as e:
            logger.error(f"Error processing facility request: {e}", exc_info=True)
            return error_response(
                message="Internal server error processing request",
                status_code=500
            )
    
    def _format_choices(self, provider_response: Dict[str, Any], facility: str) -> list:
        """
        Format provider response into choices array.
        
        Args:
            provider_response: Response from provider
            facility: Facility type
            
        Returns:
            List of choice objects
        """
        # Handle different response formats
        if isinstance(provider_response, dict):
            # Check if response already has choices
            if "choices" in provider_response:
                return provider_response["choices"]
            
            # Check if response has data array
            if "data" in provider_response:
                return provider_response["data"]
            
            # For audio/speech, return audio data
            if facility in ["audio", "speech"]:
                return [{
                    "index": 0,
                    "audio": provider_response.get("audio") or provider_response.get("data"),
                    "text": provider_response.get("text", "")
                }]
            
            # For images, return image URLs/data
            if facility in ["image", "images"]:
                images = provider_response.get("images") or provider_response.get("data") or []
                if isinstance(images, list):
                    return [{"index": i, "url": img} if isinstance(img, str) else img for i, img in enumerate(images)]
                return [{"index": 0, "url": images}]
            
            # For embeddings, return embedding vectors
            if facility in ["embedding", "embeddings"]:
                embeddings = provider_response.get("embeddings") or provider_response.get("data") or []
                return [{"index": i, "embedding": emb} for i, emb in enumerate(embeddings)]
            
            # For text/vision, return text content
            text = provider_response.get("text") or provider_response.get("content") or provider_response.get("message")
            if text:
                return [{
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": text
                    },
                    "finish_reason": provider_response.get("finish_reason", "stop")
                }]
        
        # Fallback: wrap response in choice format
        return [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": str(provider_response)
            },
            "finish_reason": "stop"
        }]

