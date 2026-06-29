"""Statistics and analytics engine framework tests — ATH-REL-009."""

from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

import pandas as pd

from athena_core.application.analytics_engine import AnalyticsEngine
from athena_core.application.analytics_reporting import export_report, report_to_dict
from athena_core.application.bootstrap import bootstrap_athena_core
from athena_core.application.config import AthenaConfig
from athena_core.application.experiment_tracker import ExperimentRecord, ExperimentTracker
from athena_core.application.optimizer import OptimizerResult, OptimizerTrial
from athena_core.application.statistics_manager import StatisticsManager
from athena_core.application.walk_forward import WalkForwardFoldResult, WalkForwardSummary, WalkForwardWindow
from athena_core.domain.backtest import TradeRecord
from athena_core.domain.plugins import PluginType
from athena_core.domain.statistics import (
    compute_distribution,
    compute_risk_metrics,
    correlation_matrix,
    linear_regression,
    list_analytics_modules,
    mann_whitney_u_test,
    register_builtin_statistics_plugins,
    student_t_test,
    welch_t_test,
)
from athena_core.domain.statistics.context import StatisticsContext
from athena_core.domain.statistics.statistics_plugins import build_statistics_registry


def _equity_curve(n: int = 60, start: float = 100_000.0, drift: float = 0.001) -> pd.DataFrame:
    dates = [date(2024, 1, 2) + timedelta(days=i) for i in range(n)]
    equity = [start * (1 + drift) ** i for i in range(n)]
    return pd.DataFrame({"date": dates, "equity": equity, "cash": [0.0] * n})


def _trades() -> list[TradeRecord]:
    return [
        TradeRecord(
            symbol="A",
            side="long",
            entry_date=date(2024, 1, 2),
            exit_date=date(2024, 1, 10),
            entry_price=100.0,
            exit_price=110.0,
            quantity=10,
            entry_fees=1.0,
            exit_fees=1.0,
            gross_pnl=100.0,
            net_pnl=98.0,
            exit_reason="signal",
        ),
        TradeRecord(
            symbol="B",
            side="long",
            entry_date=date(2024, 1, 5),
            exit_date=date(2024, 1, 12),
            entry_price=50.0,
            exit_price=45.0,
            quantity=20,
            entry_fees=1.0,
            exit_fees=1.0,
            gross_pnl=-100.0,
            net_pnl=-102.0,
            exit_reason="stop_loss",
        ),
    ]


def test_req_stat_dist_001_distribution() -> None:
    """REQ-STAT-DIST-001 — descriptive statistics."""
    returns = _equity_curve()["equity"].pct_change().dropna()
    dist = compute_distribution(returns)
    assert dist.count > 0
    assert dist.std_dev >= 0
    assert dist.q25 <= dist.q50 <= dist.q75


def test_req_stat_risk_001_risk_metrics() -> None:
    """REQ-STAT-RISK-001 — risk analytics."""
    dates = [date(2024, 1, 2) + timedelta(days=i) for i in range(30)]
    equity = [100_000.0]
    for i in range(1, 30):
        equity.append(equity[-1] * (1.002 if i % 5 else 0.995))
    curve = pd.DataFrame({"date": dates, "equity": equity, "cash": [0.0] * 30})
    risk = compute_risk_metrics(curve)
    assert risk.max_drawdown <= 0
    assert risk.volatility >= 0
    assert risk.var_95 <= 0


def test_req_stat_hypothesis_001_t_tests() -> None:
    """REQ-STAT-HYPOTHESIS-001 — hypothesis testing."""
    a = [0.01, 0.02, -0.005, 0.015, 0.008, 0.012, -0.003]
    b = [0.005, 0.001, -0.002, 0.003, 0.004, -0.001, 0.002]
    pooled = student_t_test(a, b, equal_var=True)
    welch = welch_t_test(a, b)
    mw = mann_whitney_u_test(a, b)
    assert 0.0 <= pooled.p_value <= 1.0
    assert 0.0 <= welch.p_value <= 1.0
    assert 0.0 <= mw.p_value <= 1.0


def test_req_stat_corr_001_correlation() -> None:
    """REQ-STAT-CORR-001 — correlation analysis."""
    data = pd.DataFrame({"A": [0.01, 0.02, 0.01, 0.02], "B": [0.01, 0.02, 0.01, 0.015]})
    result = correlation_matrix(data, method="pearson")
    assert not result.matrix.empty
    assert ("A", "B") in result.pairwise


def test_req_stat_regression_001_linear() -> None:
    """REQ-STAT-REGRESSION-001 — linear regression."""
    x = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0])
    y = pd.Series([2.0, 4.1, 5.9, 8.2, 10.0])
    result = linear_regression(y, x.to_frame("x"))
    assert result.r_squared > 0.9
    assert "x" in result.coefficients


