"""MACD indicator — REQ-IND-MACD-001."""

from __future__ import annotations

import pandas as pd

from athena_core.domain.indicators.ema import compute_ema


def compute_macd(
    series: pd.Series,
    fast: int = 12,
    slow: int = 26,
    signal: int = 9,
) -> pd.DataFrame:
    """MACD line, signal line, and histogram — REQ-IND-MACD-001."""
    fast_ema = compute_ema(series, fast)
    slow_ema = compute_ema(series, slow)
    macd_line = fast_ema - slow_ema
    signal_line = compute_ema(macd_line, signal)
    histogram = macd_line - signal_line
    return pd.DataFrame(
        {
            "macd": macd_line,
            "signal": signal_line,
            "histogram": histogram,
        },
        index=series.index,
    )


def compute_macd_from_ohlcv(
    df: pd.DataFrame,
    fast: int = 12,
    slow: int = 26,
    signal: int = 9,
    price_column: str = "close",
) -> pd.DataFrame:
    """Compute MACD from OHLCV DataFrame."""
    return compute_macd(df[price_column], fast=fast, slow=slow, signal=signal)
