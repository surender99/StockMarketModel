"""Backtest session manager — ATH-REL-007 §5.1."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any

from athena_core.application.backtest_config import BacktestConfig
from athena_core.application.backtest_engine import BacktestEngine, BacktestResult
from athena_core.domain.backtest.trade_journal import TradeJournalEntry, build_trade_journal
from athena_core.domain.strategy.config import StrategyConfig


@dataclass
class BacktestSession:
    """Deterministic backtest run context — FR-001."""

    session_id: str
    strategy: StrategyConfig
    config: BacktestConfig
    symbols: list[str] | None = None
    dataset_version: str = "v1"
    metadata: dict[str, Any] = field(default_factory=dict)


class BacktestManager:
    """Coordinate backtest simulations — ATH-REL-007 §5.1."""

    def __init__(self, engine: BacktestEngine) -> None:
        self._engine = engine

    def create_session(
        self,
        strategy: StrategyConfig,
        config: BacktestConfig,
        *,
        symbols: list[str] | None = None,
        dataset_version: str = "v1",
    ) -> BacktestSession:
        return BacktestSession(
            session_id=str(uuid.uuid4()),
            strategy=strategy,
            config=config,
            symbols=symbols,
            dataset_version=dataset_version,
        )

    def run(self, session: BacktestSession) -> BacktestResult:
        """Execute a backtest session deterministically — FR-001."""
        return self._engine.run(
            session.strategy,
            session.config,
            symbols=session.symbols,
            dataset_version=session.dataset_version,
        )

    @staticmethod
    def trade_journal(
        result: BacktestResult,
        strategy: StrategyConfig,
        config: BacktestConfig,
    ) -> list[TradeJournalEntry]:
        """Build trade journal from backtest result — FR-010."""
        return build_trade_journal(
            result.trades,
            strategy_id=strategy.strategy.id,
            slippage_pct=config.costs.slippage_pct,
        )
