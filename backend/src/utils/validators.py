"""Request validation utilities."""

from typing import Any, Dict, List, Optional
from .exceptions import ValidationError


def validate_required_fields(data: Dict, required_fields: List[str]) -> None:
    """
    Validate that required fields are present in data.
    
    Args:
        data: Data dictionary to validate
        required_fields: List of required field names
        
    Raises:
        ValidationError: If any required field is missing
    """
    missing_fields = [field for field in required_fields if field not in data or data[field] is None]
    if missing_fields:
        raise ValidationError(
            f"Missing required fields: {', '.join(missing_fields)}",
            details={"missing_fields": missing_fields}
        )


def validate_field_type(data: Dict, field: str, expected_type: type) -> None:
    """
    Validate that a field has the expected type.
    
    Args:
        data: Data dictionary
        field: Field name to validate
        expected_type: Expected type
        
    Raises:
        ValidationError: If field type doesn't match
    """
    if field in data and not isinstance(data[field], expected_type):
        raise ValidationError(
            f"Field '{field}' must be of type {expected_type.__name__}",
            details={"field": field, "expected_type": expected_type.__name__}
        )


def validate_string_length(value: str, min_length: Optional[int] = None, max_length: Optional[int] = None) -> None:
    """
    Validate string length.
    
    Args:
        value: String to validate
        min_length: Minimum length
        max_length: Maximum length
        
    Raises:
        ValidationError: If length constraints are violated
    """
    if not isinstance(value, str):
        raise ValidationError("Value must be a string")
    
    length = len(value)
    if min_length is not None and length < min_length:
        raise ValidationError(f"String must be at least {min_length} characters long")
    if max_length is not None and length > max_length:
        raise ValidationError(f"String must be at most {max_length} characters long")

