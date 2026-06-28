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


def pandas_ta_rsi(series: pd.Series, period: int) -> pd.Series | None:
    """Return pandas-ta RSI when the library is installed."""
    try:
        import pandas_ta as ta
    except ImportError:
        return None
    return ta.rsi(series, length=period)


def pandas_ta_macd(
    series: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9
) -> pd.DataFrame | None:
    """Return pandas-ta MACD when the library is installed."""
    try:
        import pandas_ta as ta
    except ImportError:
        return None
    result = ta.macd(series, fast=fast, slow=slow, signal=signal)
    if result is None:
        return None
    cols = result.columns.tolist()
    return pd.DataFrame(
        {
            "macd": result[cols[0]],
            "histogram": result[cols[1]],
            "signal": result[cols[2]],
        },
        index=series.index,
    )


def pandas_ta_stoch(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    k_period: int = 14,
    d_period: int = 3,
) -> pd.DataFrame | None:
    """Return pandas-ta stochastic when the library is installed."""
    try:
        import pandas_ta as ta
    except ImportError:
        return None
    result = ta.stoch(high, low, close, k=k_period, d=d_period)
    if result is None:
        return None
    cols = result.columns.tolist()
    return pd.DataFrame(
        {
            "stoch_k": result[cols[0]],
            "stoch_d": result[cols[1]],
        },
        index=close.index,
    )
