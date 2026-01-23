"""Dependency injection container."""

from typing import Dict, Any, Type, Callable
from config import get_config


class Container:
    """Simple dependency injection container."""
    
    def __init__(self):
        self._services: Dict[str, Any] = {}
        self._factories: Dict[str, Callable] = {}
        self._singletons: Dict[str, Any] = {}
        self._config = get_config()
    
    def register(self, name: str, factory: Callable, singleton: bool = True):
        """
        Register a service factory.
        
        Args:
            name: Service name
            factory: Factory function to create the service
            singleton: Whether to create a singleton instance
        """
        self._factories[name] = factory
        if singleton:
            self._singletons[name] = None
    
    def get(self, name: str) -> Any:
        """
        Get a service instance.
        
        Args:
            name: Service name
            
        Returns:
            Service instance
        """
        if name not in self._factories:
            raise ValueError(f"Service '{name}' not registered")
        
        # Return singleton if exists
        if name in self._singletons:
            if self._singletons[name] is None:
                self._singletons[name] = self._factories[name](self)
            return self._singletons[name]
        
        # Create new instance
        return self._factories[name](self)
    
    def get_config(self):
        """Get configuration instance."""
        return self._config


# Global container instance
_container: Container = None


def get_container() -> Container:
    """Get the global container instance."""
    global _container
    if _container is None:
        _container = Container()
    return _container

