"""Vision/image analysis routes for v1 API."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from src.controllers.facility_controller import FacilityController
from src.services.agentic import AgenticService
from src.middleware.auth import verify_api_key
from src.container import get_container

router = APIRouter()


class VisionAnalysisRequest(BaseModel):
    """Vision/image analysis request model."""
    model: str = Field(..., description="Model name in format 'provider/model' (e.g., 'openai/gpt-4-vision')")
    image: str = Field(..., description="Base64-encoded image or image URL")
    prompt: Optional[str] = Field(None, description="Prompt/question about the image")
    text: Optional[str] = Field(None, description="Text prompt (alternative to 'prompt')")
    max_tokens: Optional[int] = Field(None, ge=1, le=8000, description="Maximum tokens to generate")
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0, description="Sampling temperature (0-2)")
    metadata: Optional[dict] = Field(None, description="Additional metadata")
    
    class Config:
        json_schema_extra = {
            "example": {
                "model": "openai/gpt-4-vision",
                "image": "data:image/jpeg;base64,/9j/4AAQSkZJRg...",
                "prompt": "What's in this image?"
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


@router.post("/vision/analyze")
async def vision_analyze(
    request: VisionAnalysisRequest,
    user_id: str = Depends(verify_api_key),
    controller: FacilityController = Depends(get_facility_controller)
):
    """
    Vision/image analysis endpoint.
    
    Analyze images using vision-capable models.
    
    **Authentication**: Requires API key in `Authorization: Bearer <key>` or `X-API-Key: <key>` header.
    
    **Request Format**:
    - `model`: Model name in format `provider/model` (e.g., `openai/gpt-4-vision`)
    - `image`: Base64-encoded image or image URL (required)
    - `prompt` or `text`: Question or prompt about the image (required)
    - `max_tokens`: Maximum tokens to generate (optional)
    - `temperature`: Sampling temperature 0-2 (optional)
    
    **Response Format**:
    - `id`: Request ID
    - `model`: Model used
    - `choices`: Array with analysis results
    - `usage`: Token usage information
    - `payment`: Payment information (if applicable)
    """
    request_dict = request.model_dump(exclude_none=True)
    result = await controller.handle_facility_request("vision", request_dict, user_id)
    
    if not result.get("success", True):
        error = result.get("error", {})
        raise HTTPException(
            status_code=error.get("status_code", 400),
            detail=error.get("message", "Request processing failed")
        )
    
    return result.get("data", result)

