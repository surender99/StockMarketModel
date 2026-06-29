"""Signal engine — ATH-REL-006 §5.3, FR-009."""

from __future__ import annotations

import pandas as pd

from athena_core.domain.strategy.config import StrategyConfig
from athena_core.domain.strategy.expression import evaluate_condition_at_index
from athena_core.domain.strategy.indicators import indicator_column_name
from athena_core.domain.strategy.types import SignalDirection, TradeSignal


def _indicator_columns(strategy: StrategyConfig) -> dict[str, str]:
    return {spec.id: indicator_column_name(spec) for spec in strategy.indicators}


class SignalEngine:
    """Generate entry/exit signals from strategy rules — ATH-REL-006 §5.3."""

    def evaluate_entry(
        self,
        strategy: StrategyConfig,
        frame: pd.DataFrame,
        index: int,
    ) -> list[TradeSignal]:
        """Evaluate entry rules at a single bar index."""
        cols = _indicator_columns(strategy)
        signals: list[TradeSignal] = []
        for rule in strategy.entry.rules:
            if evaluate_condition_at_index(rule.condition, frame, cols, index):
                direction = SignalDirection.BUY if rule.side == "long" else SignalDirection.SELL
                signals.append(
                    TradeSignal(
                        direction=direction,
                        confidence=1.0,
                        reason=f"entry:{rule.side}",
                        side=rule.side,
                    )
                )
        return signals

    def evaluate_exit(
        self,
        strategy: StrategyConfig,
        frame: pd.DataFrame,
        index: int,
    ) -> list[TradeSignal]:
        """Evaluate exit rules at a single bar index."""
        cols = _indicator_columns(strategy)
        signals: list[TradeSignal] = []
        for rule in strategy.exit.rules:
            if evaluate_condition_at_index(rule.condition, frame, cols, index):
                signals.append(
                    TradeSignal(
                        direction=SignalDirection.SELL,
                        confidence=1.0,
                        reason=f"exit:{rule.reason}",
                    )
                )
        return signals

    def best_entry_signal(
        self,
        strategy: StrategyConfig,
        frame: pd.DataFrame,
        index: int,
    ) -> TradeSignal | None:
        """Return highest-confidence entry signal or None."""
        signals = self.evaluate_entry(strategy, frame, index)
        if not signals:
            return None
        return max(signals, key=lambda s: s.confidence)