def test_statistics_registry_fr_015() -> None:
    """FR-015 — plugin-based analytics modules."""
    registry = build_statistics_registry()
    assert "performance" in registry.list_metrics()
    assert "student_t" in registry.list_tests()
    assert "json" in registry.list_report_formats()
    assert len(list_analytics_modules()) == 11


def test_bootstrap_registers_statistics_plugins() -> None:
    ctx = bootstrap_athena_core(AthenaConfig())
    models = ctx.plugin_registry.list(plugin_type=PluginType.REPORT, active_only=True)
    ids = {p.id for p in models}
    assert any(i.startswith("analytics:") for i in ids)
    assert any(i.startswith("report:") for i in ids)


def test_analytics_engine_full_pipeline() -> None:
    """FR-012 — reusable analytics APIs."""
    engine = AnalyticsEngine()
    context = StatisticsContext(
        equity_curve=_equity_curve(),
        trades=_trades(),
        initial_capital=100_000.0,
    )
    report = engine.analyze(context)
    assert report.reproducibility_hash
    assert report.performance["trade_count"] == 2
    assert report.risk.volatility >= 0
    assert report.distribution.count > 0
    assert report.confidence is not None


def test_analytics_engine_reproducibility_hash_fr_014() -> None:
    """FR-014 — reproducible results."""
    engine = AnalyticsEngine()
    context = StatisticsContext(equity_curve=_equity_curve(), trades=_trades())
    r1 = engine.analyze(context)
    r2 = engine.analyze(context)
    assert r1.reproducibility_hash == r2.reproducibility_hash


def test_req_stat_report_001_export_formats(tmp_path: Path) -> None:
    """REQ-STAT-REPORT-001 — structured reports."""
    engine = AnalyticsEngine()
    report = engine.analyze(StatisticsContext(equity_curve=_equity_curve(), trades=_trades()))
    json_out = export_report(report, "json", output_path=tmp_path / "report.json")
    assert "reproducibility_hash" in json_out
    md_out = export_report(report, "markdown")
    assert "# Analytics Report" in md_out
    csv_out = export_report(report, "csv")
    assert "section" in csv_out
    payload = report_to_dict(report)
    assert payload["performance"]["trade_count"] == 2


def test_statistics_manager_orchestration() -> None:
    manager = StatisticsManager()
    context = StatisticsContext(equity_curve=_equity_curve(), trades=_trades())
    report = manager.run_analysis(context)
    assert report.reproducibility_hash


def test_statistics_manager_robustness_fr_009() -> None:
    from athena_core.application.backtest_engine import BacktestResult

    manager = StatisticsManager()
    fold = WalkForwardFoldResult(
        window=WalkForwardWindow(0, date(2024, 1, 1), date(2024, 3, 1), date(2024, 3, 2), date(2024, 4, 1)),
        result=BacktestResult(
            trades=[],
            equity_curve=_equity_curve(10),
            metrics={"sharpe": 1.2},
            benchmark_metrics={},
        ),
    )
    summary = WalkForwardSummary(folds=[fold, fold])
    robust = manager.run_robustness(summary, monte_carlo_stability=0.8)
    assert robust.walk_forward_folds == 2
    assert robust.out_of_sample_sharpe_mean == 1.2


def test_statistics_manager_optimization_fr_010() -> None:
    manager = StatisticsManager()
    trials = [
        OptimizerTrial(0, {"period": 10}, {"sharpe": 1.0}, 1.0),
        OptimizerTrial(1, {"period": 20}, {"sharpe": 1.5}, 1.5),
        OptimizerTrial(2, {"period": 30}, {"sharpe": 0.8}, 0.8),
    ]
    analysis = manager.run_optimization_analysis(OptimizerResult(trials=trials, best_trial=trials[1]))
    assert analysis.trial_count == 3
    assert analysis.best_metric == 1.5
    assert "period" in analysis.sensitivity


def test_statistics_manager_experiment_compare(tmp_path: Path) -> None:
    """Experiment comparison with hypothesis tracking."""
    from athena_core.application.backtest_config import ExperimentTrackingConfig

    tracker = ExperimentTracker(ExperimentTrackingConfig(base_path=str(tmp_path / "experiments")))
    for sharpe in (1.2, 0.5):
        record = ExperimentRecord(
            experiment_id=f"exp_{sharpe}",
            strategy_id="test",
            strategy_version="1",
            dataset_version="v1",
            train_start="2024-01-01",
            train_end="2024-06-01",
            metrics={"sharpe": sharpe, "total_return": 0.1},
            git_commit="abc",
            created_at="2024-06-01T00:00:00+00:00",
        )
        tracker.save(record)

    manager = StatisticsManager()
    comparison = manager.compare_experiments(tracker, latest=2)
    assert len(comparison["experiments"]) == 2
    assert "hypothesis_checks" in comparison
