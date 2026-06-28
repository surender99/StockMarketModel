"""Tests for RSI indicator — REQ-IND-RSI-001."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from tests.reference_indicators import pandas_ta_rsi

from athena_core.domain.indicators.rsi import compute_rsi


@pytest.fixture
def price_series() -> pd.Series:
    rng = np.random.default_rng(7)
    prices = 100 + np.cumsum(rng.normal(0, 1, 500))
    return pd.Series(prices, index=pd.date_range("2020-01-01", periods=500, freq="B"))


def test_rsi_bounded_0_100(price_series: pd.Series) -> None:
    rsi = compute_rsi(price_series, period=14)
    valid = rsi.dropna()
    assert (valid >= 0).all()
    assert (valid <= 100).all()


def test_rsi_pandas_ta_parity_when_available(price_series: pd.Series) -> None:
    ta_result = pandas_ta_rsi(price_series, 14)
    if ta_result is None:
        pytest.skip("pandas-ta not installed")
    ours = compute_rsi(price_series, period=14)
    pd.testing.assert_series_equal(ours, ta_result, check_names=False, rtol=1e-4, atol=1e-4)
