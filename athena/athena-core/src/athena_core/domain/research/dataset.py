"""Dataset snapshots and lineage — ATH-REL-010 §5.3, REQ-RS-DATASET-001."""

from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass(frozen=True)
class DatasetSnapshot:
    """Immutable dataset snapshot for reproducibility — FR-004."""

    snapshot_id: str
    dataset_id: str
    version: str
    content_hash: str
    lineage: tuple[str, ...]
    captured_at: datetime
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def capture(
        cls,
        dataset_id: str,
        version: str,
        payload: dict[str, Any],
        *,
        parent_snapshot_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> DatasetSnapshot:
        content_hash = reproducibility_hash(payload)
        lineage: list[str] = []
        if parent_snapshot_id:
            lineage.append(parent_snapshot_id)
        return cls(
            snapshot_id=str(uuid.uuid4()),
            dataset_id=dataset_id,
            version=version,
            content_hash=content_hash,
            lineage=tuple(lineage),
            captured_at=datetime.now(UTC),
            metadata=dict(metadata or {}),
        )


def reproducibility_hash(payload: dict[str, Any]) -> str:
    """Deterministic hash for dataset reproducibility — FR-014."""
    encoded = json.dumps(payload, sort_keys=True, default=str).encode()
    return hashlib.sha256(encoded).hexdigest()


def compare_snapshots(a: DatasetSnapshot, b: DatasetSnapshot) -> dict[str, Any]:
    """Compare two dataset snapshots — FR-005."""
    return {
        "same_content": a.content_hash == b.content_hash,
        "same_version": a.version == b.version,
        "hash_a": a.content_hash,
        "hash_b": b.content_hash,
        "lineage_overlap": list(set(a.lineage) & set(b.lineage)),
    }
