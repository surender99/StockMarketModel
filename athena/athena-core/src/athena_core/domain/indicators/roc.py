"""ROC indicator — REQ-IND-ROC-001."""

from __future__ import annotations

import pandas as pd


def compute_roc(series: pd.Series, period: int = 12) -> pd.Series:
    """Rate of change (percent) — REQ-IND-ROC-001."""
    prices = series.astype(float)
    return ((prices / prices.shift(period)) - 1.0) * 100.0


def compute_roc_from_ohlcv(
    df: pd.DataFrame,
    period: int = 12,
    price_column: str = "close",
) -> pd.Series:
    """Compute ROC from OHLCV DataFrame."""
    return compute_roc(df[price_column], period=period)
