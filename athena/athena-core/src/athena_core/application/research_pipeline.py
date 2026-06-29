"""Research pipeline execution — ATH-REL-010 §5.4, REQ-RS-PIPELINE-001."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Callable

from athena_core.domain.research.context import ExperimentSpec
from athena_core.domain.research.research_plugins import PIPELINE_STAGES


StageHandler = Callable[[ExperimentSpec, dict[str, Any]], dict[str, Any]]


@dataclass
class PipelineStageResult:
    """Output from a single pipeline stage."""

    stage: str
    status: str
    output: dict[str, Any] = field(default_factory=dict)
    completed_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass
class PipelineRunResult:
    """Aggregated pipeline run output — FR-006."""

    experiment_id: str
    stages: list[PipelineStageResult] = field(default_factory=list)
    artifacts: dict[str, Any] = field(default_factory=dict)

    @property
    def success(self) -> bool:
        return all(s.status == "ok" for s in self.stages)


class ResearchPipeline:
    """Execute research pipeline stages in order — FR-006."""

    def __init__(self, handlers: dict[str, StageHandler] | None = None) -> None:
        self._handlers = handlers or {}

    def run(
        self,
        experiment: ExperimentSpec,
        *,
        context: dict[str, Any] | None = None,
        stages: list[str] | None = None,
    ) -> PipelineRunResult:
        ctx = dict(context or {})
        stage_ids = stages or list(PIPELINE_STAGES)
        result = PipelineRunResult(experiment_id=experiment.experiment_id)
        for stage_id in stage_ids:
            if stage_id not in PIPELINE_STAGES:
                result.stages.append(
                    PipelineStageResult(stage=stage_id, status="skipped", output={"reason": "unknown stage"})
                )
                continue
            handler = self._handlers.get(stage_id)
            if handler is None:
                result.stages.append(
                    PipelineStageResult(stage=stage_id, status="ok", output={"note": "default pass-through"})
                )
                ctx[stage_id] = {"status": "ok"}
                continue
            try:
                output = handler(experiment, ctx)
                result.stages.append(PipelineStageResult(stage=stage_id, status="ok", output=output))
                ctx[stage_id] = output
            except Exception as exc:  # noqa: BLE001 — pipeline captures stage failures
                result.stages.append(
                    PipelineStageResult(stage=stage_id, status="error", output={"error": str(exc)})
                )
                break
        result.artifacts = ctx
        return result
