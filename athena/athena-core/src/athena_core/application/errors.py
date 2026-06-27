"""Ingestion errors — REQ-DATA-INGEST-001."""

from __future__ import annotations

from datetime import date


class IngestError(Exception):
    """Base ingestion error with structured context."""

    def __init__(self, symbol: str, start: date, end: date, message: str) -> None:
        self.symbol = symbol
        self.start = start
        self.end = end
        super().__init__(f"{symbol} [{start}..{end}]: {message}")


class EmptyDataError(IngestError):
    """yfinance returned no rows for the requested range."""
