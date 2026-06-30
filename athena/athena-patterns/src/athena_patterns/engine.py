"""Pattern engine adapter implementing IPatternEngine."""
from __future__ import annotations

import pandas as pd

from athena_core.domain.patterns.pipeline import PatternPipeline
from athena_core.domain.patterns.types import PatternEvent


class PatternEngineFacade:
    """Delegates to athena-core PatternPipeline — extraction path: ADR-0006."""

    def __init__(self, pipeline: PatternPipeline | None = None) -> None:
        self._pipeline = pipeline or PatternPipeline()

    def detect(self, ohlcv: pd.DataFrame) -> list[PatternEvent]:
        return self._pipeline.run_validated(ohlcv)
