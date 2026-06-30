"""Strategy engine adapter implementing IStrategyEngine."""
from __future__ import annotations

import pandas as pd

from athena_core.domain.strategy.config import StrategyConfig
from athena_core.domain.strategy.engine import StrategyEngine
from athena_core.domain.strategy.types import TradeSignal


class StrategyEngineFacade:
    """Delegates to athena-core StrategyEngine — extraction path: ADR-0006."""

    def __init__(self, engine: StrategyEngine | None = None) -> None:
        self._engine = engine or StrategyEngine()

    def validate(self, strategy: StrategyConfig) -> None:
        self._engine.validate(strategy)

    def evaluate_entry(
        self, strategy: StrategyConfig, frame: pd.DataFrame, index: int
    ) -> TradeSignal | None:
        return self._engine.evaluate_entry(strategy, frame, index)
