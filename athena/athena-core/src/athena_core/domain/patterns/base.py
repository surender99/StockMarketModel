"""Pattern recognition framework stub — AES-0600, REQ-PAT-001."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

import pandas as pd


class PatternType(str, Enum):
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


class PatternDetector:
    """Stub pattern detector — implementations deferred to Package 06 backlog."""

    def detect(self, ohlcv: pd.DataFrame, pattern_id: str) -> list[PatternEvent]:
        """Return empty list until pattern plugins are implemented."""
        _ = ohlcv, pattern_id
        return []
