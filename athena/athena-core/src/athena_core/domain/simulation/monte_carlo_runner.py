"""Monte Carlo simulation runner — REQ-APS-MC-RETURNS-001."""

from __future__ import annotations

import pandas as pd

from athena_core.application.statistics_engine import MonteCarloResult, StatisticsEngine


class MonteCarloRunner:
    """Return-sampling Monte Carlo built on StatisticsEngine — APS-MC-RETURNS-001."""

    def __init__(self, engine: StatisticsEngine | None = None) -> None:
        self._engine = engine or StatisticsEngine()

    def run_return_sampling(
        self,
        equity_curve: pd.DataFrame,
        *,
        n_simulations: int = 1000,
        horizon_days: int | None = None,
        seed: int = 42,
    ) -> MonteCarloResult:
        return self._engine.monte_carlo_returns(
            equity_curve,
            n_simulations=n_simulations,
            horizon_days=horizon_days,
            seed=seed,
        )
