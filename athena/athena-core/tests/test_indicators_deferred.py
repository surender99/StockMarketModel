"""Tests for deferred Phase-3 indicators — Ichimoku, VWAP, ATR Bands, Pivot Points."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from athena_core.domain.features.indicator_plugins import register_builtin_indicators
from athena_core.domain.indicators.atr_bands import compute_atr_bands, compute_atr_bands_from_ohlcv
from athena_core.domain.indicators.catalog import lookup_by_aps_id
from athena_core.domain.indicators.ichimoku import compute_ichimoku, compute_ichimoku_from_ohlcv
from athena_core.domain.indicators.pivot_points import compute_pivot_points, compute_pivot_points_from_ohlcv
from athena_core.domain.indicators.vwap import compute_vwap, compute_vwap_from_ohlcv
from athena_core.domain.plugins import PluginRegistry, PluginType
from tests.reference_indicators import (
    pandas_ta_ichimoku,
    pandas_ta_vwap,
    reference_ichimoku,
    reference_pivot_points,
    reference_vwap,
)


@pytest.fixture
def ohlcv_df() -> pd.DataFrame:
    rng = np.random.default_rng(7)
    n = 200
    dates = pd.date_range("2020-01-01", periods=n, freq="B")
    close = pd.Series(100 + np.cumsum(rng.normal(0, 0.6, n)), index=dates)
    return pd.DataFrame(
        {
            "date": dates.date,
            "open": close.values,
            "high": close.values + rng.uniform(0.5, 2.0, n),
            "low": close.values - rng.uniform(0.5, 2.0, n),
            "close": close.values,
            "volume": rng.integers(500, 5000, n),
        }
    )


def test_catalog_mvp_status_for_deferred_indicators() -> None:
    """APS registry marks newly implemented indicators as MVP."""
    for aps_id in (
        "APS-IND-ICHIMOKU-001",
        "APS-IND-VWAP-001",
        "APS-IND-ATRBANDS-001",
        "APS-PRICE-PIVOT-001",
    ):
        entry = lookup_by_aps_id(aps_id)
        assert entry is not None
        assert entry.status == "MVP"


def test_builtin_plugins_include_deferred_indicators() -> None:
    registry = PluginRegistry()
    register_builtin_indicators(registry)
    ids = {p.id for p in registry.list(plugin_type=PluginType.INDICATOR, active_only=True)}
    assert {"ichimoku", "vwap", "atr_bands", "pivot_points"} <= ids


def test_ichimoku_from_ohlcv_matches_direct(ohlcv_df: pd.DataFrame) -> None:
    direct = compute_ichimoku(ohlcv_df)
    from_df = compute_ichimoku_from_ohlcv(ohlcv_df)
    pd.testing.assert_frame_equal(direct.reset_index(drop=True), from_df.reset_index(drop=True))


def test_ichimoku_reference_parity(ohlcv_df: pd.DataFrame) -> None:
    ours = compute_ichimoku(ohlcv_df)
    ref = reference_ichimoku(ohlcv_df["high"], ohlcv_df["low"], ohlcv_df["close"])
    pd.testing.assert_frame_equal(ours.reset_index(drop=True), ref.reset_index(drop=True))
    ta_ref = pandas_ta_ichimoku(ohlcv_df["high"], ohlcv_df["low"], ohlcv_df["close"])
    if ta_ref is not None:
        for col in ("tenkan", "kijun", "senkou_a", "senkou_b", "chikou"):
            valid = ours[col].notna() & ta_ref[col].notna()
            assert valid.sum() > 0
            np.testing.assert_allclose(ours.loc[valid, col], ta_ref.loc[valid, col], rtol=1e-8, atol=1e-8)


def test_vwap_session_reference_parity(ohlcv_df: pd.DataFrame) -> None:
    ours = compute_vwap(ohlcv_df, anchor="session")
    ref = reference_vwap(
        ohlcv_df["high"],
        ohlcv_df["low"],
        ohlcv_df["close"],
        ohlcv_df["volume"],
        session=ohlcv_df["date"],
    )
    pd.testing.assert_series_equal(ours.reset_index(drop=True), ref.reset_index(drop=True), check_names=False)


def test_vwap_pandas_ta_parity(ohlcv_df: pd.DataFrame) -> None:
    ours = compute_vwap_from_ohlcv(ohlcv_df, anchor="cumulative")
    ref = pandas_ta_vwap(ohlcv_df["high"], ohlcv_df["low"], ohlcv_df["close"], ohlcv_df["volume"])
    if ref is None:
        pytest.skip("pandas-ta not installed")
    valid = ours.notna() & ref.notna()
    np.testing.assert_allclose(ours.loc[valid], ref.loc[valid], rtol=1e-8, atol=1e-8)


def test_atr_bands_order_and_adapter(ohlcv_df: pd.DataFrame) -> None:
    bands = compute_atr_bands(ohlcv_df, period=20, atr_period=14, multiplier=2.0)
    valid = bands.dropna()
    assert (valid["atr_upper"] >= valid["atr_middle"]).all()
    assert (valid["atr_middle"] >= valid["atr_lower"]).all()
    from_df = compute_atr_bands_from_ohlcv(ohlcv_df, period=20, atr_period=14, multiplier=2.0)
    pd.testing.assert_frame_equal(bands.reset_index(drop=True), from_df.reset_index(drop=True))


def test_pivot_points_reference_parity(ohlcv_df: pd.DataFrame) -> None:
    ours = compute_pivot_points(ohlcv_df)
    ref = reference_pivot_points(ohlcv_df["high"], ohlcv_df["low"], ohlcv_df["close"])
    pd.testing.assert_frame_equal(
        ours.reset_index(drop=True),
        ref.reset_index(drop=True),
        check_names=False,
    )
    assert ours.iloc[0].isna().all()
    from_df = compute_pivot_points_from_ohlcv(ohlcv_df)
    pd.testing.assert_frame_equal(ours.reset_index(drop=True), from_df.reset_index(drop=True))
