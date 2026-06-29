"""MFI indicator — REQ-IND-MFI-001."""

from __future__ import annotations

import pandas as pd


def compute_mfi(ohlcv: pd.DataFrame, period: int = 14) -> pd.Series:
    """Money Flow Index — REQ-IND-MFI-001."""
    high = ohlcv["high"].astype(float)
    low = ohlcv["low"].astype(float)
    close = ohlcv["close"].astype(float)
    volume = ohlcv["volume"].astype(float)
    typical = (high + low + close) / 3.0
    raw_flow = typical * volume
    delta = typical.diff()
    pos_flow = raw_flow.where(delta > 0, 0.0)
    neg_flow = raw_flow.where(delta < 0, 0.0)
    pos_sum = pos_flow.rolling(window=period, min_periods=period).sum()
    neg_sum = neg_flow.rolling(window=period, min_periods=period).sum()
    ratio = pos_sum / neg_sum.replace(0, pd.NA)
    return 100.0 - (100.0 / (1.0 + ratio))


def compute_mfi_from_ohlcv(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """Compute MFI from OHLCV DataFrame."""
    return compute_mfi(df, period=period)
