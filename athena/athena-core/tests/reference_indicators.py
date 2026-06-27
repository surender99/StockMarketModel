"""Reference indicators for parity tests — REQ-IND-EMA-001, REQ-IND-SMA-001."""

from __future__ import annotations

import pandas as pd


def reference_ema(series: pd.Series, period: int) -> pd.Series:
    """Independent reference matching pandas-ta ``ema`` (ewm span, adjust=False)."""
    return series.ewm(span=period, adjust=False).mean()


def reference_sma(series: pd.Series, period: int) -> pd.Series:
    """Independent reference matching pandas-ta ``sma`` (rolling window)."""
    return series.rolling(window=period, min_periods=period).mean()


def pandas_ta_ema(series: pd.Series, period: int) -> pd.Series | None:
    """Return pandas-ta EMA when the library is installed."""
    try:
        import pandas_ta as ta
    except ImportError:
        return None
    return ta.ema(series, length=period)


def pandas_ta_sma(series: pd.Series, period: int) -> pd.Series | None:
    """Return pandas-ta SMA when the library is installed."""
    try:
        import pandas_ta as ta
    except ImportError:
        return None
    return ta.sma(series, length=period)
