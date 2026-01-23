"""Response formatting utilities."""

from typing import Any, Optional, Dict
from pydantic import BaseModel


class SuccessResponse(BaseModel):
    """Standardized success response model."""
    success: bool = True
    message: str = "Success"
    data: Optional[Any] = None


class ErrorResponse(BaseModel):
    """Standardized error response model."""
    success: bool = False
    error: Dict[str, Any]


def success_response(data: Any = None, message: str = "Success", status_code: int = 200) -> Dict:
    """
    Create a standardized success response.
    
    Args:
        data: Response data
        message: Success message
        status_code: HTTP status code (for FastAPI, returned separately)
        
    Returns:
        Response dictionary
    """
    response = {
        "success": True,
        "message": message
    }
    if data is not None:
        response["data"] = data
    
    return response


def error_response(
    message: str,
    status_code: int = 400,
    error_code: Optional[str] = None,
    details: Optional[Dict] = None
) -> Dict:
    """
    Create a standardized error response.
    
    Args:
        message: Error message
        status_code: HTTP status code (for FastAPI, use HTTPException)
        error_code: Optional error code
        details: Optional error details
        
    Returns:
        Response dictionary
    """
    response = {
        "success": False,
        "error": {
            "message": message
        }
    }
    
    if error_code:
        response["error"]["code"] = error_code
    
    if details:
        response["error"]["details"] = details
    
    return response
