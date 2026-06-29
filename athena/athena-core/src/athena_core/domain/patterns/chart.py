"""Chart pattern detectors — AES-0600, REQ-PAT-002."""

from __future__ import annotations

import pandas as pd

from athena_core.domain.patterns.types import PatternEvent, PatternType


def detect_bull_flag(
    ohlcv: pd.DataFrame, *, pole_bars: int = 5, flag_bars: int = 4
) -> list[PatternEvent]:
    """Detect simplified bull flag chart pattern — REQ-PAT-002."""
    events: list[PatternEvent] = []
    min_len = pole_bars + flag_bars
    if len(ohlcv) < min_len:
        return events

    closes = ohlcv["close"].astype(float)
    for end in range(min_len - 1, len(ohlcv)):
        pole_start = end - min_len + 1
        pole_end = pole_start + pole_bars - 1
        flag_start = pole_end + 1
        flag_end = end

        pole_return = (closes.iloc[pole_end] / closes.iloc[pole_start]) - 1.0
        if pole_return < 0.03:
            continue

        flag_slice = ohlcv.iloc[flag_start : flag_end + 1]
        flag_highs = flag_slice["high"].astype(float)
        flag_lows = flag_slice["low"].astype(float)
        flag_range = float(flag_highs.max() - flag_lows.min())
        pole_range = float(
            ohlcv.iloc[pole_start : pole_end + 1]["high"].max()
            - ohlcv.iloc[pole_start : pole_end + 1]["low"].min()
        )
        if pole_range <= 0:
            continue
        if flag_range / pole_range > 0.5:
            continue

        events.append(
            PatternEvent(
                pattern_id="bull_flag",
                pattern_type=PatternType.CHART,
                bar_index=end,
                confidence=0.65,
                metadata={"pole_return": pole_return, "flag_bars": flag_bars},
            )
        )
    return events


def detect_bear_flag(
    ohlcv: pd.DataFrame, *, pole_bars: int = 5, flag_bars: int = 4
) -> list[PatternEvent]:
    """Detect simplified bear flag chart pattern — REQ-PAT-002."""
    events: list[PatternEvent] = []
    min_len = pole_bars + flag_bars
    if len(ohlcv) < min_len:
        return events

    closes = ohlcv["close"].astype(float)
    for end in range(min_len - 1, len(ohlcv)):
        pole_start = end - min_len + 1
        pole_end = pole_start + pole_bars - 1
        flag_start = pole_end + 1
        flag_end = end

        pole_return = (closes.iloc[pole_end] / closes.iloc[pole_start]) - 1.0
        if pole_return > -0.03:
            continue

        flag_slice = ohlcv.iloc[flag_start : flag_end + 1]
        flag_highs = flag_slice["high"].astype(float)
        flag_lows = flag_slice["low"].astype(float)
        flag_range = float(flag_highs.max() - flag_lows.min())
        pole_range = float(
            ohlcv.iloc[pole_start : pole_end + 1]["high"].max()
            - ohlcv.iloc[pole_start : pole_end + 1]["low"].min()
        )
        if pole_range <= 0:
            continue
        if flag_range / pole_range > 0.5:
            continue

        events.append(
            PatternEvent(
                pattern_id="bear_flag",
                pattern_type=PatternType.CHART,
                bar_index=end,
                confidence=0.65,
                metadata={"pole_return": pole_return, "flag_bars": flag_bars},
            )
        )
    return events


def detect_double_top(
    ohlcv: pd.DataFrame, *, lookback: int = 20, tolerance: float = 0.02
) -> list[PatternEvent]:
    """Detect simplified double-top chart pattern — REQ-PAT-002."""
    events: list[PatternEvent] = []
    if len(ohlcv) < lookback:
        return events
    highs = ohlcv["high"].astype(float)
    for end in range(lookback - 1, len(ohlcv)):
        window = highs.iloc[end - lookback + 1 : end + 1]
        peak_idx = window.idxmax()
        peak_val = float(window.max())
        others = window.drop(peak_idx)
        if others.empty:
            continue
        second_peak = float(others.max())
        if abs(second_peak - peak_val) / peak_val > tolerance:
            continue
        trough = float(ohlcv.iloc[end - lookback + 1 : end + 1]["low"].min())
        if float(ohlcv.iloc[end]["close"]) >= trough * 1.01:
            continue
        events.append(
            PatternEvent(
                pattern_id="double_top",
                pattern_type=PatternType.CHART,
                bar_index=end,
                confidence=0.6,
                metadata={"peak": peak_val, "trough": trough},
            )
        )
    return events


def detect_double_bottom(
    ohlcv: pd.DataFrame, *, lookback: int = 20, tolerance: float = 0.02
) -> list[PatternEvent]:
    """Detect simplified double-bottom chart pattern — REQ-PAT-002."""
    events: list[PatternEvent] = []
    if len(ohlcv) < lookback:
        return events
    lows = ohlcv["low"].astype(float)
    for end in range(lookback - 1, len(ohlcv)):
        window = lows.iloc[end - lookback + 1 : end + 1]
        trough_idx = window.idxmin()
        trough_val = float(window.min())
        others = window.drop(trough_idx)
        if others.empty:
            continue
        second_trough = float(others.min())
        if abs(second_trough - trough_val) / abs(trough_val) > tolerance:
            continue
        peak = float(ohlcv.iloc[end - lookback + 1 : end + 1]["high"].max())
        if float(ohlcv.iloc[end]["close"]) <= peak * 0.99:
            continue
        events.append(
            PatternEvent(
                pattern_id="double_bottom",
                pattern_type=PatternType.CHART,
                bar_index=end,
                confidence=0.6,
                metadata={"trough": trough_val, "peak": peak},
            )
        )
    return events
