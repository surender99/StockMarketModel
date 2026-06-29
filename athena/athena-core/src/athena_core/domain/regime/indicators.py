"""Regime indicator computations — REQ-REGIME-001."""

from __future__ import annotations

from typing import cast

import numpy as np
import pandas as pd

from athena_core.domain.indicators.adx import compute_adx
from athena_core.domain.indicators.atr import compute_atr
from athena_core.domain.indicators.ema import compute_ema

__all__ = [
    "compute_adx",
    "compute_atr",
    "compute_regime_features",
    "compute_rolling_volatility",
]


def compute_rolling_volatility(close: pd.Series, window: int = 20) -> pd.Series:
    """Annualized rolling volatility from log returns — REQ-REGIME-001."""
    log_ret = pd.Series(
        np.log(close.astype(float) / close.astype(float).shift(1)),
        index=close.index,
    )
    vol = log_ret.rolling(window=window, min_periods=window).std() * np.sqrt(252)
    return cast(pd.Series, vol)


def compute_regime_features(
    ohlcv: pd.DataFrame,
    *,
    ema_fast_period: int = 50,
    ema_slow_period: int = 200,
    adx_period: int = 14,
    atr_period: int = 14,
    rolling_vol_window: int = 20,
) -> pd.DataFrame:
    """Build regime feature frame aligned to OHLCV dates — REQ-REGIME-001."""
    frame = ohlcv.sort_values("date").reset_index(drop=True).copy()
    close = frame["close"].astype(float)
    frame["ema_fast"] = compute_ema(close, ema_fast_period)
    frame["ema_slow"] = compute_ema(close, ema_slow_period)
    frame["adx"] = compute_adx(frame, adx_period)
    atr = compute_atr(frame, atr_period)
    frame["atr_pct"] = atr / close.replace(0, np.nan)
    frame["rolling_vol"] = compute_rolling_volatility(close, rolling_vol_window)
    return frame
