"""Custom exceptions for SmartSpace backend."""


class BackendException(Exception):
    """Base exception for backend errors."""
    
    def __init__(self, message: str, status_code: int = 500, details: dict = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class ValidationError(BackendException):
    """Validation error exception."""
    
    def __init__(self, message: str, details: dict = None):
        super().__init__(message, status_code=400, details=details)


class NotFoundError(BackendException):
    """Resource not found exception."""
    
    def __init__(self, message: str = "Resource not found", details: dict = None):
        super().__init__(message, status_code=404, details=details)


class UnauthorizedError(BackendException):
    """Unauthorized access exception."""
    
    def __init__(self, message: str = "Unauthorized", details: dict = None):
        super().__init__(message, status_code=401, details=details)

