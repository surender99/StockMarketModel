"""Tests for ATR indicator — REQ-IND-ATR-001."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from athena_core.domain.indicators.atr import compute_atr, compute_atr_from_ohlcv


@pytest.fixture
def ohlcv_df() -> pd.DataFrame:
    dates = pd.date_range("2020-01-01", periods=100, freq="B")
    close = pd.Series(100 + np.arange(100) * 0.5, index=dates)
    return pd.DataFrame(
        {
            "date": dates.date,
            "open": close.values,
            "high": close.values + 2,
            "low": close.values - 2,
            "close": close.values,
            "volume": 1000,
        }
    )


def test_atr_positive_after_warmup(ohlcv_df: pd.DataFrame) -> None:
    result = compute_atr(ohlcv_df, period=14)
    assert result.iloc[13:].notna().all()
    assert (result.iloc[13:] > 0).all()


def test_atr_from_ohlcv_matches_direct(ohlcv_df: pd.DataFrame) -> None:
    direct = compute_atr(ohlcv_df, 14)
    from_df = compute_atr_from_ohlcv(ohlcv_df, 14)
    pd.testing.assert_series_equal(direct.reset_index(drop=True), from_df.reset_index(drop=True))


def test_atr_warmup_is_nan(ohlcv_df: pd.DataFrame) -> None:
    result = compute_atr(ohlcv_df, period=14)
    assert result.iloc[:13].isna().all()
