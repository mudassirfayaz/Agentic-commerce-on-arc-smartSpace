"""Models controller."""

from typing import Optional
from src.services.models.model_catalog_service import ModelCatalogService
from src.utils.responses import success_response, error_response
from src.utils.exceptions import NotFoundError


class ModelsController:
    """Controller for model catalog endpoints."""
    
    def __init__(self, model_catalog_service: ModelCatalogService):
        """
        Initialize models controller.
        
        Args:
            model_catalog_service: Model catalog service instance
        """
        self.model_catalog_service = model_catalog_service
    
    def get_models(
        self,
        provider: Optional[str] = None,
        category: Optional[str] = None,
        search: Optional[str] = None
    ):
        """
        Get all models with optional filtering.
        
        Args:
            provider: Filter by provider
            category: Filter by category
            search: Search query
            
        Returns:
            Response dictionary
        """
        try:
            models = self.model_catalog_service.get_all_models(
                provider=provider,
                category=category,
                search=search
            )
            
            return success_response(
                data={
                    "models": [model.to_dict() for model in models],
                    "total": len(models)
                },
                message=f"Found {len(models)} models"
            )
        except Exception as e:
            return error_response(
                message=f"Error fetching models: {str(e)}",
                status_code=500
            )
    
    def get_model(self, model_id: str):
        """
        Get model by ID.
        
        Args:
            model_id: Model ID
            
        Returns:
            Response dictionary
        """
        try:
            model = self.model_catalog_service.get_model_by_id(model_id)
            
            if not model:
                raise NotFoundError(f"Model '{model_id}' not found")
            
            return success_response(
                data=model.to_dict(),
                message="Model retrieved successfully"
            )
        except NotFoundError as e:
            return error_response(
                message=e.message,
                status_code=e.status_code
            )
        except Exception as e:
            return error_response(
                message=f"Error fetching model: {str(e)}",
                status_code=500
            )
    
    def get_providers(self):
        """Get list of providers."""
        try:
            providers = self.model_catalog_service.get_providers()
            return success_response(
                data={"providers": providers},
                message="Providers retrieved successfully"
            )
        except Exception as e:
            return error_response(
                message=f"Error fetching providers: {str(e)}",
                status_code=500
            )
    
    def get_categories(self):
        """Get list of categories."""
        try:
            categories = self.model_catalog_service.get_categories()
            return success_response(
                data={"categories": categories},
                message="Categories retrieved successfully"
            )
        except Exception as e:
            return error_response(
                message=f"Error fetching categories: {str(e)}",
                status_code=500
            )

