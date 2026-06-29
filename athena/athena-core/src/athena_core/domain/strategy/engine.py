"""Strategy execution engine — ATH-REL-006 §5.1, FR-001–FR-015."""

from __future__ import annotations

import pandas as pd

from athena_core.domain.plugins import PluginRegistry
from athena_core.domain.strategy.composition import CompositionMode, compose_signals
from athena_core.domain.strategy.config import StrategyConfig
from athena_core.domain.strategy.risk import RiskContext, RiskLimits, within_risk_limits
from athena_core.domain.strategy.signals import SignalEngine
from athena_core.domain.strategy.strategy_plugins import resolve_strategy
from athena_core.domain.strategy.types import TradeSignal
from athena_core.domain.strategy.validation import validate_strategy_or_raise


class StrategyEngine:
    """Orchestrate signal generation and validation — ATH-REL-006 §5.1."""

    def __init__(
        self,
        registry: PluginRegistry | None = None,
        *,
        signal_engine: SignalEngine | None = None,
    ) -> None:
        self._registry = registry
        self._signals = signal_engine or SignalEngine()

    def load(self, strategy_id: str) -> StrategyConfig:
        """Load a registered strategy template by id — FR-002, FR-003."""
        if self._registry is None:
            msg = "strategy registry required to load by id"
            raise ValueError(msg)
        return resolve_strategy(self._registry, strategy_id)

    def validate(self, strategy: StrategyConfig) -> None:
        """Validate strategy configuration — ATH-REL-006 §5.10."""
        validate_strategy_or_raise(strategy)

    def evaluate_entry(
        self,
        strategy: StrategyConfig,
        frame: pd.DataFrame,
        index: int,
        *,
        composition: CompositionMode = CompositionMode.OR,
        risk_context: RiskContext | None = None,
        risk_limits: RiskLimits | None = None,
    ) -> TradeSignal | None:
        """Evaluate entry signals with optional composition and risk gating."""
        self.validate(strategy)
        if risk_context is not None and risk_limits is not None:
            if not within_risk_limits(risk_context, risk_limits):
                return None
        raw = self._signals.evaluate_entry(strategy, frame, index)
        return compose_signals(raw, composition)

    def evaluate_exit(
        self,
        strategy: StrategyConfig,
        frame: pd.DataFrame,
        index: int,
        *,
        composition: CompositionMode = CompositionMode.OR,
    ) -> TradeSignal | None:
        """Evaluate exit signals with optional composition."""
        self.validate(strategy)
        raw = self._signals.evaluate_exit(strategy, frame, index)
        return compose_signals(raw, composition)
