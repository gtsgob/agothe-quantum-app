"""
Validation utilities
"""

from typing import Any, List, Tuple

def validate_range(value: float, min_val: float = 0.0, max_val: float = 1.0,
                   name: str = "value") -> None:
    """
    Validate that a value is within specified range

    Args:
        value: Value to validate
        min_val: Minimum allowed value
        max_val: Maximum allowed value
        name: Name of the value (for error messages)

    Raises:
        ValueError: If value is outside range
    """
    if not min_val <= value <= max_val:
        raise ValueError(
            f"{name} must be between {min_val} and {max_val}, got {value}"
        )

def validate_positive(value: float, name: str = "value") -> None:
    """
    Validate that a value is positive

    Args:
        value: Value to validate
        name: Name of the value (for error messages)

    Raises:
        ValueError: If value is not positive
    """
    if value < 0:
        raise ValueError(f"{name} must be positive, got {value}")

def validate_required_fields(obj: Any, required_fields: List[str]) -> None:
    """
    Validate that an object has all required fields

    Args:
        obj: Object to validate
        required_fields: List of required field names

    Raises:
        ValueError: If any required field is missing
    """
    missing = []
    for field in required_fields:
        if not hasattr(obj, field) or getattr(obj, field) is None:
            missing.append(field)

    if missing:
        raise ValueError(f"Missing required fields: {', '.join(missing)}")
