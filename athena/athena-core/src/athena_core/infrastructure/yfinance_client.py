"""yfinance OHLCV client — REQ-DATA-INGEST-001."""

from __future__ import annotations

import time
from datetime import date
from typing import Protocol

import pandas as pd
import yfinance as yf

from athena_core.application.errors import EmptyDataError


class YFinanceClientProtocol(Protocol):
    """Protocol for test doubles."""

    def download(
        self,
        ticker: str,
        start: date,
        end: date,
        *,
        auto_adjust: bool = False,
    ) -> pd.DataFrame: ...


class YFinanceClient:
    """Download daily OHLCV via yfinance with retry."""

    def __init__(self, max_attempts: int = 3, backoff_seconds: float = 2.0) -> None:
        self._max_attempts = max_attempts
        self._backoff = backoff_seconds

    def download(
        self,
        ticker: str,
        start: date,
        end: date,
        *,
        auto_adjust: bool = False,
    ) -> pd.DataFrame:
        last_error: Exception | None = None
        for attempt in range(1, self._max_attempts + 1):
            try:
                raw = yf.download(
                    ticker,
                    start=start.isoformat(),
                    end=end.isoformat(),
                    auto_adjust=auto_adjust,
                    progress=False,
                    threads=False,
                )
                if raw.empty:
                    raise EmptyDataError(ticker, start, end, "yfinance returned empty DataFrame")
                return raw
            except EmptyDataError:
                raise
            except Exception as exc:  # noqa: BLE001 — retry boundary
                last_error = exc
                if attempt < self._max_attempts:
                    time.sleep(self._backoff * attempt)
        assert last_error is not None
        raise EmptyDataError(ticker, start, end, str(last_error)) from last_error


def normalize_yfinance_frame(raw: pd.DataFrame, symbol: str) -> pd.DataFrame:
    """Normalize yfinance response to canonical schema — REQ-DATA-INGEST-001."""
    df = raw.copy()
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df = df.reset_index()
    rename_map = {
        "Date": "date",
        "Datetime": "date",
        "index": "date",
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Volume": "volume",
    }
    df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})
    if "date" not in df.columns:
        date_col = df.columns[0]
        df = df.rename(columns={date_col: "date"})
    df["date"] = pd.to_datetime(df["date"]).dt.date
    df["symbol"] = symbol
    for col in ("open", "high", "low", "close", "volume"):
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df[["date", "open", "high", "low", "close", "volume", "symbol"]]


def validate_ohlcv(df: pd.DataFrame) -> None:
    """Validate OHLC consistency — REQ-DATA-INGEST-001."""
    if df["date"].duplicated().any():
        msg = "duplicate dates in OHLCV frame"
        raise ValueError(msg)
    if (df["volume"] < 0).any():
        msg = "negative volume detected"
        raise ValueError(msg)
    high_ok = df["high"] >= df[["open", "close"]].max(axis=1)
    low_ok = df["low"] <= df[["open", "close"]].min(axis=1)
    if not high_ok.all() or not low_ok.all():
        msg = "OHLC consistency violation"
        raise ValueError(msg)
