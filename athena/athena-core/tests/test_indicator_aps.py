"""Indicator APS tests — PHASE-3 Indicators."""

from __future__ import annotations

import time

import numpy as np
import pandas as pd

from athena_core.domain.indicators.catalog import INDICATOR_CATALOG, list_mvp_indicators, lookup_indicator_aps
from athena_core.domain.indicators.ema import compute_ema_from_ohlcv


def _ohlcv(n: int = 500) -> pd.DataFrame:
    dates = pd.date_range("2020-01-01", periods=n, freq="B")
    close = pd.Series(100 + np.arange(n) * 0.1, index=dates)
    return pd.DataFrame(
        {
            "date": dates.date,
            "open": close.values,
            "high": close.values + 1,
            "low": close.values - 1,
            "close": close.values,
            "volume": 1000 + np.arange(n),
        }
    )


def test_indicator_catalog_maps_mvp_plugins() -> None:
    """APS-IND-REGISTRY-001 — catalog covers all MVP builtin indicators."""
    mvp = list_mvp_indicators()
    assert len(mvp) == 19
    assert lookup_indicator_aps("ema") is not None
    assert lookup_indicator_aps("ema").aps_id == "APS-IND-EMA-001"


def test_indicator_catalog_unique_aps_ids() -> None:
    """APS-IND-ARCH-001 — each MVP indicator has a distinct APS id."""
    aps_ids = [e.aps_id for e in INDICATOR_CATALOG]
    assert len(aps_ids) == len(set(aps_ids))


def test_ema_10k_bars_under_benchmark() -> None:
    """APS-IND-EMA-001 — EMA 10k bars < 50 ms (ATHENA/Benchmarks/indicators.md)."""
    df = _ohlcv(10_000)
    start = time.perf_counter()
    result = compute_ema_from_ohlcv(df, 20)
    elapsed_ms = (time.perf_counter() - start) * 1000
    assert len(result) == len(df)
    assert elapsed_ms < 50
