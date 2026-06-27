"""Tests for SMA indicator — REQ-IND-SMA-001."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from athena_core.domain.indicators.sma import compute_sma, compute_sma_from_ohlcv
from tests.reference_indicators import pandas_ta_sma, reference_sma


@pytest.fixture
def price_series() -> pd.Series:
    rng = np.random.default_rng(7)
    prices = 50 + np.cumsum(rng.normal(0, 0.5, 300))
    return pd.Series(prices, index=pd.date_range("2021-01-01", periods=300, freq="B"))


@pytest.mark.parametrize("period", [20, 50, 200])
def test_sma_reference_parity(price_series: pd.Series, period: int) -> None:
    ours = compute_sma(price_series, period)
    ref = reference_sma(price_series, period)
    pd.testing.assert_series_equal(ours, ref, check_names=False, rtol=1e-6, atol=1e-6)


@pytest.mark.parametrize("period", [20, 50, 200])
def test_sma_pandas_ta_parity_when_available(price_series: pd.Series, period: int) -> None:
    ta_result = pandas_ta_sma(price_series, period)
    if ta_result is None:
        pytest.skip("pandas-ta not installed")
    ours = compute_sma(price_series, period)
    pd.testing.assert_series_equal(ours, ta_result, check_names=False, rtol=1e-6, atol=1e-6)


def test_sma_warmup_nan(price_series: pd.Series) -> None:
    result = compute_sma(price_series, 20)
    assert result.iloc[:19].isna().all()
    assert not pd.isna(result.iloc[19])


def test_sma_period_exceeds_length() -> None:
    short = pd.Series([1.0, 2.0, 3.0])
    result = compute_sma(short, 10)
    assert result.isna().all()


def test_sma_multi_period_shape(price_series: pd.Series) -> None:
    result = compute_sma(price_series, [20, 50, 200])
    assert list(result.columns) == ["sma_20", "sma_50", "sma_200"]


def test_sma_from_ohlcv(price_series: pd.Series) -> None:
    df = pd.DataFrame({"close": price_series, "date": price_series.index.date})
    direct = compute_sma(price_series, 20)
    from_df = compute_sma_from_ohlcv(df, 20)
    pd.testing.assert_series_equal(
        direct.reset_index(drop=True), from_df.reset_index(drop=True), check_names=False
    )
