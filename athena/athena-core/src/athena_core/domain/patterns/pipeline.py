"""Pattern detection pipeline — APS-PAT-PIPELINE-001, MSP CTO recommendation."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

import pandas as pd

from athena_core.domain.patterns.base import PatternDetector
from athena_core.domain.patterns.types import PatternEvent


class PatternPipelineStage(str, Enum):
    """Ordered stages in the shared pattern detection pipeline."""

    SWING = "swing"
    MARKET_STRUCTURE = "market_structure"
    CANDIDATE = "candidate_detection"
    VOLUME = "volume_confirmation"
    TREND = "trend_confirmation"
    SUPPORT_RESISTANCE = "support_resistance_confirmation"
    SCORING = "confidence_scoring"
    VALIDATED = "validated_pattern"


@dataclass(frozen=True, slots=True)
class PipelineStageResult:
    """Output from a single pipeline stage."""

    stage: PatternPipelineStage
    events: tuple[PatternEvent, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)


class PatternPipeline:
    """Run pattern detection through MSP decision stages."""

    DEFAULT_STAGES: tuple[PatternPipelineStage, ...] = tuple(PatternPipelineStage)

    def __init__(
        self,
        detector: PatternDetector | None = None,
        *,
        stages: tuple[PatternPipelineStage, ...] | None = None,
        pattern_ids: list[str] | None = None,
    ) -> None:
        self._detector = detector or PatternDetector()
        self._stages = stages or self.DEFAULT_STAGES
        self._pattern_ids = pattern_ids

    @property
    def stages(self) -> tuple[PatternPipelineStage, ...]:
        return self._stages

    def run(self, ohlcv: pd.DataFrame) -> list[PipelineStageResult]:
        """Execute pipeline stages; candidate stage runs builtin pattern detectors."""
        results: list[PipelineStageResult] = []
        candidates: list[PatternEvent] = []

        for stage in self._stages:
            if stage == PatternPipelineStage.CANDIDATE:
                if self._pattern_ids:
                    for pid in self._pattern_ids:
                        candidates.extend(self._detector.detect(ohlcv, pid))
                else:
                    candidates = self._detector.detect_all(ohlcv)
                results.append(
                    PipelineStageResult(stage=stage, events=tuple(candidates), metadata={"count": len(candidates)})
                )
            elif stage == PatternPipelineStage.SCORING:
                scored = tuple(self._score_events(c) for c in candidates)
                results.append(
                    PipelineStageResult(stage=stage, events=scored, metadata={"count": len(scored)})
                )
                candidates = list(scored)
            elif stage == PatternPipelineStage.VALIDATED:
                validated = tuple(e for e in candidates if e.confidence >= 0.5)
                results.append(
                    PipelineStageResult(stage=stage, events=validated, metadata={"count": len(validated)})
                )
            else:
                results.append(PipelineStageResult(stage=stage, metadata={"status": "deferred"}))

        return results

    def run_validated(self, ohlcv: pd.DataFrame) -> list[PatternEvent]:
        """Return validated patterns after full pipeline."""
        for result in reversed(self.run(ohlcv)):
            if result.stage == PatternPipelineStage.VALIDATED:
                return list(result.events)
        return []

    @staticmethod
    def _score_events(event: PatternEvent) -> PatternEvent:
        return PatternEvent(
            pattern_id=event.pattern_id,
            pattern_type=event.pattern_type,
            bar_index=event.bar_index,
            confidence=min(1.0, event.confidence + 0.05),
            metadata=dict(event.metadata),
        )
