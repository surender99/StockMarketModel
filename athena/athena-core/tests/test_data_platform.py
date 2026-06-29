"""Data platform tests — ATH-REL-002."""

from __future__ import annotations

from datetime import UTC, date, datetime
from pathlib import Path

import pandas as pd
import pytest

from athena_core.application.bootstrap import bootstrap_athena_core
from athena_core.application.config import AthenaConfig, DataIngestConfig
from athena_core.application.data_bootstrap import bootstrap_data_platform
from athena_core.application.data_platform_config import DataPlatformConfig, DataRegistryConfig, DataValidationConfig
from athena_core.application.errors import DataQualityGateError, ImmutabilityViolationError
from athena_core.application.ingest_ohlcv import IngestOHLCVUseCase
from athena_core.domain.data.cleaning import clean_ohlcv_frame
from athena_core.domain.data.lineage import LineageStepKind, build_ingest_lineage
from athena_core.domain.data.quality import (
    DataQualityIssue,
    check_ohlcv_quality,
    compute_quality_score,
    profile_ohlcv_frame,
)
from athena_core.domain.data.registry import DatasetDescriptor, DatasetKind
from athena_core.domain.data.versioning import build_snapshot_id, compute_content_version
from athena_core.infrastructure.file_dataset_registry import FileDatasetRegistry
from athena_core.infrastructure.instrument_master import YamlInstrumentMaster
from athena_core.infrastructure.parquet_ohlcv_store import ParquetOHLCVStore
from athena_core.infrastructure.yfinance_client import normalize_yfinance_frame


def _sample_df() -> pd.DataFrame:
    return normalize_yfinance_frame(
        pd.DataFrame(
            {
                "Open": [100.0, 101.0],
                "High": [105.0, 106.0],
                "Low": [99.0, 100.0],
                "Close": [104.0, 105.0],
                "Volume": [1000, 1100],
            },
            index=pd.to_datetime(["2024-01-02", "2024-01-03"]),
        ),
        "RELIANCE.NS",
    )


class MockYFinanceClient:
    def download(
        self,
        ticker: str,
        start: date,
        end: date,
        *,
        auto_adjust: bool = False,
    ) -> pd.DataFrame:
        return pd.DataFrame(
            {
                "Open": [100.0, 101.0, 500.0],
                "High": [105.0, 106.0, 510.0],
                "Low": [99.0, 100.0, 490.0],
                "Close": [104.0, 105.0, 505.0],
                "Volume": [1000, 0, 1000],
            },
            index=pd.to_datetime(["2024-01-02", "2024-01-03", "2024-01-04"]),
        )


def test_clean_ohlcv_drops_na_and_duplicates() -> None:
    df = _sample_df()
    df = pd.concat([df, df.iloc[[0]]], ignore_index=True)
    df.loc[2, "open"] = None
    cleaned = clean_ohlcv_frame(df)
    assert len(cleaned) == 2
    assert cleaned["date"].is_monotonic_increasing
    assert cleaned["open"].notna().all()


def test_compute_content_version_is_stable() -> None:
    checksum = "a" * 64
    assert compute_content_version(checksum, "v1") == compute_content_version(checksum, "v1")
    assert build_snapshot_id("RELIANCE.NS", "abc123") == "RELIANCE.NS@abc123"


def test_file_dataset_registry_roundtrip(tmp_path: Path) -> None:
    registry = FileDatasetRegistry(tmp_path)
    descriptor = DatasetDescriptor(
        dataset_id="RELIANCE.NS@v1",
        kind=DatasetKind.OHLCV,
        path=str(tmp_path / "bars.parquet"),
        data_version="v1",
        content_version="deadbeef",
        checksum_sha256="a" * 64,
        symbol="RELIANCE.NS",
        source="yfinance",
        row_count=10,
        registered_at=datetime.now(UTC),
    )
    registry.register(descriptor)
    loaded = registry.get("RELIANCE.NS@v1")
    assert loaded is not None
    assert loaded.symbol == "RELIANCE.NS"
    assert registry.list_datasets(kind=DatasetKind.OHLCV) == [loaded]


