"""Tests for data quality — REQ-DATA-QUALITY-001."""

from __future__ import annotations

import pandas as pd

from athena_core.domain.data.quality import DataQualityIssue, check_ohlcv_quality


def _sample_ohlcv(n: int = 10) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "date": pd.date_range("2024-01-01", periods=n, freq="B").date,
            "open": range(100, 100 + n),
            "high": range(101, 101 + n),
            "low": range(99, 99 + n),
            "close": range(100, 100 + n),
            "volume": [1000] * n,
        }
    )


def test_clean_data_passes() -> None:
    report = check_ohlcv_quality(_sample_ohlcv(), symbol="TEST")
    assert report.passed
    assert report.issues == []


def test_duplicate_dates_flagged() -> None:
    df = _sample_ohlcv(5)
    df = pd.concat([df, df.iloc[[0]]], ignore_index=True)
    report = check_ohlcv_quality(df)
    assert DataQualityIssue.DUPLICATE_ROWS in report.issues


def test_invalid_ohlc_flagged() -> None:
    df = _sample_ohlcv(3)
    df.loc[0, "high"] = 50
    report = check_ohlcv_quality(df)
    assert DataQualityIssue.INVALID_OHLC in report.issues


def test_zero_volume_flagged() -> None:
    df = _sample_ohlcv(3)
    df.loc[1, "volume"] = 0
    report = check_ohlcv_quality(df)
    assert DataQualityIssue.ZERO_VOLUME in report.issues


def test_empty_dataframe_fails() -> None:
    report = check_ohlcv_quality(pd.DataFrame(), symbol="EMPTY")
    assert not report.passed
    assert DataQualityIssue.MISSING_CANDLES in report.issues
