"""Execution/backtest — facade over athena_core simulation and backtest."""
from athena_execution.engine import ExecutionEngineFacade
from athena_core.application.backtest_manager import BacktestManager
from athena_core.domain.simulation.catalog import (
    SIMULATION_CATALOG,
    SimulationCatalogEntry,
    list_mvp_simulation,
)

__all__ = [
    "BacktestManager",
    "ExecutionEngineFacade",
    "SIMULATION_CATALOG",
    "SimulationCatalogEntry",
    "list_mvp_simulation",
]
