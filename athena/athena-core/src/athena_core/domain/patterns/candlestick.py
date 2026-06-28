"""Candlestick pattern detectors — AES-0600, REQ-PAT-001."""

from __future__ import annotations

import pandas as pd

from athena_core.domain.patterns.types import PatternEvent, PatternType


def _body(row: pd.Series) -> float:
    return abs(float(row["close"]) - float(row["open"]))


def _range(row: pd.Series) -> float:
    return float(row["high"]) - float(row["low"])


def detect_bullish_engulfing(ohlcv: pd.DataFrame) -> list[PatternEvent]:
    """Detect bullish engulfing candlestick — REQ-PAT-001."""
    events: list[PatternEvent] = []
    if len(ohlcv) < 2:
        return events
    for i in range(1, len(ohlcv)):
        prev = ohlcv.iloc[i - 1]
        curr = ohlcv.iloc[i]
        prev_bearish = float(prev["close"]) < float(prev["open"])
        curr_bullish = float(curr["close"]) > float(curr["open"])
        if not (prev_bearish and curr_bullish):
            continue
        prev_body_low = min(float(prev["open"]), float(prev["close"]))
        prev_body_high = max(float(prev["open"]), float(prev["close"]))
        curr_body_low = min(float(curr["open"]), float(curr["close"]))
        curr_body_high = max(float(curr["open"]), float(curr["close"]))
        if curr_body_low <= prev_body_low and curr_body_high >= prev_body_high:
            events.append(
                PatternEvent(
                    pattern_id="bullish_engulfing",
                    pattern_type=PatternType.CANDLESTICK,
                    bar_index=i,
                    confidence=0.8,
                    metadata={
                        "prev_close": float(prev["close"]),
                        "curr_close": float(curr["close"]),
                    },
                )
            )
    return events


def detect_doji(ohlcv: pd.DataFrame, *, body_ratio_max: float = 0.1) -> list[PatternEvent]:
    """Detect doji candlestick — REQ-PAT-001."""
    events: list[PatternEvent] = []
    for i in range(len(ohlcv)):
        row = ohlcv.iloc[i]
        bar_range = _range(row)
        if bar_range <= 0:
            continue
        body = _body(row)
        if body / bar_range <= body_ratio_max:
            events.append(
                PatternEvent(
                    pattern_id="doji",
                    pattern_type=PatternType.CANDLESTICK,
                    bar_index=i,
                    confidence=0.7,
                    metadata={"body_ratio": body / bar_range},
                )
            )
    return events


def detect_morning_star(ohlcv: pd.DataFrame) -> list[PatternEvent]:
    """Detect morning star three-candle reversal — REQ-PAT-001."""
    events: list[PatternEvent] = []
    if len(ohlcv) < 3:
        return events
    for i in range(2, len(ohlcv)):
        first = ohlcv.iloc[i - 2]
        middle = ohlcv.iloc[i - 1]
        third = ohlcv.iloc[i]
        first_bearish = float(first["close"]) < float(first["open"])
        third_bullish = float(third["close"]) > float(third["open"])
        if not (first_bearish and third_bullish):
            continue
        middle_body = _body(middle)
        middle_range = _range(middle)
        if middle_range <= 0:
            continue
        if middle_body / middle_range > 0.35:
            continue
        if float(middle["close"]) >= float(first["close"]):
            continue
        if float(third["close"]) <= float(first["open"]):
            continue
        midpoint = (float(first["open"]) + float(first["close"])) / 2.0
        if float(third["close"]) < midpoint:
            continue
        events.append(
            PatternEvent(
                pattern_id="morning_star",
                pattern_type=PatternType.CANDLESTICK,
                bar_index=i,
                confidence=0.85,
                metadata={
                    "first_close": float(first["close"]),
                    "third_close": float(third["close"]),
                },
            )
        )
    return events


def detect_hammer(ohlcv: pd.DataFrame) -> list[PatternEvent]:
    """Detect hammer candlestick — REQ-PAT-001."""
    events: list[PatternEvent] = []
    for i in range(len(ohlcv)):
        row = ohlcv.iloc[i]
        bar_range = _range(row)
        if bar_range <= 0:
            continue
        body = _body(row)
        open_p, close_p = float(row["open"]), float(row["close"])
        high_p, low_p = float(row["high"]), float(row["low"])
        body_top = max(open_p, close_p)
        body_bottom = min(open_p, close_p)
        upper_shadow = high_p - body_top
        lower_shadow = body_bottom - low_p
        if body <= 0:
            continue
        if lower_shadow >= 2.0 * body and upper_shadow <= body * 0.5:
            events.append(
                PatternEvent(
                    pattern_id="hammer",
                    pattern_type=PatternType.CANDLESTICK,
                    bar_index=i,
                    confidence=0.75,
                    metadata={"lower_shadow": lower_shadow, "body": body},
                )
            )
    return events
