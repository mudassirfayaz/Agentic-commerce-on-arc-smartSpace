"""Model catalog data model."""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ModelCatalogEntry:
    """Model catalog entry."""
    id: str
    name: str
    provider: str
    category: str
    capabilities: List[str]
    pricing_tier: str
    description: str
    icon: str
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "provider": self.provider,
            "category": self.category,
            "capabilities": self.capabilities,
            "pricing_tier": self.pricing_tier,
            "description": self.description,
            "icon": self.icon
        }

