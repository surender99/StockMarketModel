"""OHLCV repository port — REQ-DATA-INGEST-001."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date, datetime

import pandas as pd


class OHLCVRepositoryPort(ABC):
    """Persist and load normalized OHLCV bars."""

    @abstractmethod
    def read(self, symbol: str, start: date | None = None, end: date | None = None) -> pd.DataFrame:
        """Load bars for *symbol*, optionally filtered by date range."""

    @abstractmethod
    def write(
        self,
        symbol: str,
        df: pd.DataFrame,
        *,
        source: str | None = None,
        ingestion_timestamp: datetime | None = None,
    ) -> int:
        """Merge and persist bars; return final row count."""

    @abstractmethod
    def exists(self, symbol: str) -> bool:
        """Return True if stored data exists for *symbol*."""
