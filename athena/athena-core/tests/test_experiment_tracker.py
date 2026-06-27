"""Tests for experiment tracking — REQ-EXP-TRACK-001."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import pandas as pd
import pytest

from athena_core.application.backtest_config import BacktestConfig, ExperimentTrackingConfig
from athena_core.application.backtest_engine import BacktestResult
from athena_core.application.experiment_tracker import ExperimentRecord, ExperimentTracker
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
        strategy=StrategyMeta(id="exp_test", version="1.0.0"),
        universe=UniverseConfig(symbols=["X"]),
        entry=EntryConfig(rules=[RuleSpec(condition="True", side="long")]),
        exit=ExitConfig(rules=[ExitRuleSpec(condition="False", reason="x")]),
        position_sizing=PositionSizingConfig(
            method="fixed_fraction",
            params={"fraction": 0.1, "max_positions": 1},
        ),
    )


def _result() -> BacktestResult:
    return BacktestResult(
        trades=[],
        equity_curve=pd.DataFrame({"date": [date(2024, 1, 2)], "equity": [1_000_000.0], "cash": [1_000_000.0]}),
        metrics={"total_return": 0.0, "trade_count": 0},
        benchmark_metrics={"benchmark_total_return": 0.0},
    )


def test_record_serialization(tmp_path: Path) -> None:
    tracker = ExperimentTracker(ExperimentTrackingConfig(base_path=str(tmp_path)))
    record = tracker.create_record(
        _strategy(),
        BacktestConfig(start=date(2024, 1, 1), end=date(2024, 6, 1)),
        _result(),
        dataset_version="v1",
        git_commit="abc123",
    )
    path = tracker.save(record)
    loaded = json.loads(path.read_text(encoding="utf-8"))
    assert loaded["strategy_id"] == "exp_test"
    assert loaded["git_commit"] == "abc123"
    assert "total_return" in loaded["metrics"]


def test_git_commit_null_when_unavailable(tmp_path: Path) -> None:
    tracker = ExperimentTracker(ExperimentTrackingConfig(base_path=str(tmp_path), auto_capture_git=False))
    record = tracker.create_record(
        _strategy(),
        BacktestConfig(start=date(2024, 1, 1), end=date(2024, 6, 1)),
        _result(),
        dataset_version="v1",
        git_commit=None,
    )
    assert record.git_commit is None


def test_experiment_id_unique(tmp_path: Path) -> None:
    tracker = ExperimentTracker(ExperimentTrackingConfig(base_path=str(tmp_path)))
    bt = BacktestConfig(start=date(2024, 1, 1), end=date(2024, 6, 1))
    r1 = tracker.create_record(_strategy(), bt, _result(), dataset_version="v1", git_commit="a")
    r2 = tracker.create_record(_strategy(), bt, _result(), dataset_version="v1", git_commit="a")
    assert r1.experiment_id != r2.experiment_id


def test_required_field_validation(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        ExperimentRecord(
            experiment_id="x",
            strategy_id="",
            strategy_version="1",
            dataset_version="v1",
            train_start="2024-01-01",
            train_end="2024-06-01",
            metrics={},
            git_commit=None,
            created_at="2024-01-01T00:00:00+00:00",
        )


def test_list_records(tmp_path: Path) -> None:
    tracker = ExperimentTracker(ExperimentTrackingConfig(base_path=str(tmp_path)))
    record = tracker.create_record(
        _strategy(),
        BacktestConfig(start=date(2024, 1, 1), end=date(2024, 6, 1)),
        _result(),
        dataset_version="v1",
        git_commit="deadbeef",
    )
    tracker.save(record)
    listed = tracker.list_records()
    assert len(listed) == 1
    assert listed[0].strategy_id == "exp_test"
