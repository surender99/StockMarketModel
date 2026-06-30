"""Execution engine adapter implementing IExecutionEngine."""

from __future__ import annotations

from athena_core.application.backtest_manager import BacktestManager


class ExecutionEngineFacade:
    """Delegates to athena-core backtest manager — extraction path: ADR-0006."""

    def __init__(self, manager: BacktestManager | None = None) -> None:
        self._manager = manager

    @property
    def backtest_manager(self) -> BacktestManager:
        if self._manager is None:
            msg = "BacktestManager not configured — inject with calendar, ohlcv_repo, feature_provider"
            raise RuntimeError(msg)
        return self._manager
