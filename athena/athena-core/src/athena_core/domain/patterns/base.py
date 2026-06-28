"""Pattern recognition framework — AES-0600, REQ-PAT-001."""

from __future__ import annotations

from collections.abc import Callable

import pandas as pd

from athena_core.domain.patterns.candlestick import detect_bullish_engulfing, detect_hammer
from athena_core.domain.patterns.chart import detect_bull_flag
from athena_core.domain.patterns.types import PatternEvent

PatternFn = Callable[[pd.DataFrame], list[PatternEvent]]

_REGISTRY: dict[str, PatternFn] = {
    "bullish_engulfing": detect_bullish_engulfing,
    "hammer": detect_hammer,
    "bull_flag": detect_bull_flag,
}


class PatternDetector:
    """Pattern detector with registered candlestick and chart patterns."""

    def __init__(self, registry: dict[str, PatternFn] | None = None) -> None:
        self._registry = registry if registry is not None else dict(_REGISTRY)

    def registered_patterns(self) -> list[str]:
        return sorted(self._registry.keys())

    def detect(self, ohlcv: pd.DataFrame, pattern_id: str) -> list[PatternEvent]:
        """Detect occurrences of *pattern_id* in OHLCV bars."""
        fn = self._registry.get(pattern_id)
        if fn is None:
            return []
        return fn(ohlcv)

    def detect_all(self, ohlcv: pd.DataFrame) -> list[PatternEvent]:
        """Run all registered pattern detectors."""
        events: list[PatternEvent] = []
        for pattern_id in self._registry:
            events.extend(self.detect(ohlcv, pattern_id))
        return events
