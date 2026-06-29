"""Williams %R indicator — REQ-IND-WILLR-001."""

from __future__ import annotations

import pandas as pd


def compute_willr(ohlcv: pd.DataFrame, period: int = 14) -> pd.Series:
    """Williams %R — REQ-IND-WILLR-001."""
    high = ohlcv["high"].astype(float)
    low = ohlcv["low"].astype(float)
    close = ohlcv["close"].astype(float)
    highest = high.rolling(window=period, min_periods=period).max()
    lowest = low.rolling(window=period, min_periods=period).min()
    hl_range = (highest - lowest).replace(0, pd.NA)
    return -100.0 * (highest - close) / hl_range


def compute_willr_from_ohlcv(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """Compute Williams %R from OHLCV DataFrame."""
    return compute_willr(df, period=period)
