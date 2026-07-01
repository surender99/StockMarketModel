# GENERATED — DO NOT EDIT
# Source: athena-spec/schemas/dtos/*.dto.yaml
# Regenerate: make codegen

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, ClassVar

@dataclass(frozen=True, slots=True)
class QuoteSnapshot:
    """Minimal quote DTO for codegen validation — v1."""

    VERSION: ClassVar[int] = 1

    symbol: str
    price: float
    timestamp: str


DTO_REGISTRY: dict[str, type] = {
    'QuoteSnapshot': QuoteSnapshot,
}

__all__ = [
    "QuoteSnapshot",
    "DTO_REGISTRY",
]
