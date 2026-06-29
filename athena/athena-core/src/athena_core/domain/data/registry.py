"""Dataset registry models — REQ-DATA-REGISTRY-001, ATH-REL-002 §10."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class DatasetKind(str, Enum):
    """Registered dataset categories."""

    OHLCV = "ohlcv"
    FEATURES = "features"
    INSTRUMENTS = "instruments"


@dataclass(frozen=True, slots=True)
class DatasetDescriptor:
    """Catalog entry for a versioned on-disk dataset."""

    dataset_id: str
    kind: DatasetKind
    path: str
    data_version: str
    content_version: str
    checksum_sha256: str
    symbol: str = ""
    source: str = ""
    row_count: int = 0
    registered_at: datetime = field(default_factory=datetime.utcnow)
