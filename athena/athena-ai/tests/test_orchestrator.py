"""Tests for research orchestrator — REQ-AI-ASSISTANT-001."""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

from athena_ai.application.intent_parser import RuleBasedIntentParser
from athena_ai.application.orchestrator import ResearchOrchestrator
from athena_ai.domain.intent import WorkflowAction
from athena_ai.infrastructure.config import ResearchAssistantConfig


def _config(tmp_path: Path) -> ResearchAssistantConfig:
    strategy = tmp_path / "strategy.yaml"
    return ResearchAssistantConfig(
        default_strategy_path=str(strategy),
        strategy_paths={"ema": str(strategy), "sma": str(strategy), "crossover": str(strategy)},
        ai_session_log_path=str(tmp_path / "ai_sessions"),
        default_start=date(2023, 1, 1),
        default_end=date(2023, 12, 31),
    )


def test_build_full_research_plan(tmp_path: Path) -> None:
    strategy = tmp_path / "strategy.yaml"
    strategy.write_text("strategy:\n  id: test\n  version: '1'\n", encoding="utf-8")
    config = _config(tmp_path)
    config.default_strategy_path = str(strategy)
    client = MagicMock()
    orchestrator = ResearchOrchestrator(client, config)
    intent = RuleBasedIntentParser().parse("Find best EMA for sideways markets")
    plan = orchestrator.build_plan(intent)
    actions = [step.action for step in plan.steps]
    assert WorkflowAction.SCAN in actions
    assert WorkflowAction.BACKTEST in actions
    assert WorkflowAction.WALK_FORWARD in actions
    assert WorkflowAction.COMPARE in actions
    assert plan.strategy_path == str(strategy)


def test_execute_dry_run_logs_session(tmp_path: Path) -> None:
    config = _config(tmp_path)
    client = MagicMock()
    orchestrator = ResearchOrchestrator(client, config)
    intent = RuleBasedIntentParser().parse("backtest ema strategy")
    plan = orchestrator.build_plan(intent)
    result = orchestrator.execute(plan, dry_run=True)
    assert result.dry_run is True
    assert len(result.steps_executed) == 1
    assert (tmp_path / "ai_sessions" / f"{result.session_id}.json").is_file()
    client.backtest.assert_not_called()


def test_execute_backtest_tracks_experiment_ids(tmp_path: Path) -> None:
    config = _config(tmp_path)
    client = MagicMock()
    backtest_result = MagicMock()
    backtest_result.result.metrics = {"sharpe": 1.1}
    backtest_result.result.trades = []
    backtest_result.experiment_id = "exp_test_001"
    client.backtest.return_value = backtest_result
    client.walk_forward_dict.return_value = {
        "aggregate_metrics": {"sharpe": 0.9, "max_drawdown": -0.12},
        "fold_count": 2,
    }
    client.compare_experiments.return_value = {
        "metric_keys": ["sharpe"],
        "experiments": [{"experiment_id": "exp_test_001", "sharpe": 0.9}],
    }
    orchestrator = ResearchOrchestrator(client, config)
    intent = RuleBasedIntentParser().parse("backtest ema crossover")
    plan = orchestrator.build_plan(intent)
    result = orchestrator.execute(plan, dry_run=False)
    assert "exp_test_001" in result.experiment_ids
    assert result.recommendations
    assert result.recommendations[0].validation_passed is True
    assert "exp_test_001" in result.recommendations[0].experiment_ids


def test_recommendation_requires_experiment_id(tmp_path: Path) -> None:
    config = _config(tmp_path)
    client = MagicMock()
    backtest_result = MagicMock()
    backtest_result.result.metrics = {"sharpe": 0.5}
    backtest_result.result.trades = []
    backtest_result.experiment_id = None
    client.backtest.return_value = backtest_result
    orchestrator = ResearchOrchestrator(client, config)
    intent = RuleBasedIntentParser().parse("backtest strategy")
    plan = orchestrator.build_plan(intent)
    result = orchestrator.execute(plan, dry_run=False)
    assert result.recommendations[0].validation_passed is False