def test_yaml_instrument_master_resolves_symbols() -> None:
    master = YamlInstrumentMaster()
    symbol = master.resolve("RELIANCE")
    assert symbol is not None
    assert symbol.yfinance_ticker == "RELIANCE.NS"
    assert len(master.list_symbols()) >= 3


def test_parquet_metadata_includes_data_version(tmp_path: Path) -> None:
    store = ParquetOHLCVStore(tmp_path, data_version="v2")
    store.write("X.NS", _sample_df(), source="yfinance", data_version="v2")
    meta = store.read_metadata("X.NS")
    assert meta is not None
    assert meta["data_version"] == "v2"
    assert meta["content_version"]
    assert meta["immutable"] is False


def test_immutable_store_blocks_second_write(tmp_path: Path) -> None:
    store = ParquetOHLCVStore(tmp_path, immutable_snapshots=True)
    store.write("X.NS", _sample_df(), source="yfinance")
    with pytest.raises(ImmutabilityViolationError):
        store.write("X.NS", _sample_df(), source="yfinance")


def test_ingest_registers_dataset(tmp_path: Path) -> None:
    registry_path = tmp_path / "registry"
    ohlcv_path = tmp_path / "ohlcv"
    store = ParquetOHLCVStore(ohlcv_path)
    registry = FileDatasetRegistry(registry_path)
    platform = DataPlatformConfig(registry=DataRegistryConfig(registry_path=registry_path))
    use_case = IngestOHLCVUseCase(
        store,
        DataIngestConfig(base_path=ohlcv_path),
        client=MockYFinanceClient(),
        platform_config=platform,
        dataset_registry=registry,
    )
    result = use_case.run("RELIANCE", date(2024, 1, 1), date(2024, 1, 10))
    assert result.data_version == "v1"
    datasets = registry.list_datasets(kind=DatasetKind.OHLCV)
    assert len(datasets) == 1
    assert datasets[0].symbol == "RELIANCE.NS"


def test_quality_gate_blocks_ingest(tmp_path: Path) -> None:
    store = ParquetOHLCVStore(tmp_path)
    platform = DataPlatformConfig(validation=DataValidationConfig(enforce_quality_gate=True))
    use_case = IngestOHLCVUseCase(
        store,
        DataIngestConfig(),
        client=MockYFinanceClient(),
        platform_config=platform,
    )
    with pytest.raises(DataQualityGateError, match="zero_volume"):
        use_case.run("RELIANCE", date(2024, 1, 1), date(2024, 1, 10))


def test_bootstrap_data_platform_wires_services() -> None:
    ctx = bootstrap_data_platform(AthenaConfig())
    assert ctx.calendar is not None
    assert ctx.ohlcv_repository is not None
    assert ctx.dataset_registry is not None
    assert ctx.instrument_registry is not None


def test_bootstrap_core_includes_data_context() -> None:
    ctx = bootstrap_athena_core(AthenaConfig())
    assert ctx.data is not None
    assert ctx.container.has("data")


def test_compute_quality_score_penalizes_issues() -> None:
    df = _sample_df()
    df.loc[0, "high"] = 50.0
    report = check_ohlcv_quality(df, "TEST.NS")
    assert DataQualityIssue.INVALID_OHLC in report.issues
    score = compute_quality_score(report)
    assert 0.0 < score < 100.0
    clean_report = check_ohlcv_quality(_sample_df(), "TEST.NS")
    assert compute_quality_score(clean_report) == 100.0


def test_profile_ohlcv_frame_summarizes_columns() -> None:
    profile = profile_ohlcv_frame(_sample_df())
    assert profile["row_count"] == 2
    assert "close_min" in profile
    assert "volume_null_count" in profile


def test_build_ingest_lineage_tracks_pipeline() -> None:
    lineage = build_ingest_lineage(
        "RELIANCE.NS@abc123",
        source="yfinance",
        symbol="RELIANCE.NS",
        content_version="abc123",
    )
    assert lineage.origin is not None
    assert lineage.origin.kind == LineageStepKind.SOURCE
    assert len(lineage.steps) == 4
    assert lineage.steps[-1].kind == LineageStepKind.VALIDATE
