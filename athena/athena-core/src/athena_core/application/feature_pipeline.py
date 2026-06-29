"""Feature pipeline orchestration — REQ-FEAT-PIPELINE-001, ATH-REL-003 §10."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Any

import pandas as pd

from athena_core.application.feature_service import FeatureService


@dataclass(frozen=True)
class FeatureRequest:
    """Single feature computation request within a pipeline."""

    feature_id: str
    params: dict[str, Any]
    alias: str | None = None


@dataclass
class FeaturePipelineResult:
    """Output bundle from a pipeline run."""

    symbol: str
    frames: dict[str, pd.DataFrame] = field(default_factory=dict)


class FeaturePipeline:
    """Orchestrate multiple feature requests for one symbol — REQ-FEAT-PIPELINE-001."""

    def __init__(self, service: FeatureService, requests: list[FeatureRequest]) -> None:
        self._service = service
        self._requests = requests

    def run(
        self,
        symbol: str,
        *,
        start: date | None = None,
        end: date | None = None,
    ) -> FeaturePipelineResult:
        result = FeaturePipelineResult(symbol=symbol)
        for request in self._requests:
            key = request.alias or request.feature_id
            result.frames[key] = self._service.get_feature(
                symbol,
                request.feature_id,
                request.params,
                start=start,
                end=end,
            )
        return result
