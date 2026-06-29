"""OHLCV ingest use case — REQ-DATA-INGEST-001, REQ-DATA-CLEAN-001, REQ-DATA-QUALITY-001."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, date, datetime
from pathlib import Path

import structlog

from athena_core.application.config import AthenaConfig, DataIngestConfig
from athena_core.application.data_bootstrap import DataContext
from athena_core.application.data_platform_config import DataPlatformConfig
from athena_core.application.errors import DataQualityGateError, EmptyDataError
from athena_core.domain.data.cleaning import clean_ohlcv_frame
from athena_core.domain.data.quality import check_ohlcv_quality
from athena_core.domain.data.registry import DatasetDescriptor, DatasetKind
from athena_core.domain.data.versioning import build_snapshot_id, compute_content_version
from athena_core.domain.ports.dataset_registry import DatasetRegistryPort
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
    data_version: str = "v1"
    content_version: str = ""


class IngestOHLCVUseCase:
    """Fetch yfinance OHLCV and persist to Parquet."""

    def __init__(
        self,
        repository: OHLCVRepositoryPort,
        config: DataIngestConfig,
        client: YFinanceClientProtocol | None = None,
        *,
        platform_config: DataPlatformConfig | None = None,
        dataset_registry: DatasetRegistryPort | None = None,
    ) -> None:
        self._repo = repository
        self._config = config
        self._client = client or YFinanceClient(
            max_attempts=config.max_attempts,
            backoff_seconds=config.backoff_seconds,
        )
        self._platform = platform_config or DataPlatformConfig()
        self._registry = dataset_registry

    def _resolve_ticker(self, symbol: str) -> str:
        suffix = self._config.symbol_suffix
        if symbol.endswith(suffix):
            return symbol
        return f"{symbol}{suffix}"

    def _register_dataset(self, symbol: str, *, source: str, row_count: int) -> None:
        if self._registry is None:
            return
        meta = self._repo.read_metadata(symbol)
        if meta is None:
            return
        checksum = str(meta.get("checksum_sha256", ""))
        version = str(meta.get("data_version", self._platform.versioning.data_version))
        content_version = str(meta.get("content_version", compute_content_version(checksum, version)))
        dataset_id = build_snapshot_id(symbol, content_version)
        path = str(Path(self._config.base_path) / symbol.replace("/", "_") / "bars.parquet")
        self._registry.register(
            DatasetDescriptor(
                dataset_id=dataset_id,
                kind=DatasetKind.OHLCV,
                path=path,
                data_version=version,
                content_version=content_version,
                checksum_sha256=checksum,
                symbol=symbol,
                source=source,
                row_count=row_count,
                registered_at=datetime.now(UTC),
            )
        )

    def run(self, symbol: str, start: date, end: date) -> IngestResult:
        ticker = self._resolve_ticker(symbol)
        log.info("ingest.start", symbol=ticker, start=start.isoformat(), end=end.isoformat())
        raw = self._client.download(ticker, start, end, auto_adjust=False)
        df = normalize_yfinance_frame(raw, ticker)
        cleaning = self._platform.cleaning
        df = clean_ohlcv_frame(
            df,
            drop_na_ohlc=cleaning.drop_na_ohlc,
            sort_by_date=cleaning.sort_by_date,
        )
        validate_ohlcv(df)
        if df.empty:
            raise EmptyDataError(ticker, start, end, "no rows after normalization")

        validation = self._platform.validation
        quality = check_ohlcv_quality(
            df,
            symbol=ticker,
            outlier_z_threshold=validation.outlier_z_threshold,
        )
        if validation.enforce_quality_gate and not quality.passed:
            issues = ", ".join(issue.value for issue in quality.issues)
            raise DataQualityGateError(ticker, start, end, f"quality gate failed: {issues}")

        data_version = self._platform.versioning.data_version
        row_count = self._repo.write(
            ticker,
            df,
            source=self._config.source,
            ingestion_timestamp=datetime.now(UTC),
            data_version=data_version,
        )
        self._register_dataset(ticker, source=self._config.source, row_count=row_count)
        meta = self._repo.read_metadata(ticker) or {}
        result = IngestResult(
            symbol=ticker,
            start=start,
            end=end,
            row_count=row_count,
            timestamp=datetime.now(UTC),
            source=self._config.source,
            data_version=str(meta.get("data_version", data_version)),
            content_version=str(meta.get("content_version", "")),
        )
        log.info(
            "ingest.complete",
            symbol=result.symbol,
            row_count=result.row_count,
            source=result.source,
            data_version=result.data_version,
        )
        return result


def build_ingest_use_case(config: AthenaConfig, data: DataContext) -> IngestOHLCVUseCase:
    """Factory for wired ingest use case — ATH-REL-002."""
    return IngestOHLCVUseCase(
        data.ohlcv_repository,
        config.data_ingest,
        platform_config=config.data_platform,
        dataset_registry=data.dataset_registry,
    )
