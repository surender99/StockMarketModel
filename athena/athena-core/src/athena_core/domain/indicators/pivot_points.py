"""Classic pivot points — REQ-IND-PIVOT-001."""

from __future__ import annotations

import pandas as pd


def compute_pivot_points(ohlcv: pd.DataFrame) -> pd.DataFrame:
    """Floor-trader pivot levels from prior bar HLC — REQ-IND-PIVOT-001."""
    high = ohlcv["high"].astype(float)
    low = ohlcv["low"].astype(float)
    close = ohlcv["close"].astype(float)

    prev_high = high.shift(1)
    prev_low = low.shift(1)
    prev_close = close.shift(1)
    range_hl = prev_high - prev_low

    pivot = (prev_high + prev_low + prev_close) / 3
    r1 = 2 * pivot - prev_low
    s1 = 2 * pivot - prev_high
    r2 = pivot + range_hl
    s2 = pivot - range_hl
    r3 = prev_high + 2 * (pivot - prev_low)
    s3 = prev_low - 2 * (prev_high - pivot)

    return pd.DataFrame(
        {
            "pivot": pivot,
            "r1": r1,
            "r2": r2,
            "r3": r3,
            "s1": s1,
            "s2": s2,
            "s3": s3,
        },
        index=ohlcv.index,
    )


def compute_pivot_points_from_ohlcv(df: pd.DataFrame) -> pd.DataFrame:
    """Compute classic pivot points from OHLCV DataFrame."""
    return compute_pivot_points(df)
