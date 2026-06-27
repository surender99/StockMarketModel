"""Tests for MACD indicator — REQ-IND-MACD-001."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from athena_core.domain.indicators.macd import compute_macd
from tests.reference_indicators import pandas_ta_macd


@pytest.fixture
def price_series() -> pd.Series:
    rng = np.random.default_rng(42)
    prices = 100 + np.cumsum(rng.normal(0, 1, 500))
    return pd.Series(prices, index=pd.date_range("2020-01-01", periods=500, freq="B"))


def test_macd_outputs_three_columns(price_series: pd.Series) -> None:
    result = compute_macd(price_series)
    assert list(result.columns) == ["macd", "signal", "histogram"]
    assert len(result) == len(price_series)


def test_macd_histogram_equals_macd_minus_signal(price_series: pd.Series) -> None:
    result = compute_macd(price_series)
    diff = result["macd"] - result["signal"]
    pd.testing.assert_series_equal(result["histogram"], diff, check_names=False, rtol=1e-9)


def test_macd_pandas_ta_parity_when_available(price_series: pd.Series) -> None:
    ta_result = pandas_ta_macd(price_series)
    if ta_result is None:
        pytest.skip("pandas-ta not installed")
    ours = compute_macd(price_series)
    for col in ("macd", "signal", "histogram"):
        pd.testing.assert_series_equal(
            ours[col], ta_result[col], check_names=False, rtol=1e-4, atol=1e-4
        )
