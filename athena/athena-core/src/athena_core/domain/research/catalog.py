"""QREP APS catalog — PHASE 9 Research Experimentation Platform."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

QrepStatus = Literal["MVP", "Partial", "Deferred"]


@dataclass(frozen=True, slots=True)
class QrepCatalogEntry:
    aps_id: str
    name: str
    domain: str
    status: QrepStatus


QREP_CATALOG: tuple[QrepCatalogEntry, ...] = (
    QrepCatalogEntry("APS-RES-CORE-001", "Research Workspace", "Research-Workspace", "MVP"),
    QrepCatalogEntry("APS-RES-PROJECT-001", "Research Projects", "Research-Workspace", "MVP"),
    QrepCatalogEntry("APS-EXP-CORE-001", "Experiment Framework", "Experiment-Engine", "MVP"),
    QrepCatalogEntry("APS-EXP-LIFECYCLE-001", "Experiment State Machine", "Experiment-Engine", "MVP"),
    QrepCatalogEntry("APS-EXP-COMPARISON-001", "Compare Experiments", "Experiment-Engine", "MVP"),
    QrepCatalogEntry("APS-HYPOTHESIS-CORE-001", "Research Hypotheses", "Hypothesis-Management", "MVP"),
    QrepCatalogEntry("APS-HYPOTHESIS-TRACKING-001", "Hypothesis Tracking", "Hypothesis-Management", "MVP"),
    QrepCatalogEntry("APS-RDATA-SNAPSHOT-001", "Immutable Dataset Snapshots", "Dataset-Management", "MVP"),
    QrepCatalogEntry("APS-RDATA-LINEAGE-001", "Dataset Lineage", "Dataset-Management", "MVP"),
    QrepCatalogEntry("APS-RDATA-COMPARISON-001", "Dataset Diff", "Dataset-Management", "MVP"),
    QrepCatalogEntry("APS-TRACKING-CORE-001", "Experiment Tracking Core", "Experiment-Tracking", "MVP"),
    QrepCatalogEntry("APS-TRACKING-METRICS-001", "Performance Tracking", "Experiment-Tracking", "MVP"),
    QrepCatalogEntry("APS-KB-NOTES-001", "Research Notes", "Research-Knowledge-Base", "MVP"),
    QrepCatalogEntry("APS-KB-FINDINGS-001", "Findings Repository", "Research-Knowledge-Base", "MVP"),
    QrepCatalogEntry("APS-REPRO-CORE-001", "Reproducibility Capture", "Reproducibility-Engine", "MVP"),
    QrepCatalogEntry("APS-REPRO-REPLAY-001", "Replay Experiments", "Reproducibility-Engine", "MVP"),
    QrepCatalogEntry("APS-REPRO-VERIFY-001", "Reproducibility Verification", "Reproducibility-Engine", "MVP"),
    QrepCatalogEntry("APS-COMP-EXPERIMENT-001", "Experiment Comparison", "Comparison-Engine", "MVP"),
    QrepCatalogEntry("APS-REGISTRY-RESEARCH-001", "Research Registry", "Research-Registry", "MVP"),
    QrepCatalogEntry("APS-VALIDATE-EXPERIMENT-001", "Experiment Validation", "Research-Validation", "MVP"),
)


def list_mvp_qrep() -> list[QrepCatalogEntry]:
    return [e for e in QREP_CATALOG if e.status == "MVP"]


def get_qrep_entry(aps_id: str) -> QrepCatalogEntry | None:
    for entry in QREP_CATALOG:
        if entry.aps_id == aps_id:
            return entry
    return None
