"""VWAP indicator — REQ-IND-VWAP-001."""

from __future__ import annotations

import pandas as pd


def compute_vwap(
    ohlcv: pd.DataFrame,
    *,
    anchor: str = "session",
) -> pd.Series:
    """Volume-weighted average price — REQ-IND-VWAP-001.

    When ``anchor`` is ``session`` and a ``date`` column exists, VWAP resets per session.
    Otherwise cumulative VWAP is computed over the full series.
    """
    high = ohlcv["high"].astype(float)
    low = ohlcv["low"].astype(float)
    close = ohlcv["close"].astype(float)
    volume = ohlcv["volume"].astype(float)
    typical = (high + low + close) / 3
    tp_vol = typical * volume

    if anchor == "session" and "date" in ohlcv.columns:
        session = ohlcv["date"]
        cum_tp = tp_vol.groupby(session).cumsum()
        cum_vol = volume.groupby(session).cumsum()
    else:
        cum_tp = tp_vol.cumsum()
        cum_vol = volume.cumsum()

    return cum_tp / cum_vol


def compute_vwap_from_ohlcv(
    df: pd.DataFrame,
    *,
    anchor: str = "session",
) -> pd.Series:
    """Compute VWAP from OHLCV DataFrame."""
    return compute_vwap(df, anchor=anchor)
