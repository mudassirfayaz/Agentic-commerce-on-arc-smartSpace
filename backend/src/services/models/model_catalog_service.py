"""Model catalog service."""

import json
import os
from pathlib import Path
from typing import List, Optional, Dict
from src.models.model_catalog import ModelCatalogEntry


class ModelCatalogService:
    """Service for model catalog operations."""
    
    def __init__(self, catalog_path: Optional[str] = None):
        """
        Initialize model catalog service.
        
        Args:
            catalog_path: Path to model catalog JSON file
        """
        if catalog_path is None:
            # Default to frontend data file
            catalog_path = str(
                Path(__file__).parent.parent.parent.parent.parent / 
                "frontend" / "src" / "data" / "models.json"
            )
        self.catalog_path = catalog_path
        self._catalog_cache: Optional[List[ModelCatalogEntry]] = None
    
    def _load_catalog(self) -> List[ModelCatalogEntry]:
        """Load model catalog from JSON file."""
        if self._catalog_cache is not None:
            return self._catalog_cache
        
        try:
            with open(self.catalog_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            models = []
            for model_data in data.get('models', []):
                models.append(ModelCatalogEntry(**model_data))
            
            self._catalog_cache = models
            return models
        except Exception as e:
            # Return empty list if file not found or error
            return []
    
    def get_all_models(
        self,
        provider: Optional[str] = None,
        category: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[ModelCatalogEntry]:
        """
        Get all models with optional filtering.
        
        Args:
            provider: Filter by provider
            category: Filter by category
            search: Search query (matches name, provider, description)
            
        Returns:
            List of model catalog entries
        """
        models = self._load_catalog()
        
        # Apply filters
        if provider:
            models = [m for m in models if m.provider == provider]
        
        if category:
            models = [m for m in models if m.category == category]
        
        if search:
            query = search.lower()
            models = [
                m for m in models
                if query in m.name.lower() or
                   query in m.provider.lower() or
                   query in m.description.lower() or
                   any(query in cap.lower() for cap in m.capabilities)
            ]
        
        return models
    
    def get_model_by_id(self, model_id: str) -> Optional[ModelCatalogEntry]:
        """
        Get model by ID.
        
        Args:
            model_id: Model ID
            
        Returns:
            Model catalog entry or None
        """
        models = self._load_catalog()
        for model in models:
            if model.id == model_id:
                return model
        return None
    
    def get_providers(self) -> List[str]:
        """Get list of unique providers."""
        models = self._load_catalog()
        providers = list(set(m.provider for m in models))
        return sorted(providers)
    
    def get_categories(self) -> List[str]:
        """Get list of unique categories."""
        models = self._load_catalog()
        categories = list(set(m.category for m in models))
        return sorted(categories)

