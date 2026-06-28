"""Stochastic oscillator — REQ-IND-STOCH-001."""

from __future__ import annotations

import pandas as pd

from athena_core.domain.indicators.sma import compute_sma


def compute_stochastic(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    *,
    k_period: int = 14,
    d_period: int = 3,
) -> pd.DataFrame:
    """Stochastic %K and %D — REQ-IND-STOCH-001."""
    lowest_low = low.rolling(window=k_period, min_periods=k_period).min()
    highest_high = high.rolling(window=k_period, min_periods=k_period).max()
    span = (highest_high - lowest_low).replace(0, pd.NA)
    stoch_k = ((close - lowest_low) / span) * 100.0
    stoch_d = compute_sma(stoch_k, d_period)
    return pd.DataFrame({"stoch_k": stoch_k, "stoch_d": stoch_d})


def compute_stoch_from_ohlcv(
    df: pd.DataFrame,
    *,
    k_period: int = 14,
    d_period: int = 3,
) -> pd.DataFrame:
    """Compute stochastic from OHLCV DataFrame."""
    return compute_stochastic(
        df["high"].astype(float),
        df["low"].astype(float),
        df["close"].astype(float),
        k_period=k_period,
        d_period=d_period,
    )
