"""OHLCV ingest use case — REQ-DATA-INGEST-001."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, date, datetime

import structlog

from athena_core.application.config import DataIngestConfig
from athena_core.application.errors import EmptyDataError
from athena_core.domain.ports.ohlcv_repository import OHLCVRepositoryPort
from athena_core.infrastructure.yfinance_client import (
    YFinanceClient,
    YFinanceClientProtocol,
    normalize_yfinance_frame,
    validate_ohlcv,
)

log = structlog.get_logger(__name__)


@dataclass(frozen=True, slots=True)
class IngestResult:
    """Manifest entry for a completed ingest."""

    symbol: str
    start: date
    end: date
    row_count: int
    timestamp: datetime
    source: str


class IngestOHLCVUseCase:
    """Fetch yfinance OHLCV and persist to Parquet."""

    def __init__(
        self,
        repository: OHLCVRepositoryPort,
        config: DataIngestConfig,
        client: YFinanceClientProtocol | None = None,
    ) -> None:
        self._repo = repository
        self._config = config
        self._client = client or YFinanceClient(
            max_attempts=config.max_attempts,
            backoff_seconds=config.backoff_seconds,
        )

    def _resolve_ticker(self, symbol: str) -> str:
        suffix = self._config.symbol_suffix
        if symbol.endswith(suffix):
            return symbol
        return f"{symbol}{suffix}"

    def run(self, symbol: str, start: date, end: date) -> IngestResult:
        ticker = self._resolve_ticker(symbol)
        log.info("ingest.start", symbol=ticker, start=start.isoformat(), end=end.isoformat())
        raw = self._client.download(ticker, start, end, auto_adjust=False)
        df = normalize_yfinance_frame(raw, ticker)
        validate_ohlcv(df)
        if df.empty:
            raise EmptyDataError(ticker, start, end, "no rows after normalization")
        row_count = self._repo.write(
            ticker,
            df,
            source=self._config.source,
            ingestion_timestamp=datetime.now(UTC),
        )
        result = IngestResult(
            symbol=ticker,
            start=start,
            end=end,
            row_count=row_count,
            timestamp=datetime.now(UTC),
            source=self._config.source,
        )
        log.info(
            "ingest.complete",
            symbol=result.symbol,
            row_count=result.row_count,
            source=result.source,
        )
        return result
