"""Audio/speech routes for v1 API."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from src.controllers.facility_controller import FacilityController
from src.services.agentic import AgenticService
from src.middleware.auth import verify_api_key
from src.container import get_container

router = APIRouter()


class AudioSpeechRequest(BaseModel):
    """Audio/speech request model."""
    model: str = Field(..., description="Model name in format 'provider/model' (e.g., 'openai/tts-1')")
    text: Optional[str] = Field(None, description="Text to convert to speech")
    input: Optional[str] = Field(None, description="Input text (alternative to 'text')")
    voice: Optional[str] = Field(None, description="Voice to use (e.g., 'nova', 'alloy', 'echo')")
    speed: Optional[float] = Field(None, ge=0.25, le=4.0, description="Speech speed (0.25-4.0)")
    response_format: Optional[str] = Field(None, description="Response format (e.g., 'mp3', 'opus')")
    metadata: Optional[dict] = Field(None, description="Additional metadata")
    
    class Config:
        json_schema_extra = {
            "example": {
                "model": "openai/tts-1",
                "text": "Hello, world!",
                "voice": "nova"
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


@router.post("/audio/speech")
async def audio_speech(
    request: AudioSpeechRequest,
    user_id: str = Depends(verify_api_key),
    controller: FacilityController = Depends(get_facility_controller)
):
    """
    Audio/speech generation endpoint.
    
    Convert text to speech using the specified model.
    
    **Authentication**: Requires API key in `Authorization: Bearer <key>` or `X-API-Key: <key>` header.
    
    **Request Format**:
    - `model`: Model name in format `provider/model` (e.g., `openai/tts-1`)
    - `text` or `input`: Text to convert to speech (required)
    - `voice`: Voice to use (optional)
    - `speed`: Speech speed 0.25-4.0 (optional)
    - Additional optional parameters
    
    **Response Format**:
    - `id`: Request ID
    - `model`: Model used
    - `choices`: Array with audio data
    - `usage`: Token usage information
    - `payment`: Payment information (if applicable)
    """
    request_dict = request.model_dump(exclude_none=True)
    result = await controller.handle_facility_request("audio", request_dict, user_id)
    
    if not result.get("success", True):
        error = result.get("error", {})
        raise HTTPException(
            status_code=error.get("status_code", 400),
            detail=error.get("message", "Request processing failed")
        )
    
    return result.get("data", result)

