"""WMA indicator — REQ-IND-WMA-001."""

from __future__ import annotations

import pandas as pd


def compute_wma(series: pd.Series, period: int) -> pd.Series:
    """Weighted moving average — REQ-IND-WMA-001."""
    weights = pd.Series(range(1, period + 1), dtype=float)

    def _wma(window: pd.Series) -> float:
        return float((window.values * weights.values).sum() / weights.sum())

    return series.astype(float).rolling(window=period, min_periods=period).apply(_wma, raw=False)


def compute_wma_from_ohlcv(
    df: pd.DataFrame,
    period: int,
    price_column: str = "close",
) -> pd.Series:
    """Compute WMA from OHLCV DataFrame."""
    return compute_wma(df[price_column], period)
