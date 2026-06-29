"""Research engine framework tests — ATH-REL-010."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pandas as pd

from athena_core.application.backtest_config import BacktestConfig, ExperimentTrackingConfig
from athena_core.application.backtest_engine import BacktestResult
from athena_core.application.bootstrap import bootstrap_athena_core
from athena_core.application.config import AthenaConfig
from athena_core.application.experiment_tracker import ExperimentTracker
from athena_core.application.research_manager import ResearchManager
from athena_core.application.research_pipeline import ResearchPipeline
from athena_core.application.result_repository import ResultRepository
from athena_core.domain.plugins import PluginType
from athena_core.domain.research import (
    ExperimentState,
    can_transition,
    compare_snapshots,
    list_pipeline_stages,
    register_builtin_research_plugins,
    reproducibility_hash,
    transition,
)
from athena_core.domain.research.dataset import DatasetSnapshot
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
        strategy=StrategyMeta(id="rs_test", version="1.0.0"),
        universe=UniverseConfig(symbols=["X"]),
        entry=EntryConfig(rules=[RuleSpec(condition="True", side="long")]),
        exit=ExitConfig(rules=[ExitRuleSpec(condition="False", reason="x")]),
        position_sizing=PositionSizingConfig(
            method="fixed_fraction",
            params={"fraction": 0.1, "max_positions": 1},
        ),
    )


def _backtest_result() -> BacktestResult:
    return BacktestResult(
        trades=[],
        equity_curve=pd.DataFrame(
            {"date": [date(2024, 1, 2)], "equity": [1_000_000.0], "cash": [1_000_000.0]}
        ),
        metrics={"sharpe": 1.2, "total_return": 0.05},
        benchmark_metrics={"benchmark_total_return": 0.0},
    )


def test_req_rs_workspace_001_create_project() -> None:
    """REQ-RS-WORKSPACE-001 — research workspace project creation."""
    mgr = ResearchManager()
    project = mgr.create_project("momentum study", description="test project")
    assert project.project_id
    assert mgr.get_project(project.project_id).name == "momentum study"
    assert len(mgr.list_projects()) == 1


def test_req_rs_experiment_001_lifecycle() -> None:
    """REQ-RS-EXPERIMENT-001 — experiment lifecycle transitions."""
    assert can_transition(ExperimentState.DRAFT, ExperimentState.RUNNING)
    assert not can_transition(ExperimentState.DRAFT, ExperimentState.VALIDATED)
    assert transition(ExperimentState.DRAFT, ExperimentState.RUNNING) == ExperimentState.RUNNING

    mgr = ResearchManager()
    project = mgr.create_project("lifecycle")
    exp = mgr.create_experiment(project.project_id, "exp-1", dataset_version="v1")
    assert exp.state == ExperimentState.DRAFT
    mgr.advance_experiment(exp.experiment_id, ExperimentState.RUNNING)
    assert mgr._experiments[exp.experiment_id].state == ExperimentState.RUNNING


def test_req_rs_dataset_001_snapshot_and_compare() -> None:
    """REQ-RS-DATASET-001 — dataset snapshots and comparison."""
    payload = {"symbols": ["A", "B"], "rows": 100}
    snap_a = DatasetSnapshot.capture("ds1", "v1", payload)
    snap_b = DatasetSnapshot.capture("ds1", "v1", payload)
    snap_c = DatasetSnapshot.capture("ds1", "v2", {"symbols": ["A"], "rows": 50})
    assert snap_a.content_hash == snap_b.content_hash
    assert reproducibility_hash(payload) == snap_a.content_hash
    cmp = compare_snapshots(snap_a, snap_c)
    assert cmp["same_content"] is False
    assert cmp["same_version"] is False


def test_req_rs_pipeline_001_run_stages() -> None:
    """REQ-RS-PIPELINE-001 — research pipeline execution."""
    mgr = ResearchManager()
    project = mgr.create_project("pipeline")
    exp = mgr.create_experiment(project.project_id, "pipe-1")
    result = mgr.run_pipeline(exp.experiment_id, context={"seed": 42})
    assert result.success
    assert len(result.stages) == 4
    assert mgr._experiments[exp.experiment_id].state == ExperimentState.COMPLETED


def test_req_rs_pipeline_001_custom_handler() -> None:
    """REQ-RS-PIPELINE-001 — custom stage handler."""
    def feature_handler(exp, ctx):
        return {"features": ["rsi", "macd"]}

    pipeline = ResearchPipeline(handlers={"feature_generation": feature_handler})
    mgr = ResearchManager(pipeline=pipeline)
    project = mgr.create_project("custom")
    exp = mgr.create_experiment(project.project_id, "custom-1")
    result = mgr.run_pipeline(exp.experiment_id)
    assert result.stages[0].output.get("features") == ["rsi", "macd"]


def test_req_rs_results_001_rank_experiments(tmp_path: Path) -> None:
    """REQ-RS-RESULTS-001 — experiment ranking."""
    tracker = ExperimentTracker(ExperimentTrackingConfig(base_path=str(tmp_path)))
    bt = BacktestConfig(start=date(2024, 1, 1), end=date(2024, 6, 1))
    for sharpe in (0.5, 1.8, 1.1):
        result = _backtest_result()
        result.metrics["sharpe"] = sharpe
        record = tracker.create_record(_strategy(), bt, result, dataset_version="v1", git_commit="abc")
        tracker.save(record)

    repo = ResultRepository(tracker)
    ranked = repo.rank("sharpe", limit=3)
    assert ranked[0]["sharpe"] == 1.8
    assert ranked[0]["rank"] == 1
    comparison = repo.compare(latest=2, metric_keys=["sharpe"])
    assert len(comparison["experiments"]) == 2


def test_research_knowledge_base() -> None:
    """ATH-REL-010 §5.6 — knowledge base entries."""
    mgr = ResearchManager()
    project = mgr.create_project("kb")
    entry = mgr.add_knowledge(project.project_id, "Finding", "RSI works", tags=["rsi"])
    entries = mgr.list_knowledge(project.project_id)
    assert len(entries) == 1
    assert entries[0].entry_id == entry.entry_id


def test_research_plugins_registered() -> None:
    """ATH-REL-010 §5.4 — pipeline stages registered."""
    ctx = bootstrap_athena_core(AthenaConfig(), wire_data=False)
    stages = list_pipeline_stages()
    assert len(stages) == 4
    plugins = ctx.plugin_registry.list(plugin_type=PluginType.REPORT, active_only=True)
    ids = {p.id for p in plugins}
    assert "research:feature_generation" in ids

    from athena_core.domain.plugins import PluginRegistry

    registry = PluginRegistry()
    count = register_builtin_research_plugins(registry)
    assert count == 4
