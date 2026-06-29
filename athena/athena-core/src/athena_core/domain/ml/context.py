"""ML context and metadata — ATH-REL-011 §5."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass(frozen=True)
class ModelMetadata:
    """Registered model metadata — FR-003."""

    model_id: str
    version: str
    algorithm: str
    features: tuple[str, ...]
    metrics: dict[str, float]
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    tags: dict[str, str] = field(default_factory=dict)

    def reproducibility_hash(self) -> str:
        payload = {
            "model_id": self.model_id,
            "version": self.version,
            "algorithm": self.algorithm,
            "features": list(self.features),
            "metrics": self.metrics,
        }
        return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()[:16]


@dataclass
class MLContext:
    """Input bundle for ML workflows — FR-012."""

    dataset_id: str
    feature_columns: list[str]
    target_column: str
    params: dict[str, Any] = field(default_factory=dict)
    split_method: str = "time_series"
