"""Data platform configuration — ATH-REL-002 §01, §06–§10."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field


class DataVersioningConfig(BaseModel):
    """REQ-DATA-VERSION-001 — dataset snapshots and lineage tags."""

    data_version: str = "v1"
    immutable_snapshots: bool = False


class DataRegistryConfig(BaseModel):
    """REQ-DATA-REGISTRY-001 — dataset catalog location."""

    registry_path: Path = Field(default=Path("./data/registry"))


class DataCleaningConfig(BaseModel):
    """REQ-DATA-CLEAN-001 — normalization without silent correction."""

    drop_na_ohlc: bool = True
    sort_by_date: bool = True


class DataValidationConfig(BaseModel):
    """REQ-DATA-QUALITY-001 — ingest quality gate settings."""

    enforce_quality_gate: bool = False
    outlier_z_threshold: float = 5.0


class DataPlatformConfig(BaseModel):
    """Release-02 data platform bundle — ATH-REL-002."""

    versioning: DataVersioningConfig = Field(default_factory=DataVersioningConfig)
    registry: DataRegistryConfig = Field(default_factory=DataRegistryConfig)
    cleaning: DataCleaningConfig = Field(default_factory=DataCleaningConfig)
    validation: DataValidationConfig = Field(default_factory=DataValidationConfig)
    instrument_master_file: Path = Field(default=Path("./config/instruments.yaml"))
