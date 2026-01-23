"""Embeddings routes for v1 API."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Union, List
from src.controllers.facility_controller import FacilityController
from src.services.agentic import AgenticService
from src.middleware.auth import verify_api_key
from src.container import get_container

router = APIRouter()


class EmbeddingsRequest(BaseModel):
    """Embeddings request model."""
    model: str = Field(..., description="Model name in format 'provider/model' (e.g., 'openai/text-embedding-ada-002')")
    input: Union[str, List[str]] = Field(..., description="Input text(s) to generate embeddings for")
    metadata: Optional[dict] = Field(None, description="Additional metadata")
    
    class Config:
        json_schema_extra = {
            "example": {
                "model": "openai/text-embedding-ada-002",
                "input": "Hello, world!"
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


@router.post("/embeddings")
async def embeddings(
    request: EmbeddingsRequest,
    user_id: str = Depends(verify_api_key),
    controller: FacilityController = Depends(get_facility_controller)
):
    """
    Embeddings generation endpoint.
    
    Generate embeddings for text using the specified model.
    
    **Authentication**: Requires API key in `Authorization: Bearer <key>` or `X-API-Key: <key>` header.
    
    **Request Format**:
    - `model`: Model name in format `provider/model` (e.g., `openai/text-embedding-ada-002`)
    - `input`: Text or array of texts to generate embeddings for (required)
    
    **Response Format**:
    - `id`: Request ID
    - `model`: Model used
    - `choices`: Array with embedding vectors
    - `usage`: Token usage information
    - `payment`: Payment information (if applicable)
    """
    request_dict = request.model_dump(exclude_none=True)
    result = await controller.handle_facility_request("embeddings", request_dict, user_id)
    
    if not result.get("success", True):
        error = result.get("error", {})
        raise HTTPException(
            status_code=error.get("status_code", 400),
            detail=error.get("message", "Request processing failed")
        )
    
    return result.get("data", result)

