"""Pattern types — AES-0600."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any


class PatternType(StrEnum):
    """Pattern categories — Package 06."""

    CANDLESTICK = "candlestick"
    CHART = "chart"


@dataclass(frozen=True)
class PatternEvent:
    """Detected pattern occurrence."""

    pattern_id: str
    pattern_type: PatternType
    bar_index: int
    confidence: float
    metadata: dict[str, Any]
