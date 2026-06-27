"""Pattern framework stub tests — AES-0600."""

from __future__ import annotations

import pandas as pd

from athena_core.domain.patterns import PatternDetector


def test_pattern_detector_returns_empty_stub() -> None:
    df = pd.DataFrame(
        {
            "date": pd.date_range("2024-01-01", periods=5, freq="B").date,
            "open": [1, 2, 3, 4, 5],
            "high": [2, 3, 4, 5, 6],
            "low": [0, 1, 2, 3, 4],
            "close": [1.5, 2.5, 3.5, 4.5, 5.5],
            "volume": [100] * 5,
        }
    )
    detector = PatternDetector()
    assert detector.detect(df, "bull_flag") == []
