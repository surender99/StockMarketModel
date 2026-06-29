"""ATR indicator — REQ-IND-ATR-001."""

from __future__ import annotations

import pandas as pd


def compute_atr(ohlcv: pd.DataFrame, period: int = 14) -> pd.Series:
    """Average True Range — REQ-IND-ATR-001."""
    high = ohlcv["high"].astype(float)
    low = ohlcv["low"].astype(float)
    close = ohlcv["close"].astype(float)
    prev_close = close.shift(1)
    tr = pd.concat(
        [
            high - low,
            (high - prev_close).abs(),
            (low - prev_close).abs(),
        ],
        axis=1,
    ).max(axis=1)
    return tr.rolling(window=period, min_periods=period).mean()


def compute_atr_from_ohlcv(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """Compute ATR from OHLCV DataFrame."""
    return compute_atr(df, period=period)
