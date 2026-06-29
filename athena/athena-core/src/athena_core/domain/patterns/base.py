"""Pattern recognition framework — AES-0600, REQ-PAT-001."""

from __future__ import annotations

from collections.abc import Callable

import pandas as pd

from athena_core.domain.patterns.candlestick import (
    detect_bearish_engulfing,
    detect_bullish_engulfing,
    detect_doji,
    detect_evening_star,
    detect_hammer,
    detect_inverted_hammer,
    detect_morning_star,
    detect_shooting_star,
)
from athena_core.domain.patterns.chart import (
    detect_bear_flag,
    detect_bull_flag,
    detect_double_bottom,
    detect_double_top,
)
from athena_core.domain.patterns.types import PatternEvent

PatternFn = Callable[[pd.DataFrame], list[PatternEvent]]

_BUILTIN_REGISTRY: dict[str, PatternFn] = {
    "bullish_engulfing": detect_bullish_engulfing,
    "bearish_engulfing": detect_bearish_engulfing,
    "hammer": detect_hammer,
    "inverted_hammer": detect_inverted_hammer,
    "shooting_star": detect_shooting_star,
    "doji": detect_doji,
    "morning_star": detect_morning_star,
    "evening_star": detect_evening_star,
    "bull_flag": detect_bull_flag,
    "bear_flag": detect_bear_flag,
    "double_top": detect_double_top,
    "double_bottom": detect_double_bottom,
}


def builtin_pattern_registry() -> dict[str, PatternFn]:
    """Return a copy of the built-in pattern detector registry."""
    return dict(_BUILTIN_REGISTRY)


class PatternDetector:
    """Pattern detector with registered candlestick and chart patterns."""

    def __init__(self, registry: dict[str, PatternFn] | None = None) -> None:
        self._registry = registry if registry is not None else dict(_BUILTIN_REGISTRY)

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
