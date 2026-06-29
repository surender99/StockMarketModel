"""CMF indicator — REQ-IND-CMF-001."""

from __future__ import annotations

import pandas as pd


def compute_cmf(ohlcv: pd.DataFrame, period: int = 20) -> pd.Series:
    """Chaikin Money Flow — REQ-IND-CMF-001."""
    high = ohlcv["high"].astype(float)
    low = ohlcv["low"].astype(float)
    close = ohlcv["close"].astype(float)
    volume = ohlcv["volume"].astype(float)
    hl_range = (high - low).replace(0, pd.NA)
    mfm = ((close - low) - (high - close)) / hl_range
    mfv = mfm * volume
    return mfv.rolling(window=period, min_periods=period).sum() / volume.rolling(
        window=period, min_periods=period
    ).sum()


def compute_cmf_from_ohlcv(df: pd.DataFrame, period: int = 20) -> pd.Series:
    """Compute CMF from OHLCV DataFrame."""
    return compute_cmf(df, period=period)
