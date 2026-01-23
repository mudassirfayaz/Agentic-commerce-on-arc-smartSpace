"""Request validation middleware."""

from flask import request
from src.utils.validators import validate_required_fields
from src.utils.exceptions import ValidationError


def validate_json_request():
    """Validate that request has JSON content type."""
    if request.method in ['POST', 'PUT', 'PATCH']:
        if not request.is_json:
            raise ValidationError("Request must have Content-Type: application/json")


def validate_request_data(required_fields: list):
    """
    Decorator to validate request data.
    
    Args:
        required_fields: List of required field names
    """
    def decorator(f):
        from functools import wraps
        
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if request.is_json:
                data = request.get_json() or {}
                validate_required_fields(data, required_fields)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

