"""Walk-forward validation framework — REQ-WALK-FORWARD-001."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Any

import structlog

from athena_core.application.backtest_config import BacktestConfig
from athena_core.application.backtest_engine import BacktestEngine, BacktestResult
from athena_core.application.walk_forward_config import WalkForwardConfig
from athena_core.domain.ports.trading_calendar import TradingCalendarPort
from athena_core.domain.strategy.config import StrategyConfig

log = structlog.get_logger(__name__)

METRIC_KEYS = (
    "total_return",
    "cagr",
    "max_drawdown",
    "sharpe",
    "win_rate",
    "profit_factor",
    "trade_count",
)


@dataclass(frozen=True)
class WalkForwardWindow:
    """Train/test date boundaries for one fold — REQ-WALK-FORWARD-001."""

    fold: int
    train_start: date
    train_end: date
    test_start: date
    test_end: date


@dataclass
class WalkForwardFoldResult:
    """Backtest metrics for one test fold — REQ-WALK-FORWARD-001."""

    window: WalkForwardWindow
    result: BacktestResult


@dataclass
class WalkForwardSummary:
    """Aggregated walk-forward output — REQ-WALK-FORWARD-001."""

    folds: list[WalkForwardFoldResult] = field(default_factory=list)
    aggregate_metrics: dict[str, Any] = field(default_factory=dict)


class WalkForwardValidator:
    """Generate folds and run out-of-sample backtests — REQ-WALK-FORWARD-001."""

    def __init__(
        self,
        calendar: TradingCalendarPort,
        engine: BacktestEngine,
        config: WalkForwardConfig | None = None,
    ) -> None:
        self._calendar = calendar
        self._engine = engine
        self._config = config or WalkForwardConfig()

    def generate_windows(self, start: date, end: date) -> list[WalkForwardWindow]:
        """Build train/test windows over trading days."""
        days = self._calendar.trading_days_between(start, end)
        if len(days) < self._config.min_train_days + self._config.test_days:
            return []

        windows: list[WalkForwardWindow] = []
        fold = 0
        train_start_idx = 0

        while True:
            if self._config.mode == "expanding":
                train_end_idx = (
                    train_start_idx + self._config.train_days + fold * self._config.step_days - 1
                )
            else:
                train_end_idx = train_start_idx + self._config.train_days - 1

            test_start_idx = train_end_idx + 1
            test_end_idx = test_start_idx + self._config.test_days - 1

            if test_end_idx >= len(days):
                break
            if train_end_idx - train_start_idx + 1 < self._config.min_train_days:
                break

            windows.append(
                WalkForwardWindow(
                    fold=fold,
                    train_start=days[train_start_idx],
                    train_end=days[train_end_idx],
                    test_start=days[test_start_idx],
                    test_end=days[test_end_idx],
                )
            )
            fold += 1
            if self._config.mode == "expanding":
                train_start_idx = 0
            else:
                train_start_idx += self._config.step_days

        return windows

    def run(
        self,
        strategy: StrategyConfig,
        backtest: BacktestConfig,
        *,
        symbols: list[str] | None = None,
        dataset_version: str = "v1",
        start: date | None = None,
        end: date | None = None,
    ) -> WalkForwardSummary:
        """Run backtest on each test window and aggregate metrics."""
        range_start = start or backtest.start
        range_end = end or backtest.end
        windows = self.generate_windows(range_start, range_end)
        fold_results: list[WalkForwardFoldResult] = []

        for window in windows:
            fold_config = backtest.model_copy(
                update={"start": window.test_start, "end": window.test_end},
            )
            result = self._engine.run(
                strategy,
                fold_config,
                symbols=symbols,
                dataset_version=dataset_version,
            )
            fold_results.append(WalkForwardFoldResult(window=window, result=result))
            log.info(
                "walk_forward.fold_complete",
                fold=window.fold,
                test_start=window.test_start.isoformat(),
                test_end=window.test_end.isoformat(),
                trade_count=result.metrics.get("trade_count"),
            )

        aggregate = self._aggregate_metrics(fold_results)
        return WalkForwardSummary(folds=fold_results, aggregate_metrics=aggregate)

    @staticmethod
    def _aggregate_metrics(folds: list[WalkForwardFoldResult]) -> dict[str, Any]:
        if not folds:
            return {"fold_count": 0}

        agg: dict[str, Any] = {"fold_count": len(folds)}
        for key in METRIC_KEYS:
            values = [
                float(f.result.metrics[key])
                for f in folds
                if key in f.result.metrics and f.result.metrics[key] is not None
            ]
            if not values:
                continue
            agg[f"{key}_mean"] = sum(values) / len(values)
            agg[f"{key}_min"] = min(values)
            agg[f"{key}_max"] = max(values)
            if len(values) > 1:
                mean = agg[f"{key}_mean"]
                variance = sum((v - mean) ** 2 for v in values) / (len(values) - 1)
                agg[f"{key}_std"] = variance**0.5
        return agg
