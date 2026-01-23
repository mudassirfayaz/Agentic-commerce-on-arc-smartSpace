"""Text completion routes for v1 API."""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional
from src.controllers.facility_controller import FacilityController
from src.services.agentic import AgenticService
from src.middleware.auth import verify_api_key
from src.container import get_container

router = APIRouter()


class TextCompletionRequest(BaseModel):
    """Text completion request model."""
    model: str = Field(..., description="Model name in format 'provider/model' (e.g., 'openai/gpt-4')")
    text: Optional[str] = Field(None, description="Text to complete")
    prompt: Optional[str] = Field(None, description="Prompt text (alternative to 'text')")
    max_tokens: Optional[int] = Field(None, ge=1, le=8000, description="Maximum tokens to generate")
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0, description="Sampling temperature (0-2)")
    top_p: Optional[float] = Field(None, ge=0.0, le=1.0, description="Nucleus sampling parameter")
    frequency_penalty: Optional[float] = Field(None, ge=-2.0, le=2.0, description="Frequency penalty")
    presence_penalty: Optional[float] = Field(None, ge=-2.0, le=2.0, description="Presence penalty")
    metadata: Optional[dict] = Field(None, description="Additional metadata")
    
    class Config:
        json_schema_extra = {
            "example": {
                "model": "openai/gpt-4",
                "text": "Hello, world!",
                "max_tokens": 100,
                "temperature": 0.7
            }
        }


def get_facility_controller() -> FacilityController:
    """Dependency to get facility controller."""
    container = get_container()
    try:
        agentic_service = container.get('agentic_service')
    except KeyError:
        from src.services.agentic import AgenticService
        agentic_service = AgenticService()
        container.register('agentic_service', lambda c: agentic_service, singleton=True)
    
    return FacilityController(agentic_service)


@router.post("/text/completion")
async def text_completion(
    request: TextCompletionRequest,
    user_id: str = Depends(verify_api_key),
    controller: FacilityController = Depends(get_facility_controller)
):
    """
    Text completion endpoint.
    
    Generate text completions using the specified model.
    
    **Authentication**: Requires API key in `Authorization: Bearer <key>` or `X-API-Key: <key>` header.
    
    **Request Format**:
    - `model`: Model name in format `provider/model` (e.g., `openai/gpt-4`)
    - `text` or `prompt`: Text to complete (required)
    - `max_tokens`: Maximum tokens to generate (optional)
    - `temperature`: Sampling temperature 0-2 (optional)
    - Additional optional parameters
    
    **Response Format**:
    - `id`: Request ID
    - `model`: Model used
    - `choices`: Array of completion choices
    - `usage`: Token usage information
    - `payment`: Payment information (if applicable)
    """
    request_dict = request.model_dump(exclude_none=True)
    result = await controller.handle_facility_request("text", request_dict, user_id)
    
    if not result.get("success", True):
        error = result.get("error", {})
        raise HTTPException(
            status_code=error.get("status_code", 400),
            detail=error.get("message", "Request processing failed")
        )
    
    return result.get("data", result)

