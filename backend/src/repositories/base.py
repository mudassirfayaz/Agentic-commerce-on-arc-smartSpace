"""Base repository interface."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class BaseRepository(ABC):
    """Base repository interface for data access."""
    
    @abstractmethod
    async def create(self, data: Dict[str, Any]) -> Any:
        """Create a new record."""
        pass
    
    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[Any]:
        """Get a record by ID."""
        pass
    
    @abstractmethod
    async def update(self, id: str, data: Dict[str, Any]) -> Optional[Any]:
        """Update a record."""
        pass
    
    @abstractmethod
    async def delete(self, id: str) -> bool:
        """Delete a record."""
        pass
    
    @abstractmethod
    async def list(self, filters: Optional[Dict[str, Any]] = None, limit: int = 100, offset: int = 0) -> List[Any]:
        """List records with optional filters."""
        pass

