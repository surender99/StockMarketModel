"""Serialization helpers — ATH-REL-001 §07-Core-Utilities."""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import Any


def to_json_safe(value: Any) -> Any:
    """Convert common domain values into JSON-serializable primitives."""
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, dict):
        return {str(key): to_json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [to_json_safe(item) for item in value]
    if hasattr(value, "model_dump"):
        return to_json_safe(value.model_dump())
    if hasattr(value, "__dict__"):
        return to_json_safe(vars(value))
    return str(value)
