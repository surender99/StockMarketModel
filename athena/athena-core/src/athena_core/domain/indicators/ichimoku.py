"""Ichimoku Cloud indicator — REQ-IND-ICHIMOKU-001."""

from __future__ import annotations

import pandas as pd


def _midprice(high: pd.Series, low: pd.Series, period: int) -> pd.Series:
    return (high.rolling(window=period, min_periods=period).max() + low.rolling(window=period, min_periods=period).min()) / 2


def compute_ichimoku(
    ohlcv: pd.DataFrame,
    tenkan_period: int = 9,
    kijun_period: int = 26,
    senkou_period: int = 52,
    displacement: int = 26,
) -> pd.DataFrame:
    """Ichimoku Cloud lines — REQ-IND-ICHIMOKU-001."""
    high = ohlcv["high"].astype(float)
    low = ohlcv["low"].astype(float)
    close = ohlcv["close"].astype(float)

    tenkan = _midprice(high, low, tenkan_period)
    kijun = _midprice(high, low, kijun_period)
    senkou_a = ((tenkan + kijun) / 2).shift(displacement)
    senkou_b = _midprice(high, low, senkou_period).shift(displacement)
    chikou = close.shift(-displacement)

    return pd.DataFrame(
        {
            "tenkan": tenkan,
            "kijun": kijun,
            "senkou_a": senkou_a,
            "senkou_b": senkou_b,
            "chikou": chikou,
        },
        index=ohlcv.index,
    )


def compute_ichimoku_from_ohlcv(
    df: pd.DataFrame,
    tenkan_period: int = 9,
    kijun_period: int = 26,
    senkou_period: int = 52,
    displacement: int = 26,
) -> pd.DataFrame:
    """Compute Ichimoku Cloud from OHLCV DataFrame."""
    return compute_ichimoku(
        df,
        tenkan_period=tenkan_period,
        kijun_period=kijun_period,
        senkou_period=senkou_period,
        displacement=displacement,
    )
