"""CCI indicator — REQ-IND-CCI-001."""

from __future__ import annotations

import pandas as pd


def compute_cci(ohlcv: pd.DataFrame, period: int = 20) -> pd.Series:
    """Commodity Channel Index — REQ-IND-CCI-001."""
    high = ohlcv["high"].astype(float)
    low = ohlcv["low"].astype(float)
    close = ohlcv["close"].astype(float)
    typical = (high + low + close) / 3.0
    sma = typical.rolling(window=period, min_periods=period).mean()
    mean_dev = typical.rolling(window=period, min_periods=period).apply(
        lambda x: abs(x - x.mean()).mean(), raw=True
    )
    return (typical - sma) / (0.015 * mean_dev)


def compute_cci_from_ohlcv(df: pd.DataFrame, period: int = 20) -> pd.Series:
    """Compute CCI from OHLCV DataFrame."""
    return compute_cci(df, period=period)
