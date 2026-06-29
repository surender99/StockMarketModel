"""OBV indicator — REQ-IND-OBV-001."""

from __future__ import annotations

import pandas as pd


def compute_obv(ohlcv: pd.DataFrame) -> pd.Series:
    """On-Balance Volume — REQ-IND-OBV-001."""
    close = ohlcv["close"].astype(float)
    volume = ohlcv["volume"].astype(float)
    direction = close.diff().fillna(0.0).apply(lambda x: 1.0 if x > 0 else (-1.0 if x < 0 else 0.0))
    return (volume * direction).cumsum()


def compute_obv_from_ohlcv(df: pd.DataFrame) -> pd.Series:
    """Compute OBV from OHLCV DataFrame."""
    return compute_obv(df)
