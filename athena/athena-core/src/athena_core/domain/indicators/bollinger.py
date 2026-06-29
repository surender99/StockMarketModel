"""Bollinger Bands indicator — REQ-IND-BOLLINGER-001."""

from __future__ import annotations

import pandas as pd

from athena_core.domain.indicators.sma import compute_sma


def compute_bollinger(
    series: pd.Series,
    period: int = 20,
    std_dev: float = 2.0,
) -> pd.DataFrame:
    """Bollinger upper, middle, and lower bands — REQ-IND-BOLLINGER-001."""
    middle = compute_sma(series, period)
    rolling_std = series.astype(float).rolling(window=period, min_periods=period).std()
    upper = middle + std_dev * rolling_std
    lower = middle - std_dev * rolling_std
    return pd.DataFrame(
        {
            "bb_upper": upper,
            "bb_middle": middle,
            "bb_lower": lower,
        },
        index=series.index,
    )


def compute_bollinger_from_ohlcv(
    df: pd.DataFrame,
    period: int = 20,
    std_dev: float = 2.0,
    price_column: str = "close",
) -> pd.DataFrame:
    """Compute Bollinger Bands from OHLCV DataFrame."""
    return compute_bollinger(df[price_column], period=period, std_dev=std_dev)
