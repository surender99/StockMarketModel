"""Indicator pipeline execution — APS-IND-PIPELINE-001."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import pandas as pd

from athena_core.domain.indicators.engine import IndicatorEngine


@dataclass(frozen=True, slots=True)
class PipelineStage:
    """Single stage in an indicator pipeline."""

    stage_id: str
    indicator_id: str
    params: dict[str, Any] = field(default_factory=dict)


class IndicatorPipeline:
    """Chain indicator computations with named stage outputs."""

    def __init__(self, engine: IndicatorEngine, stages: list[PipelineStage]) -> None:
        self._engine = engine
        self._stages = stages

    @property
    def stages(self) -> tuple[PipelineStage, ...]:
        return tuple(self._stages)

    def run(self, ohlcv: pd.DataFrame) -> dict[str, pd.Series | pd.DataFrame]:
        """Execute stages in order; each stage reads the original OHLCV input."""
        outputs: dict[str, pd.Series | pd.DataFrame] = {}
        for stage in self._stages:
            outputs[stage.stage_id] = self._engine.compute(
                stage.indicator_id,
                ohlcv,
                stage.params,
            )
        return outputs
