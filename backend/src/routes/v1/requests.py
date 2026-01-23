"""Request routes for v1 API."""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from src.controllers.requests_controller import RequestsController
from src.services.agentic import AgenticService
from src.middleware.auth import verify_api_key
from src.container import get_container

router = APIRouter()


class Message(BaseModel):
    """Chat message model."""
    role: str = Field(..., description="Message role (user, assistant, system)")
    content: str = Field(..., description="Message content")


class ExternalRequest(BaseModel):
    """External API request model."""
    provider: str = Field(..., description="API provider name (e.g., 'ollama', 'openai')")
    model: str = Field(..., description="Model name (e.g., 'deepseek-r1', 'gpt-4')")
    messages: Optional[List[Message]] = Field(None, description="Chat messages (for chat operations)")
    prompt: Optional[str] = Field(None, description="Prompt text (for completion operations)")
    operation_type: str = Field(default="chat", description="Operation type (chat, completion, etc.)")
    project_id: Optional[str] = Field(None, description="Project ID (optional)")
    agent_id: Optional[str] = Field(None, description="Agent ID (optional)")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    temperature: Optional[float] = Field(None, description="Temperature for generation")
    max_tokens: Optional[int] = Field(None, description="Maximum tokens to generate")


def get_requests_controller() -> RequestsController:
    """Dependency to get requests controller."""
    container = get_container()
    # Get or create agentic service
    try:
        agentic_service = container.get('agentic_service')
    except KeyError:
        # Create new agentic service if not in container
        agentic_service = AgenticService()
        container.register('agentic_service', lambda c: agentic_service, singleton=True)
    
    return RequestsController(agentic_service)


@router.post("/requests")
async def create_request(
    request: ExternalRequest,
    user_id: str = Depends(verify_api_key),
    controller: RequestsController = Depends(get_requests_controller)
):
    """
    Create and process an external API request.
    
    This endpoint accepts authenticated requests from external applications
    and processes them through the agentic brain.
    
    **Authentication**: Requires API key in `Authorization: Bearer <key>` or `X-API-Key: <key>` header.
    
    **Request Format**:
    - `provider`: API provider name (required)
    - `model`: Model name (required)
    - `messages`: List of chat messages (required for chat operations)
    - `prompt`: Prompt text (required for completion operations)
    - `operation_type`: Type of operation (default: "chat")
    - `project_id`: Optional project ID
    - `agent_id`: Optional agent ID
    - `metadata`: Optional metadata dictionary
    
    **Response Format**:
    - `success`: Boolean indicating if request was approved
    - `decision`: Decision object with outcome, reasoning, confidence
    - `response`: API response from provider (if approved)
    - `payment`: Payment details including transaction hash, amount, variance
    - `message`: Human-readable status message
    """
    # Convert Pydantic model to dict
    request_dict = request.model_dump(exclude_none=True)
    
    # Handle messages conversion
    if request.messages:
        request_dict["messages"] = [
            {"role": msg.role, "content": msg.content}
            for msg in request.messages
        ]
    
    # Process request
    result = await controller.handle_external_request(request_dict, user_id)
    
    # Check if there's an error in the result
    if not result.get("success", True):
        error = result.get("error", {})
        raise HTTPException(
            status_code=error.get("status_code", 400),
            detail=error.get("message", "Request processing failed")
        )
    
    return result

