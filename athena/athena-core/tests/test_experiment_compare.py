"""Tests for experiment comparison — REQ-EXP-COMPARE-001."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pandas as pd
import pytest

from athena_core.application.backtest_config import BacktestConfig, ExperimentTrackingConfig
from athena_core.application.backtest_engine import BacktestResult
from athena_core.application.experiment_tracker import ExperimentTracker
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


def _strategy() -> StrategyConfig:
    return StrategyConfig(
        strategy=StrategyMeta(id="cmp_test", version="1.0.0"),
        universe=UniverseConfig(symbols=["X"]),
        entry=EntryConfig(rules=[RuleSpec(condition="True", side="long")]),
        exit=ExitConfig(rules=[ExitRuleSpec(condition="False", reason="x")]),
        position_sizing=PositionSizingConfig(
            method="fixed_fraction",
            params={"fraction": 0.1, "max_positions": 1},
        ),
    )


def _result(metrics: dict) -> BacktestResult:
    return BacktestResult(
        trades=[],
        equity_curve=pd.DataFrame(
            {"date": [date(2024, 1, 2)], "equity": [1_000_000.0], "cash": [1_000_000.0]}
        ),
        metrics=metrics,
        benchmark_metrics={},
    )


def test_compare_two_experiments(tmp_path: Path) -> None:
    tracker = ExperimentTracker(ExperimentTrackingConfig(base_path=str(tmp_path)))
    bt = BacktestConfig(start=date(2024, 1, 1), end=date(2024, 6, 1))
    r1 = tracker.create_record(
        _strategy(),
        bt,
        _result({"total_return": 0.1, "trade_count": 5}),
        dataset_version="v1",
        git_commit="a",
    )
    r2 = tracker.create_record(
        _strategy(),
        bt,
        _result({"total_return": 0.2, "trade_count": 8}),
        dataset_version="v1",
        git_commit="b",
    )
    tracker.save(r1)
    tracker.save(r2)
    comparison = tracker.compare_experiments([r1.experiment_id, r2.experiment_id])
    assert len(comparison["experiments"]) == 2
    assert comparison["experiments"][0]["total_return"] in (0.1, 0.2)


def test_compare_latest(tmp_path: Path) -> None:
    tracker = ExperimentTracker(ExperimentTrackingConfig(base_path=str(tmp_path)))
    bt = BacktestConfig(start=date(2024, 1, 1), end=date(2024, 6, 1))
    for ret in (0.05, 0.15):
        rec = tracker.create_record(
            _strategy(), bt, _result({"total_return": ret}), dataset_version="v1", git_commit="x"
        )
        tracker.save(rec)
    comparison = tracker.compare_experiments(latest=2)
    assert len(comparison["experiments"]) == 2


def test_compare_missing_id(tmp_path: Path) -> None:
    tracker = ExperimentTracker(ExperimentTrackingConfig(base_path=str(tmp_path)))
    with pytest.raises(FileNotFoundError):
        tracker.load_record("missing-id")
