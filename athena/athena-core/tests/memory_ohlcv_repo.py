"""Shared in-memory OHLCV repository for tests."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any

import pandas as pd

from athena_core.domain.ports.ohlcv_repository import OHLCVRepositoryPort


class MemoryOHLCVRepo(OHLCVRepositoryPort):
    """Minimal OHLCV repository stub implementing the full port."""

    def __init__(self, frames: dict[str, pd.DataFrame] | None = None) -> None:
        self._frames = frames or {}

    def read(self, symbol: str, start: date | None = None, end: date | None = None) -> pd.DataFrame:
        df = self._frames.get(symbol, pd.DataFrame())
        if df.empty:
            return df
        out = df.copy()
        if start:
            out = out[out["date"] >= start]
        if end:
            out = out[out["date"] <= end]
        return out.reset_index(drop=True)

    def write(
        self,
        symbol: str,
        df: pd.DataFrame,
        *,
        source: str | None = None,
        ingestion_timestamp: datetime | None = None,
        data_version: str | None = None,
    ) -> int:
        self._frames[symbol] = df
        return len(df)

    def read_metadata(self, symbol: str) -> dict[str, Any] | None:
        if symbol not in self._frames:
            return None
        return {"symbol": symbol, "row_count": len(self._frames[symbol])}

    def exists(self, symbol: str) -> bool:
        return symbol in self._frames
