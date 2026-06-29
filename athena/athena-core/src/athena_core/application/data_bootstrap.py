"""Data platform bootstrap — ATH-REL-002, builds on REL-001 CoreContext."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from athena_core.application.config import AthenaConfig
from athena_core.domain.ports.dataset_registry import DatasetRegistryPort
from athena_core.domain.ports.instrument_registry import InstrumentRegistryPort
from athena_core.domain.ports.ohlcv_repository import OHLCVRepositoryPort
from athena_core.domain.ports.trading_calendar import TradingCalendarPort
from athena_core.infrastructure.file_dataset_registry import FileDatasetRegistry
from athena_core.infrastructure.instrument_master import YamlInstrumentMaster
from athena_core.infrastructure.nse_calendar import NSETradingCalendar
from athena_core.infrastructure.parquet_ohlcv_store import ParquetOHLCVStore

_ATHENA_CORE_ROOT = Path(__file__).resolve().parents[3]


def _resolve_core_path(path: Path) -> Path:
    """Resolve bundled athena-core config paths when cwd differs (e.g. SDK tests)."""
    if path.is_file():
        return path
    candidate = _ATHENA_CORE_ROOT / path
    if candidate.is_file():
        return candidate
    return path


@dataclass
class DataContext:
    """Wired data platform services for runtime and SDK consumers."""

    calendar: TradingCalendarPort
    ohlcv_repository: OHLCVRepositoryPort
    dataset_registry: DatasetRegistryPort
    instrument_registry: InstrumentRegistryPort


def bootstrap_data_platform(config: AthenaConfig) -> DataContext:
    """Build the Release-02 data platform context from configuration."""
    platform = config.data_platform
    calendar = NSETradingCalendar(holidays_file=_resolve_core_path(config.calendar.holidays_file))
    ohlcv_repository = ParquetOHLCVStore(
        config.data_ingest.base_path,
        data_version=platform.versioning.data_version,
        immutable_snapshots=platform.versioning.immutable_snapshots,
    )
    dataset_registry = FileDatasetRegistry(platform.registry.registry_path)
    instrument_registry = YamlInstrumentMaster(
        _resolve_core_path(platform.instrument_master_file)
    )
    return DataContext(
        calendar=calendar,
        ohlcv_repository=ohlcv_repository,
        dataset_registry=dataset_registry,
        instrument_registry=instrument_registry,
    )
