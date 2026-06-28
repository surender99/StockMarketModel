"""Pattern recognition tests — AES-0600, REQ-PAT-001, REQ-PAT-002."""

from __future__ import annotations

import pandas as pd

from athena_core.domain.patterns import PatternDetector, PatternType


def _ohlcv(rows: list[dict[str, float]]) -> pd.DataFrame:
    dates = pd.date_range("2024-01-02", periods=len(rows), freq="B").date
    return pd.DataFrame(
        {
            "date": dates,
            "open": [r["open"] for r in rows],
            "high": [r["high"] for r in rows],
            "low": [r["low"] for r in rows],
            "close": [r["close"] for r in rows],
            "volume": [r.get("volume", 1000) for r in rows],
        }
    )


def test_bullish_engulfing_detection_req_pat_001() -> None:
    df = _ohlcv(
        [
            {"open": 110, "high": 112, "low": 100, "close": 101},
            {"open": 100, "high": 115, "low": 99, "close": 114},
        ]
    )
    detector = PatternDetector()
    events = detector.detect(df, "bullish_engulfing")
    assert len(events) == 1
    assert events[0].pattern_id == "bullish_engulfing"
    assert events[0].pattern_type == PatternType.CANDLESTICK
    assert events[0].bar_index == 1


def test_hammer_detection_req_pat_001() -> None:
    df = _ohlcv(
        [
            {"open": 100, "high": 100.5, "low": 80, "close": 100.5},
        ]
    )
    events = PatternDetector().detect(df, "hammer")
    assert len(events) == 1
    assert events[0].pattern_id == "hammer"


def test_bull_flag_detection_req_pat_002() -> None:
    rows: list[dict[str, float]] = []
    price = 100.0
    for _ in range(5):
        rows.append({"open": price, "high": price + 3, "low": price - 1, "close": price + 2})
        price += 2
    for i in range(4):
        rows.append(
            {
                "open": price,
                "high": price + 0.5,
                "low": price - 0.5,
                "close": price + 0.1 * (i % 2),
            }
        )
    df = _ohlcv(rows)
    events = PatternDetector().detect(df, "bull_flag")
    assert len(events) >= 1
    assert events[-1].pattern_type == PatternType.CHART


def test_unknown_pattern_returns_empty() -> None:
    df = _ohlcv([{"open": 1, "high": 2, "low": 0.5, "close": 1.5}])
    assert PatternDetector().detect(df, "unknown") == []


def test_registered_patterns() -> None:
    names = PatternDetector().registered_patterns()
    assert "bullish_engulfing" in names
    assert "hammer" in names
    assert "bull_flag" in names
