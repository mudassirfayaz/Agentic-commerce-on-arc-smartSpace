"""Request controller for external API requests."""

import logging
from typing import Dict, Any, Optional
from src.services.agentic import AgenticService
from src.utils.responses import success_response, error_response
from src.utils.exceptions import ValidationError

logger = logging.getLogger(__name__)


class RequestsController:
    """Controller for external API request endpoints."""
    
    def __init__(self, agentic_service: AgenticService):
        """
        Initialize requests controller.
        
        Args:
            agentic_service: Agentic service instance
        """
        self.agentic_service = agentic_service
    
    def _transform_external_request(
        self,
        request_body: Dict[str, Any],
        user_id: str
    ) -> Dict[str, Any]:
        """
        Transform external request format to agentic brain format.
        
        Args:
            request_body: External request body
            user_id: Authenticated user ID
            
        Returns:
            Transformed request data for agentic brain
        """
        # Extract required fields
        provider = request_body.get("provider")
        model = request_body.get("model")
        operation_type = request_body.get("operation_type", "chat")
        
        # Extract messages or prompt
        messages = request_body.get("messages")
        prompt = request_body.get("prompt")
        
        if not messages and not prompt:
            raise ValidationError("Either 'messages' or 'prompt' is required")
        
        # Build request params
        request_params = {}
        if messages:
            request_params["messages"] = messages
        if prompt:
            request_params["prompt"] = prompt
        
        # Add any additional params from request body
        if "temperature" in request_body:
            request_params["temperature"] = request_body["temperature"]
        if "max_tokens" in request_body:
            request_params["max_tokens"] = request_body["max_tokens"]
        
        # Build agentic brain request format
        agentic_request = {
            "user_id": user_id,
            "project_id": request_body.get("project_id"),  # Optional, will use default if None
            "agent_id": request_body.get("agent_id"),  # Optional
            "api_provider": provider,
            "model_name": model,
            "operation_type": operation_type,
            "request_params": request_params,
            "metadata": request_body.get("metadata", {})
        }
        
        return agentic_request
    
    def _format_response(self, agentic_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format agentic brain response to external API format.
        
        Args:
            agentic_result: Result from agentic brain
            
        Returns:
            Formatted response
        """
        # Agentic brain already returns a well-structured response
        # We just need to ensure it matches our API contract
        return {
            "success": agentic_result.get("success", False),
            "decision": agentic_result.get("decision", {}),
            "response": agentic_result.get("response"),
            "payment": agentic_result.get("payment"),
            "message": agentic_result.get("message", "Request processed")
        }
    
    async def handle_external_request(
        self,
        request_body: Dict[str, Any],
        user_id: str
    ) -> Dict[str, Any]:
        """
        Handle external API request.
        
        Args:
            request_body: Request body from external client
            user_id: Authenticated user ID from API key
            
        Returns:
            Response dictionary
        """
        try:
            # Validate required fields
            if not request_body.get("provider"):
                raise ValidationError("'provider' field is required")
            if not request_body.get("model"):
                raise ValidationError("'model' field is required")
            if not request_body.get("messages") and not request_body.get("prompt"):
                raise ValidationError("Either 'messages' or 'prompt' field is required")
            
            # Transform external format to agentic brain format
            agentic_request = self._transform_external_request(request_body, user_id)
            
            # Process request through agentic brain
            logger.info(f"Processing request for user {user_id}: {agentic_request.get('api_provider')}/{agentic_request.get('model_name')}")
            result = await self.agentic_service.process_request(agentic_request)
            
            # Format response
            response = self._format_response(result)
            
            return success_response(
                data=response,
                message="Request processed successfully"
            )
            
        except ValidationError as e:
            logger.warning(f"Validation error: {e.message}")
            return error_response(
                message=e.message,
                status_code=e.status_code,
                details=e.details
            )
        except Exception as e:
            logger.error(f"Error processing external request: {e}", exc_info=True)
            return error_response(
                message="Internal server error processing request",
                status_code=500
            )

