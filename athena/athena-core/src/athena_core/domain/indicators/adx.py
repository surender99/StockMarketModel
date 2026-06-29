"""ADX indicator — REQ-IND-ADX-001."""

from __future__ import annotations

import numpy as np
import pandas as pd


def compute_adx(ohlcv: pd.DataFrame, period: int = 14) -> pd.Series:
    """Average Directional Index — REQ-IND-ADX-001."""
    high = ohlcv["high"].astype(float)
    low = ohlcv["low"].astype(float)
    close = ohlcv["close"].astype(float)

    up_move = high.diff()
    down_move = -low.diff()
    plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0.0)
    minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0.0)

    prev_close = close.shift(1)
    tr = pd.concat(
        [
            high - low,
            (high - prev_close).abs(),
            (low - prev_close).abs(),
        ],
        axis=1,
    ).max(axis=1)

    atr = tr.rolling(window=period, min_periods=period).mean()
    plus_di = (
        100 * pd.Series(plus_dm, index=ohlcv.index).rolling(period, min_periods=period).sum() / atr
    )
    minus_di = (
        100 * pd.Series(minus_dm, index=ohlcv.index).rolling(period, min_periods=period).sum() / atr
    )
    dx = (plus_di - minus_di).abs() / (plus_di + minus_di).replace(0, np.nan) * 100
    return dx.rolling(window=period, min_periods=period).mean()


def compute_adx_from_ohlcv(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """Compute ADX from OHLCV DataFrame."""
    return compute_adx(df, period=period)
