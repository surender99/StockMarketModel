"""Tests for Bollinger Bands — REQ-IND-BOLLINGER-001."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from athena_core.domain.indicators.bollinger import compute_bollinger, compute_bollinger_from_ohlcv
from athena_core.domain.indicators.sma import compute_sma


@pytest.fixture
def price_series() -> pd.Series:
    rng = np.random.default_rng(3)
    return pd.Series(100 + np.cumsum(rng.normal(0, 0.5, 120)))


@pytest.fixture
def ohlcv_df(price_series: pd.Series) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "date": pd.date_range("2020-01-01", periods=len(price_series), freq="B").date,
            "open": price_series.values,
            "high": price_series.values + 1,
            "low": price_series.values - 1,
            "close": price_series.values,
            "volume": 1000,
        }
    )


def test_bollinger_band_order(price_series: pd.Series) -> None:
    bands = compute_bollinger(price_series, period=20, std_dev=2.0)
    valid = bands.dropna()
    assert (valid["bb_upper"] >= valid["bb_middle"]).all()
    assert (valid["bb_middle"] >= valid["bb_lower"]).all()


def test_bollinger_middle_matches_sma(price_series: pd.Series) -> None:
    bands = compute_bollinger(price_series, period=20)
    sma = compute_sma(price_series, 20)
    pd.testing.assert_series_equal(
        bands["bb_middle"].reset_index(drop=True),
        sma.reset_index(drop=True),
        check_names=False,
    )


def test_bollinger_from_ohlcv(ohlcv_df: pd.DataFrame) -> None:
    direct = compute_bollinger(ohlcv_df["close"], period=20)
    from_df = compute_bollinger_from_ohlcv(ohlcv_df, period=20)
    pd.testing.assert_frame_equal(direct.reset_index(drop=True), from_df.reset_index(drop=True))
