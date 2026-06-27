"""Tests for OHLCV ingest — REQ-DATA-INGEST-001."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pandas as pd
import pytest

from athena_core.application.config import DataIngestConfig
from athena_core.application.errors import EmptyDataError
from athena_core.application.ingest_ohlcv import IngestOHLCVUseCase
from athena_core.infrastructure.parquet_ohlcv_store import ParquetOHLCVStore
from athena_core.infrastructure.yfinance_client import (
    normalize_yfinance_frame,
    validate_ohlcv,
)


def _sample_raw() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Open": [100.0, 101.0],
            "High": [105.0, 106.0],
            "Low": [99.0, 100.0],
            "Close": [104.0, 105.0],
            "Volume": [1000, 1100],
        },
        index=pd.to_datetime(["2024-01-02", "2024-01-03"]),
    )


class MockYFinanceClient:
    def __init__(self, frame: pd.DataFrame | None = None, *, empty: bool = False) -> None:
        self._frame = pd.DataFrame() if empty else (frame if frame is not None else _sample_raw())
        self.calls = 0

    def download(
        self,
        ticker: str,
        start: date,
        end: date,
        *,
        auto_adjust: bool = False,
    ) -> pd.DataFrame:
        self.calls += 1
        if self._frame.empty:
            raise EmptyDataError(ticker, start, end, "yfinance returned empty DataFrame")
        return self._frame


def test_normalize_schema() -> None:
    df = normalize_yfinance_frame(_sample_raw(), "RELIANCE.NS")
    assert list(df.columns) == ["date", "open", "high", "low", "close", "volume", "symbol"]
    assert df["symbol"].iloc[0] == "RELIANCE.NS"
    assert isinstance(df["date"].iloc[0], date)


def test_validate_rejects_invalid_ohlc() -> None:
    df = normalize_yfinance_frame(_sample_raw(), "X.NS")
    df.loc[0, "high"] = 50.0
    with pytest.raises(ValueError, match="OHLC"):
        validate_ohlcv(df)


def test_validate_rejects_duplicates() -> None:
    df = normalize_yfinance_frame(_sample_raw(), "X.NS")
    df = pd.concat([df, df.iloc[[0]]], ignore_index=True)
    with pytest.raises(ValueError, match="duplicate"):
        validate_ohlcv(df)


def test_incremental_merge_deduplication(tmp_path: Path) -> None:
    store = ParquetOHLCVStore(tmp_path)
    df1 = normalize_yfinance_frame(_sample_raw(), "RELIANCE.NS")
    store.write("RELIANCE.NS", df1)
    df2 = df1.copy()
    df2.loc[1, "close"] = 999.0
    df2.loc[1, "high"] = 1000.0
    count = store.write("RELIANCE.NS", df2)
    loaded = store.read("RELIANCE.NS")
    assert count == 2
    assert len(loaded) == 2
    assert loaded.loc[loaded["date"] == date(2024, 1, 3), "close"].iloc[0] == 999.0


def test_empty_response_raises_structured_error(tmp_path: Path) -> None:
    store = ParquetOHLCVStore(tmp_path)
    use_case = IngestOHLCVUseCase(
        store,
        DataIngestConfig(),
        client=MockYFinanceClient(empty=True),
    )
    with pytest.raises(EmptyDataError) as exc:
        use_case.run("RELIANCE", date(2024, 1, 1), date(2024, 12, 31))
    assert exc.value.symbol == "RELIANCE.NS"


def test_ingest_writes_parquet(tmp_path: Path) -> None:
    store = ParquetOHLCVStore(tmp_path)
    use_case = IngestOHLCVUseCase(store, DataIngestConfig(), client=MockYFinanceClient())
    result = use_case.run("RELIANCE", date(2024, 1, 1), date(2024, 1, 10))
    assert result.row_count == 2
    assert store.exists("RELIANCE.NS")


@pytest.mark.integration
def test_live_fetch_reliance() -> None:
    """Live yfinance fetch — skippable in CI."""
    pytest.importorskip("yfinance")
    store = ParquetOHLCVStore(Path("./data/test_ohlcv"))
    use_case = IngestOHLCVUseCase(store, DataIngestConfig())
    result = use_case.run("RELIANCE", date(2023, 1, 1), date(2024, 1, 1))
    assert result.row_count >= 200
