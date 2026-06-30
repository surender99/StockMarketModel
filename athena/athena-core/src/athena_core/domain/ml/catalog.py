"""MLP APS catalog — PHASE 10 Machine Learning Platform."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

MlpStatus = Literal["MVP", "Partial", "Deferred"]


@dataclass(frozen=True, slots=True)
class MlpCatalogEntry:
    aps_id: str
    name: str
    domain: str
    status: MlpStatus


MLP_CATALOG: tuple[MlpCatalogEntry, ...] = (
    MlpCatalogEntry("APS-ML-CORE-001", "Machine Learning Framework", "ML-Core", "MVP"),
    MlpCatalogEntry("APS-ML-MANAGER-001", "Model Manager", "ML-Core", "MVP"),
    MlpCatalogEntry("APS-DATASET-BUILDER-001", "Dataset Builder", "Dataset-Builder", "MVP"),
    MlpCatalogEntry("APS-REGISTRY-MODELS-001", "Model Registry", "Model-Registry", "MVP"),
    MlpCatalogEntry("APS-PREDICT-BATCH-001", "Batch Predictions", "Prediction-Services", "Partial"),
)


def list_mvp_mlp() -> tuple[MlpCatalogEntry, ...]:
    return tuple(e for e in MLP_CATALOG if e.status in ("MVP", "Partial"))
