"""Pattern signal time series — AES-0600."""

from __future__ import annotations

import pandas as pd

from athena_core.domain.patterns.base import PatternDetector
from athena_core.domain.patterns.types import PatternEvent


def events_to_frame(ohlcv: pd.DataFrame, events: list[PatternEvent]) -> pd.DataFrame:
    """Convert pattern events to per-bar signal and confidence columns."""
    signal = [0.0] * len(ohlcv)
    confidence = [0.0] * len(ohlcv)
    for event in events:
        if 0 <= event.bar_index < len(ohlcv):
            signal[event.bar_index] = 1.0
            confidence[event.bar_index] = max(confidence[event.bar_index], event.confidence)
    return pd.DataFrame(
        {
            "date": ohlcv["date"].values,
            "signal": signal,
            "confidence": confidence,
        }
    )


def compute_pattern_series(
    ohlcv: pd.DataFrame,
    pattern_id: str,
    *,
    detector: PatternDetector | None = None,
) -> pd.DataFrame:
    """Build cached feature frame for a single pattern."""
    det = detector or PatternDetector()
    events = det.detect(ohlcv, pattern_id)
    return events_to_frame(ohlcv, events)
