"""Image generation routes for v1 API."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from src.controllers.facility_controller import FacilityController
from src.services.agentic import AgenticService
from src.middleware.auth import verify_api_key
from src.container import get_container

router = APIRouter()


class ImageGenerationRequest(BaseModel):
    """Image generation request model."""
    model: str = Field(..., description="Model name in format 'provider/model' (e.g., 'openai/dall-e-3')")
    prompt: str = Field(..., description="Text prompt for image generation")
    size: Optional[str] = Field(None, description="Image size (e.g., '1024x1024', '512x512')")
    n: Optional[int] = Field(None, ge=1, le=10, description="Number of images to generate")
    quality: Optional[str] = Field(None, description="Image quality (e.g., 'standard', 'hd')")
    style: Optional[str] = Field(None, description="Image style (e.g., 'vivid', 'natural')")
    metadata: Optional[dict] = Field(None, description="Additional metadata")
    
    class Config:
        json_schema_extra = {
            "example": {
                "model": "openai/dall-e-3",
                "prompt": "A beautiful sunset over the ocean",
                "size": "1024x1024"
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


@router.post("/images/generate")
async def image_generation(
    request: ImageGenerationRequest,
    user_id: str = Depends(verify_api_key),
    controller: FacilityController = Depends(get_facility_controller)
):
    """
    Image generation endpoint.
    
    Generate images from text prompts using the specified model.
    
    **Authentication**: Requires API key in `Authorization: Bearer <key>` or `X-API-Key: <key>` header.
    
    **Request Format**:
    - `model`: Model name in format `provider/model` (e.g., `openai/dall-e-3`)
    - `prompt`: Text prompt for image generation (required)
    - `size`: Image size (optional)
    - `n`: Number of images to generate 1-10 (optional)
    - Additional optional parameters
    
    **Response Format**:
    - `id`: Request ID
    - `model`: Model used
    - `choices`: Array with generated image URLs/data
    - `usage`: Token usage information
    - `payment`: Payment information (if applicable)
    """
    request_dict = request.model_dump(exclude_none=True)
    result = await controller.handle_facility_request("image", request_dict, user_id)
    
    if not result.get("success", True):
        error = result.get("error", {})
        raise HTTPException(
            status_code=error.get("status_code", 400),
            detail=error.get("message", "Request processing failed")
        )
    
    return result.get("data", result)

