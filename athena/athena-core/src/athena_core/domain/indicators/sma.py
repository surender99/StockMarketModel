"""SMA indicator — REQ-IND-SMA-001."""

from __future__ import annotations

from typing import overload

import pandas as pd


@overload
def compute_sma(series: pd.Series, period: int) -> pd.Series: ...


@overload
def compute_sma(series: pd.Series, period: list[int]) -> pd.DataFrame: ...


def compute_sma(
    series: pd.Series,
    period: int | list[int],
    *,
    min_periods: int | None = None,
) -> pd.Series | pd.DataFrame:
    """Vectorized SMA using rolling window — REQ-IND-SMA-001."""
    if isinstance(period, int):
        mp = min_periods if min_periods is not None else period
        return series.rolling(window=period, min_periods=mp).mean()
    out = pd.DataFrame(index=series.index)
    for p in period:
        mp = min_periods if min_periods is not None else p
        out[f"sma_{p}"] = series.rolling(window=p, min_periods=mp).mean()
    return out


def compute_sma_from_ohlcv(
    df: pd.DataFrame,
    period: int | list[int],
    price_column: str = "close",
) -> pd.Series | pd.DataFrame:
    """Compute SMA from OHLCV DataFrame."""
    return compute_sma(df[price_column], period)
