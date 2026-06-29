"""Dataset lineage tracking — REQ-APS-DATASET-LINEAGE-001, ATH-REL-002 §10."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum


class LineageStepKind(str, Enum):
    """Transformation categories in a dataset lineage chain."""

    SOURCE = "source"
    INGEST = "ingest"
    CLEAN = "clean"
    VALIDATE = "validate"
    FEATURE = "feature"
    EXPORT = "export"


@dataclass(frozen=True, slots=True)
class LineageStep:
    """Single hop in a dataset lineage graph."""

    kind: LineageStepKind
    component: str
    input_id: str = ""
    output_id: str = ""
    metadata: dict[str, str] = field(default_factory=dict)
    recorded_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass
class DatasetLineage:
    """Ordered lineage for a registered dataset snapshot."""

    dataset_id: str
    steps: list[LineageStep] = field(default_factory=list)

    def append(self, step: LineageStep) -> None:
        self.steps.append(step)

    @property
    def origin(self) -> LineageStep | None:
        return self.steps[0] if self.steps else None

    @property
    def consumers(self) -> list[str]:
        return [s.component for s in self.steps if s.kind == LineageStepKind.FEATURE]


def build_ingest_lineage(
    dataset_id: str,
    *,
    source: str,
    symbol: str,
    content_version: str,
) -> DatasetLineage:
    """Build a minimal ingest→clean→validate lineage for OHLCV snapshots."""
    lineage = DatasetLineage(dataset_id=dataset_id)
    lineage.append(
        LineageStep(
            kind=LineageStepKind.SOURCE,
            component=source,
            output_id=symbol,
            metadata={"symbol": symbol},
        )
    )
    lineage.append(
        LineageStep(
            kind=LineageStepKind.INGEST,
            component="IngestOHLCVUseCase",
            input_id=symbol,
            output_id=dataset_id,
        )
    )
    lineage.append(
        LineageStep(
            kind=LineageStepKind.CLEAN,
            component="clean_ohlcv_frame",
            input_id=dataset_id,
            output_id=dataset_id,
        )
    )
    lineage.append(
        LineageStep(
            kind=LineageStepKind.VALIDATE,
            component="check_ohlcv_quality",
            input_id=dataset_id,
            output_id=content_version,
        )
    )
    return lineage
