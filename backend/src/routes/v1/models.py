"""Models routes for v1 API."""

from fastapi import APIRouter, Query, Depends
from src.controllers.models_controller import ModelsController
from src.services.models.model_catalog_service import ModelCatalogService
from src.container import get_container

router = APIRouter()


def get_models_controller() -> ModelsController:
    """Dependency to get models controller."""
    container = get_container()
    model_catalog_service = container.get('model_catalog_service')
    return ModelsController(model_catalog_service)


@router.get("/models")
async def get_models(
    provider: str = Query(None, description="Filter by provider"),
    category: str = Query(None, description="Filter by category"),
    search: str = Query(None, description="Search query"),
    controller: ModelsController = Depends(get_models_controller)
):
    """Get all models with optional filtering."""
    return controller.get_models(
        provider=provider,
        category=category,
        search=search
    )


@router.get("/models/{model_id}")
async def get_model(
    model_id: str,
    controller: ModelsController = Depends(get_models_controller)
):
    """Get model by ID."""
    return controller.get_model(model_id)


@router.get("/models/providers/list")
async def get_providers(
    controller: ModelsController = Depends(get_models_controller)
):
    """Get list of providers."""
    return controller.get_providers()


@router.get("/models/categories/list")
async def get_categories(
    controller: ModelsController = Depends(get_models_controller)
):
    """Get list of categories."""
    return controller.get_categories()

