"""Tests for EMA indicator — REQ-IND-EMA-001."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from athena_core.domain.indicators.ema import compute_ema, compute_ema_from_ohlcv
from tests.reference_indicators import pandas_ta_ema, reference_ema


@pytest.fixture
def price_series() -> pd.Series:
    rng = np.random.default_rng(42)
    prices = 100 + np.cumsum(rng.normal(0, 1, 500))
    return pd.Series(prices, index=pd.date_range("2020-01-01", periods=500, freq="B"))


@pytest.fixture
def ohlcv_df(price_series: pd.Series) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "date": price_series.index.date,
            "open": price_series.values,
            "high": price_series.values + 1,
            "low": price_series.values - 1,
            "close": price_series.values,
            "volume": 1000,
        }
    )


@pytest.mark.parametrize("period", [9, 21, 50])
def test_ema_reference_parity(price_series: pd.Series, period: int) -> None:
    ours = compute_ema(price_series, period)
    ref = reference_ema(price_series, period)
    pd.testing.assert_series_equal(ours, ref, check_names=False, rtol=1e-6, atol=1e-6)


@pytest.mark.parametrize("period", [9, 21, 50])
def test_ema_pandas_ta_parity_when_available(price_series: pd.Series, period: int) -> None:
    ta_result = pandas_ta_ema(price_series, period)
    if ta_result is None:
        pytest.skip("pandas-ta not installed")
    ours = compute_ema(price_series, period)
    pd.testing.assert_series_equal(ours, ta_result, check_names=False, rtol=1e-6, atol=1e-6)


def test_ema_warmup_not_zero_filled(price_series: pd.Series) -> None:
    result = compute_ema(price_series, 21)
    assert not (result.iloc[:21] == 0).any()
    ref = reference_ema(price_series, 21)
    pd.testing.assert_series_equal(result.iloc[:21], ref.iloc[:21], check_names=False)


def test_ema_multi_period_columns(price_series: pd.Series) -> None:
    result = compute_ema(price_series, [9, 21])
    assert list(result.columns) == ["ema_9", "ema_21"]
    assert len(result) == len(price_series)


def test_ema_empty_series() -> None:
    empty = pd.Series(dtype=float)
    result = compute_ema(empty, 9)
    assert len(result) == 0


def test_ema_single_bar() -> None:
    one = pd.Series([100.0])
    result = compute_ema(one, 9)
    assert len(result) == 1


def test_ema_from_ohlcv(ohlcv_df: pd.DataFrame) -> None:
    close = ohlcv_df["close"]
    direct = compute_ema(close, 21)
    from_df = compute_ema_from_ohlcv(ohlcv_df, 21)
    pd.testing.assert_series_equal(direct.reset_index(drop=True), from_df.reset_index(drop=True))


def test_ema_large_series_performance() -> None:
    rng = np.random.default_rng(0)
    prices = pd.Series(rng.random(10_000) + 100)
    result = compute_ema(prices, [9, 21, 50, 200])
    assert result.shape == (10_000, 4)
