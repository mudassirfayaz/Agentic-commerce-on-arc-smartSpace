"""Health check routes."""

from fastapi import APIRouter
from src.utils.responses import success_response

router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return success_response(
        data={"status": "healthy"},
        message="Service is healthy"
    )
