"""Regime indicator computations — REQ-REGIME-001."""

from __future__ import annotations

import numpy as np
import pandas as pd

from athena_core.domain.indicators.ema import compute_ema


def compute_atr(ohlcv: pd.DataFrame, period: int = 14) -> pd.Series:
    """Average True Range — REQ-REGIME-001."""
    high = ohlcv["high"].astype(float)
    low = ohlcv["low"].astype(float)
    close = ohlcv["close"].astype(float)
    prev_close = close.shift(1)
    tr = pd.concat(
        [
            high - low,
            (high - prev_close).abs(),
            (low - prev_close).abs(),
        ],
        axis=1,
    ).max(axis=1)
    return tr.rolling(window=period, min_periods=period).mean()


def compute_adx(ohlcv: pd.DataFrame, period: int = 14) -> pd.Series:
    """Average Directional Index — REQ-REGIME-001."""
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
    plus_di = 100 * pd.Series(plus_dm, index=ohlcv.index).rolling(period, min_periods=period).sum() / atr
    minus_di = 100 * pd.Series(minus_dm, index=ohlcv.index).rolling(period, min_periods=period).sum() / atr
    dx = (plus_di - minus_di).abs() / (plus_di + minus_di).replace(0, np.nan) * 100
    return dx.rolling(window=period, min_periods=period).mean()


def compute_rolling_volatility(close: pd.Series, window: int = 20) -> pd.Series:
    """Annualized rolling volatility from log returns — REQ-REGIME-001."""
    log_ret = np.log(close.astype(float) / close.astype(float).shift(1))
    return log_ret.rolling(window=window, min_periods=window).std() * np.sqrt(252)


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
