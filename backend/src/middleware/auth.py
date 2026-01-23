"""Authentication middleware for FastAPI."""

import logging
from typing import Optional
from fastapi import Header, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.services.api_keys import ApiKeyService
from src.utils.exceptions import UnauthorizedError

logger = logging.getLogger(__name__)

# Security scheme for OpenAPI docs
security = HTTPBearer(auto_error=False)


async def get_api_key_from_header(
    authorization: Optional[str] = Header(None, alias="Authorization"),
    x_api_key: Optional[str] = Header(None, alias="X-API-Key")
) -> Optional[str]:
    """
    Extract API key from request headers.
    
    Supports both:
    - Authorization: Bearer <api_key>
    - X-API-Key: <api_key>
    
    Args:
        authorization: Authorization header value
        x_api_key: X-API-Key header value
        
    Returns:
        API key string or None if not found
    """
    # Try Authorization: Bearer header first
    if authorization:
        try:
            scheme, token = authorization.split(" ", 1)
            if scheme.lower() == "bearer":
                return token
        except ValueError:
            # Invalid format, try X-API-Key
            pass
    
    # Try X-API-Key header
    if x_api_key:
        return x_api_key
    
    return None


async def get_api_key_service() -> ApiKeyService:
    """Dependency to get API key service."""
    from src.container import get_container
    container = get_container()
    try:
        return container.get('api_key_service')
    except KeyError:
        # Fallback to creating new instance
        return ApiKeyService()


async def verify_api_key(
    api_key: Optional[str] = Depends(get_api_key_from_header),
    api_key_service: ApiKeyService = Depends(get_api_key_service)
) -> str:
    """
    Verify API key and return user_id.
    
    This is a FastAPI dependency that can be used in route handlers.
    
    Args:
        api_key_service: API key service instance
        api_key: API key from headers
        
    Returns:
        user_id if valid
        
    Raises:
        HTTPException with 401 if invalid
    """
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key required. Provide 'Authorization: Bearer <key>' or 'X-API-Key: <key>' header."
        )
    
    user_id = api_key_service.verify_api_key(api_key)
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or revoked API key."
        )
    
    return user_id


def require_auth_dep() -> Depends:
    """
    Dependency factory for requiring API key authentication.
    
    Usage:
        @router.post("/endpoint")
        async def my_endpoint(user_id: str = Depends(require_auth_dep())):
            ...
    """
    return Depends(verify_api_key)
