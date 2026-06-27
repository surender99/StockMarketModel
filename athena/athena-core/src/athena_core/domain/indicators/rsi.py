"""RSI indicator — REQ-IND-RSI-001 (Wilder smoothing)."""

from __future__ import annotations

import pandas as pd


def compute_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    """Wilder RSI — REQ-IND-RSI-001."""
    delta = series.diff()
    gain = delta.clip(lower=0.0)
    loss = (-delta).clip(lower=0.0)
    avg_gain = gain.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    rs = avg_gain / avg_loss.replace(0, pd.NA)
    rsi = 100 - (100 / (1 + rs))
    return rsi.fillna(100.0)


def compute_rsi_from_ohlcv(
    df: pd.DataFrame,
    period: int = 14,
    price_column: str = "close",
) -> pd.Series:
    """Compute RSI from OHLCV DataFrame."""
    return compute_rsi(df[price_column], period=period)
