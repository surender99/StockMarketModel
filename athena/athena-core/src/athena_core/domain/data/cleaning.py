"""OHLCV cleaning and normalization — REQ-DATA-CLEAN-001, ATH-REL-002 §07."""

from __future__ import annotations

import pandas as pd


def clean_ohlcv_frame(
    df: pd.DataFrame,
    *,
    drop_na_ohlc: bool = True,
    sort_by_date: bool = True,
) -> pd.DataFrame:
    """Normalize ingested OHLCV without silent price correction."""
    if df.empty:
        return df.copy()

    out = df.copy()
    if sort_by_date and "date" in out.columns:
        out = out.sort_values("date").reset_index(drop=True)

    if drop_na_ohlc:
        ohlc_cols = [c for c in ("open", "high", "low", "close") if c in out.columns]
        if ohlc_cols:
            out = out.dropna(subset=ohlc_cols)

    if "date" in out.columns:
        dup_count = int(out.duplicated(subset=["date"]).sum())
        if dup_count > 0:
            out = out.drop_duplicates(subset=["date"], keep="last").reset_index(drop=True)

    return out.reset_index(drop=True)
