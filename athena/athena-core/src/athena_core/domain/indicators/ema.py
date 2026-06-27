"""EMA indicator — REQ-IND-EMA-001."""

from __future__ import annotations

from typing import overload

import pandas as pd


@overload
def compute_ema(series: pd.Series, period: int) -> pd.Series: ...


@overload
def compute_ema(series: pd.Series, period: list[int]) -> pd.DataFrame: ...


def compute_ema(
    series: pd.Series,
    period: int | list[int],
    *,
    price_column: str | None = None,
    ohlcv: pd.DataFrame | None = None,
) -> pd.Series | pd.DataFrame:
    """Vectorized EMA using ``ewm(span=period, adjust=False)`` — REQ-IND-EMA-001."""
    prices = _resolve_prices(series, price_column=price_column, ohlcv=ohlcv)
    if isinstance(period, int):
        return prices.ewm(span=period, adjust=False).mean()
    out = pd.DataFrame(index=prices.index)
    for p in period:
        out[f"ema_{p}"] = prices.ewm(span=p, adjust=False).mean()
    return out


def compute_ema_from_ohlcv(
    df: pd.DataFrame,
    period: int | list[int],
    price_column: str = "close",
) -> pd.Series | pd.DataFrame:
    """Compute EMA from OHLCV DataFrame."""
    return compute_ema(df[price_column], period)


def _resolve_prices(
    series: pd.Series,
    *,
    price_column: str | None,
    ohlcv: pd.DataFrame | None,
) -> pd.Series:
    if ohlcv is not None and price_column is not None:
        return ohlcv[price_column]
    return series
