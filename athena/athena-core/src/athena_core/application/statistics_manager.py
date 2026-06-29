"""Statistics manager orchestration — ATH-REL-009 §5.1."""

from __future__ import annotations

from typing import Any

from athena_core.application.analytics_engine import AnalyticsEngine, AnalyticsReport
from athena_core.application.analytics_reporting import export_report
from athena_core.application.experiment_tracker import ExperimentRecord, ExperimentTracker
from athena_core.application.optimizer import OptimizerResult
from athena_core.application.statistics_engine import StatisticsEngine
from athena_core.application.walk_forward import WalkForwardSummary
from athena_core.domain.statistics.context import StatisticsContext
from athena_core.domain.statistics.registry import StatisticsRegistry
from athena_core.domain.statistics.statistics_plugins import build_statistics_registry


class StatisticsManager:
    """Orchestrate statistics and analytics workflows — FR-012."""

    def __init__(
        self,
        *,
        statistics: StatisticsEngine | None = None,
        analytics: AnalyticsEngine | None = None,
        registry: StatisticsRegistry | None = None,
    ) -> None:
        self._stats = statistics or StatisticsEngine()
        self._analytics = analytics or AnalyticsEngine(self._stats)
        self._registry = registry or build_statistics_registry()

    @property
    def registry(self) -> StatisticsRegistry:
        return self._registry

    def run_analysis(
        self,
        context: StatisticsContext,
        *,
        benchmark_returns: Any = None,
        compare_returns: Any = None,
    ) -> AnalyticsReport:
        """Execute full analytics pipeline."""
        return self._analytics.analyze(
            context,
            benchmark_returns=benchmark_returns,
            compare_returns=compare_returns,
        )

    def run_robustness(
        self,
        walk_forward: WalkForwardSummary | None = None,
        *,
        monte_carlo_stability: float | None = None,
    ):
        return self._analytics.analyze_robustness(
            walk_forward,
            monte_carlo_stability=monte_carlo_stability,
        )

    def run_optimization_analysis(self, result: OptimizerResult):
        return self._analytics.analyze_optimization(result)

    def compare_experiments(
        self,
        tracker: ExperimentTracker,
        *,
        experiment_ids: list[str] | None = None,
        latest: int | None = None,
    ) -> dict[str, Any]:
        """Compare persisted experiments with statistical context — FR-003."""
        comparison = tracker.compare_experiments(experiment_ids=experiment_ids, latest=latest)
        records = (
            [tracker.load_record(eid) for eid in experiment_ids]
            if experiment_ids
            else tracker.load_latest(latest or 2)
        )
        hypothesis_results: list[dict[str, Any]] = []
        if len(records) >= 2:
            metrics_a = records[0].metrics.get("sharpe")
            metrics_b = records[1].metrics.get("sharpe")
            if isinstance(metrics_a, int | float) and isinstance(metrics_b, int | float):
                from athena_core.domain.statistics.hypothesis import student_t_test

                test = student_t_test([metrics_a], [metrics_b])
                hypothesis_results.append(
                    {
                        "test": test.test_name,
                        "p_value": test.p_value,
                        "significant": test.significant,
                    }
                )
        comparison["hypothesis_checks"] = hypothesis_results
        return comparison

    def export(
        self,
        report: AnalyticsReport,
        fmt: str = "json",
        *,
        output_path: str | None = None,
    ) -> str:
        """Generate structured report — FR-011."""
        return export_report(report, fmt, output_path=output_path)

    def enrich_experiment(
        self,
        record: ExperimentRecord,
        report: AnalyticsReport,
    ) -> ExperimentRecord:
        """Attach analytics summary to experiment record for reproducibility."""
        enriched_metrics = dict(record.metrics)
        enriched_metrics["analytics_hash"] = report.reproducibility_hash
        enriched_metrics["risk_volatility"] = report.risk.volatility
        enriched_metrics["distribution_skew"] = report.distribution.skewness
        return record.model_copy(update={"metrics": enriched_metrics})
