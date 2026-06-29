"""Tests for ADX indicator — REQ-IND-ADX-001."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from athena_core.domain.indicators.adx import compute_adx, compute_adx_from_ohlcv


@pytest.fixture
def ohlcv_df() -> pd.DataFrame:
    rng = np.random.default_rng(7)
    dates = pd.date_range("2020-01-01", periods=200, freq="B")
    close = pd.Series(100 + np.cumsum(rng.normal(0, 1, 200)), index=dates)
    return pd.DataFrame(
        {
            "date": dates.date,
            "open": close.values,
            "high": close.values + rng.uniform(0.5, 2, 200),
            "low": close.values - rng.uniform(0.5, 2, 200),
            "close": close.values,
            "volume": 1000,
        }
    )


def test_adx_bounded_zero_to_hundred(ohlcv_df: pd.DataFrame) -> None:
    result = compute_adx(ohlcv_df, period=14)
    valid = result.dropna()
    assert (valid >= 0).all()
    assert (valid <= 100).all()


def test_adx_from_ohlcv_matches_direct(ohlcv_df: pd.DataFrame) -> None:
    direct = compute_adx(ohlcv_df, 14)
    from_df = compute_adx_from_ohlcv(ohlcv_df, 14)
    pd.testing.assert_series_equal(direct.reset_index(drop=True), from_df.reset_index(drop=True))
