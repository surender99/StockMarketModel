"""Tests for strategy optimizer — REQ-OPT-001."""

from __future__ import annotations

from datetime import date, timedelta
from typing import Any

import pandas as pd

from athena_core.application.backtest_config import BacktestConfig
from athena_core.application.backtest_engine import BacktestEngine, FeatureProviderPort
from athena_core.application.optimizer import StrategyOptimizer
from athena_core.application.optimizer_config import OptimizerConfig, ParameterSpec
from athena_core.application.walk_forward import WalkForwardValidator
from athena_core.application.walk_forward_config import WalkForwardConfig
from athena_core.domain.ports.ohlcv_repository import OHLCVRepositoryPort
from athena_core.domain.ports.trading_calendar import TradingCalendarPort
from athena_core.domain.strategy.config import (
    EntryConfig,
    ExitConfig,
    ExitRuleSpec,
    PositionSizingConfig,
    RuleSpec,
    StrategyConfig,
    StrategyMeta,
    UniverseConfig,
)


class _Calendar(TradingCalendarPort):
    def is_trading_day(self, d: date) -> bool:
        return d.weekday() < 5

    def trading_days_between(self, start: date, end: date) -> list[date]:
        days: list[date] = []
        cur = start
        while cur <= end:
            if self.is_trading_day(cur):
                days.append(cur)
            cur += timedelta(days=1)
        return days

    def next_trading_day(self, d: date) -> date:
        n = d + timedelta(days=1)
        while not self.is_trading_day(n):
            n += timedelta(days=1)
        return n

    def previous_trading_day(self, d: date) -> date:
        n = d - timedelta(days=1)
        while not self.is_trading_day(n):
            n -= timedelta(days=1)
        return n

    def holidays_for_year(self, year: int) -> list[date]:
        return []


class _Repo(OHLCVRepositoryPort):
    def read(self, symbol: str, start: date | None = None, end: date | None = None) -> pd.DataFrame:
        days = _Calendar().trading_days_between(date(2023, 1, 2), date(2024, 12, 31))
        close = [100 + i * 0.01 for i in range(len(days))]
        df = pd.DataFrame(
            {
                "date": days,
                "open": close,
                "high": [c + 1 for c in close],
                "low": [c - 1 for c in close],
                "close": close,
                "volume": [200_000] * len(days),
                "symbol": [symbol] * len(days),
            }
        )
        if start:
            df = df[df["date"] >= start]
        if end:
            df = df[df["date"] <= end]
        return df.reset_index(drop=True)

    def write(self, symbol: str, df: pd.DataFrame) -> int:
        return len(df)

    def exists(self, symbol: str) -> bool:
        return True

    def read_metadata(self, symbol: str) -> dict[str, Any] | None:
        return None


class _Features(FeatureProviderPort):
    def get_indicator_frame(
        self,
        symbol: str,
        indicator_type: str,
        params: dict[str, Any],
        start: date | None,
        end: date | None,
    ) -> pd.DataFrame:
        return pd.DataFrame({"date": [], "ema_9": []})


def _strategy() -> StrategyConfig:
    return StrategyConfig(
        strategy=StrategyMeta(id="opt_wf", version="1.0.0"),
        universe=UniverseConfig(symbols=["TEST"]),
        entry=EntryConfig(rules=[RuleSpec(condition="False", side="long")]),
        exit=ExitConfig(rules=[ExitRuleSpec(condition="True", reason="x")]),
        position_sizing=PositionSizingConfig(
            method="fixed_fraction",
            params={"fraction": 0.1, "max_positions": 1},
        ),
        risk={"stop_loss_pct": 0.05, "take_profit_pct": 0.15, "max_holding_days": 60},
    )


def test_optimizer_grid_search_returns_best_trial() -> None:
    cal = _Calendar()
    engine = BacktestEngine(cal, _Repo(), _Features())
    wf = WalkForwardValidator(
        cal,
        engine,
        WalkForwardConfig(train_days=60, test_days=20, step_days=20, min_train_days=60),
    )
    optimizer = StrategyOptimizer(
        wf,
        OptimizerConfig(
            method="grid",
            parameters=[
                ParameterSpec(
                    path="risk.stop_loss_pct",
                    type="choice",
                    values=[0.03, 0.07],
                ),
            ],
            objectives=["sharpe", "max_drawdown", "profit_factor"],
        ),
    )
    bt = BacktestConfig(start=date(2023, 1, 2), end=date(2024, 6, 1))
    result = optimizer.run(_strategy(), bt, symbols=["TEST"])
    assert len(result.trials) == 2
    assert result.best_trial is not None
    assert "risk.stop_loss_pct" in result.best_trial.parameters


def test_optimizer_random_search_respects_max_trials() -> None:
    cal = _Calendar()
    engine = BacktestEngine(cal, _Repo(), _Features())
    wf = WalkForwardValidator(
        cal,
        engine,
        WalkForwardConfig(train_days=60, test_days=20, step_days=20, min_train_days=60),
    )
    optimizer = StrategyOptimizer(
        wf,
        OptimizerConfig(
            method="random",
            max_trials=5,
            random_seed=1,
            parameters=[
                ParameterSpec(
                    path="risk.stop_loss_pct", type="float", min=0.03, max=0.1, step=0.01
                ),
            ],
        ),
    )
    bt = BacktestConfig(start=date(2023, 1, 2), end=date(2024, 6, 1))
    result = optimizer.run(_strategy(), bt, symbols=["TEST"])
    assert len(result.trials) == 5


def test_optimizer_bayesian_search_runs() -> None:
    cal = _Calendar()
    engine = BacktestEngine(cal, _Repo(), _Features())
    wf = WalkForwardValidator(
        cal,
        engine,
        WalkForwardConfig(train_days=60, test_days=20, step_days=20, min_train_days=60),
    )
    optimizer = StrategyOptimizer(
        wf,
        OptimizerConfig(
            method="bayesian",
            max_trials=4,
            random_seed=42,
            parameters=[
                ParameterSpec(path="risk.stop_loss_pct", type="choice", values=[0.04, 0.06, 0.08]),
            ],
        ),
    )
    bt = BacktestConfig(start=date(2023, 1, 2), end=date(2024, 6, 1))
    result = optimizer.run(_strategy(), bt, symbols=["TEST"])
    assert len(result.trials) == 4
    assert result.method in {"bayesian", "bayesian+optuna"}
