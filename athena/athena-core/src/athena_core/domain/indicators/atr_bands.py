"""ATR Bands indicator — REQ-IND-ATRBANDS-001."""

from __future__ import annotations

import pandas as pd

from athena_core.domain.indicators.atr import compute_atr
from athena_core.domain.indicators.ema import compute_ema


def compute_atr_bands(
    ohlcv: pd.DataFrame,
    period: int = 20,
    atr_period: int = 14,
    multiplier: float = 2.0,
    price_column: str = "close",
) -> pd.DataFrame:
    """ATR envelope bands around an EMA center — REQ-IND-ATRBANDS-001."""
    close = ohlcv[price_column].astype(float)
    middle = compute_ema(close, period)
    atr = compute_atr(ohlcv, period=atr_period)
    offset = multiplier * atr
    return pd.DataFrame(
        {
            "atr_upper": middle + offset,
            "atr_middle": middle,
            "atr_lower": middle - offset,
        },
        index=ohlcv.index,
    )


def compute_atr_bands_from_ohlcv(
    df: pd.DataFrame,
    period: int = 20,
    atr_period: int = 14,
    multiplier: float = 2.0,
    price_column: str = "close",
) -> pd.DataFrame:
    """Compute ATR Bands from OHLCV DataFrame."""
    return compute_atr_bands(
        df,
        period=period,
        atr_period=atr_period,
        multiplier=multiplier,
        price_column=price_column,
    )
