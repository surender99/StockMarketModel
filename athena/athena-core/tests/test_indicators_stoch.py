"""Tests for stochastic indicator — REQ-IND-STOCH-001."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from tests.reference_indicators import pandas_ta_stoch

from athena_core.domain.indicators.stoch import compute_stoch_from_ohlcv, compute_stochastic


@pytest.fixture
def ohlcv() -> pd.DataFrame:
    rng = np.random.default_rng(3)
    n = 200
    close = 100 + np.cumsum(rng.normal(0, 1, n))
    high = close + rng.uniform(0.5, 2.0, n)
    low = close - rng.uniform(0.5, 2.0, n)
    return pd.DataFrame({"high": high, "low": low, "close": close})


def test_stoch_bounded_0_100(ohlcv: pd.DataFrame) -> None:
    result = compute_stochastic(ohlcv["high"], ohlcv["low"], ohlcv["close"])
    valid_k = result["stoch_k"].dropna()
    valid_d = result["stoch_d"].dropna()
    assert (valid_k >= 0).all() and (valid_k <= 100).all()
    assert (valid_d >= 0).all() and (valid_d <= 100).all()


def test_stoch_pandas_ta_parity_when_available(ohlcv: pd.DataFrame) -> None:
    ta_result = pandas_ta_stoch(ohlcv["high"], ohlcv["low"], ohlcv["close"])
    if ta_result is None:
        pytest.skip("pandas-ta not installed")
    ours = compute_stoch_from_ohlcv(ohlcv)
    pd.testing.assert_series_equal(
        ours["stoch_k"], ta_result["stoch_k"], check_names=False, rtol=1e-4, atol=1e-4
    )
    pd.testing.assert_series_equal(
        ours["stoch_d"], ta_result["stoch_d"], check_names=False, rtol=1e-4, atol=1e-4
    )
