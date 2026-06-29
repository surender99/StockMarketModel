"""Model registry — ATH-REL-011 §5.3, REQ-ML-REGISTRY-001."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from athena_core.domain.ml.context import ModelMetadata


@dataclass
class ModelVersion:
    """Versioned model artifact reference."""

    model_id: str
    version: str
    artifact_path: str
    metadata: ModelMetadata
    registered_at: datetime = field(default_factory=lambda: datetime.now(UTC))


class ModelRegistry:
    """In-memory model registry — FR-003."""

    def __init__(self) -> None:
        self._versions: dict[str, list[ModelVersion]] = {}

    def register(
        self,
        model_id: str,
        version: str,
        artifact_path: str,
        metadata: ModelMetadata,
    ) -> ModelVersion:
        entry = ModelVersion(
            model_id=model_id,
            version=version,
            artifact_path=artifact_path,
            metadata=metadata,
        )
        self._versions.setdefault(model_id, []).append(entry)
        return entry

    def get(self, model_id: str, version: str | None = None) -> ModelVersion | None:
        versions = self._versions.get(model_id, [])
        if not versions:
            return None
        if version is None:
            return versions[-1]
        for entry in versions:
            if entry.version == version:
                return entry
        return None

    def list_models(self) -> list[str]:
        return sorted(self._versions.keys())

    def list_versions(self, model_id: str) -> list[ModelVersion]:
        return list(self._versions.get(model_id, []))

    def compare(self, model_id: str, metric: str = "accuracy") -> list[dict[str, Any]]:
        versions = self.list_versions(model_id)
        rows = [
            {
                "version": v.version,
                "metric": metric,
                "value": v.metadata.metrics.get(metric, 0.0),
                "hash": v.metadata.reproducibility_hash(),
            }
            for v in versions
        ]
        return sorted(rows, key=lambda r: r["value"], reverse=True)
