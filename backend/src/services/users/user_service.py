"""User service for user management."""

from typing import Optional
from src.models.user import User
from src.repositories.base import BaseRepository


class UserService:
    """Service for user operations."""
    
    def __init__(self, user_repository: BaseRepository):
        """
        Initialize user service.
        
        Args:
            user_repository: User repository instance
        """
        self.user_repository = user_repository
    
    async def get_user(self, user_id: str) -> Optional[User]:
        """
        Get user by ID.
        
        Args:
            user_id: User ID
            
        Returns:
            User object or None
        """
        data = await self.user_repository.get_by_id(user_id)
        if data:
            return User(**data)
        return None
    
    async def create_user(self, user_data: dict) -> User:
        """
        Create a new user.
        
        Args:
            user_data: User data dictionary
            
        Returns:
            Created user
        """
        data = await self.user_repository.create(user_data)
        return User(**data)

