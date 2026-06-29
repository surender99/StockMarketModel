"""Analytics engine — ATH-REL-009 §5.2–5.12."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any

import numpy as np
import pandas as pd

from athena_core.application.optimizer import OptimizerResult
from athena_core.application.statistics_engine import StatisticsEngine
from athena_core.application.walk_forward import WalkForwardSummary
from athena_core.domain.statistics.context import StatisticsContext
from athena_core.domain.statistics.correlation import correlation_matrix
from athena_core.domain.statistics.distribution import DistributionSummary, compute_distribution
from athena_core.domain.statistics.hypothesis import HypothesisTestResult, welch_t_test
from athena_core.domain.statistics.regression import RegressionResult, linear_regression
from athena_core.domain.statistics.risk_metrics import RiskMetrics, compute_risk_metrics


@dataclass(frozen=True)
class ConfidenceInterval:
    """Confidence interval for a metric — FR-004."""

    metric_name: str
    point_estimate: float
    lower_bound: float
    upper_bound: float
    confidence: float
    method: str


@dataclass(frozen=True)
class RobustnessSummary:
    """Robustness testing aggregate — FR-009."""

    walk_forward_folds: int
    out_of_sample_sharpe_mean: float | None
    monte_carlo_stability: float | None
    passed: bool
    notes: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class OptimizationAnalysis:
    """Parameter stability and sensitivity — FR-010."""

    trial_count: int
    best_metric: float | None
    metric_std: float | None
    stability_score: float
    sensitivity: dict[str, float]


@dataclass(frozen=True)
class AnalyticsReport:
    """Immutable analytics result bundle — FR-014."""

    performance: dict[str, Any]
    risk: RiskMetrics
    distribution: DistributionSummary
    confidence: ConfidenceInterval | None
    hypothesis: HypothesisTestResult | None
    correlation: dict[str, Any] | None
    regression: RegressionResult | None
    robustness: RobustnessSummary | None
    optimization: OptimizationAnalysis | None
    reproducibility_hash: str


class AnalyticsEngine:
    """Extended statistics and analytics — ATH-REL-009."""

    def __init__(self, statistics: StatisticsEngine | None = None) -> None:
        self._stats = statistics or StatisticsEngine()

    def analyze(
        self,
        context: StatisticsContext,
        *,
        benchmark_returns: pd.Series | None = None,
        compare_returns: pd.Series | None = None,
        confidence: float = 0.95,
    ) -> AnalyticsReport:
        """Run full analytics pipeline — FR-012."""
        perf_stats = self._stats.compute_performance(
            context.equity_curve,
            context.trades,
            initial_capital=context.initial_capital,
            trading_days_per_year=context.trading_days_per_year,
        )
        risk = compute_risk_metrics(
            context.equity_curve,
            trading_days_per_year=context.trading_days_per_year,
        )
        returns = context.daily_returns
        distribution = compute_distribution(returns)

        bootstrap = self._stats.bootstrap_sharpe(
            context.equity_curve,
            confidence=confidence,
            trading_days_per_year=context.trading_days_per_year,
        )
        conf = ConfidenceInterval(
            metric_name="sharpe",
            point_estimate=bootstrap.point_estimate,
            lower_bound=bootstrap.lower_bound,
            upper_bound=bootstrap.upper_bound,
            confidence=confidence,
            method="bootstrap",
        )

        hypothesis: HypothesisTestResult | None = None
        if compare_returns is not None and len(returns) > 1:
            aligned = pd.concat([returns, compare_returns], axis=1, join="inner").dropna()
            if len(aligned) > 2:
                hypothesis = welch_t_test(
                    aligned.iloc[:, 0].to_numpy(),
                    aligned.iloc[:, 1].to_numpy(),
                )

        corr_payload: dict[str, Any] | None = None
        bench = benchmark_returns or context.benchmark_returns
        if bench is not None and len(returns) > 1:
            frame = pd.DataFrame({"strategy": returns, "benchmark": bench})
            frame = frame.dropna()
            if not frame.empty:
                corr = correlation_matrix(frame, method="pearson")
                corr_payload = {
                    "method": corr.method,
                    "pairwise": {f"{a}|{b}": v for (a, b), v in corr.pairwise.items()},
                }

        regression: RegressionResult | None = None
        if bench is not None and len(returns) > 2:
            aligned = pd.concat([returns, bench], axis=1, join="inner").dropna()
            if len(aligned) > 2:
                regression = linear_regression(
                    aligned.iloc[:, 0],
                    aligned.iloc[:, 1].to_frame("benchmark"),
                )

        performance = self._stats.to_report_dict(perf_stats, bootstrap=bootstrap)

        payload = {
            "performance": performance,
            "risk": risk,
            "distribution": distribution,
            "confidence": conf,
            "hypothesis": hypothesis,
        }
        repro_hash = self.reproducibility_hash(payload)

        return AnalyticsReport(
            performance=performance,
            risk=risk,
            distribution=distribution,
            confidence=conf,
            hypothesis=hypothesis,
            correlation=corr_payload,
            regression=regression,
            robustness=None,
            optimization=None,
            reproducibility_hash=repro_hash,
        )

    def analyze_robustness(
        self,
        walk_forward: WalkForwardSummary | None = None,
        *,
        monte_carlo_stability: float | None = None,
        min_folds: int = 2,
    ) -> RobustnessSummary:
        """Summarize walk-forward and Monte Carlo robustness — FR-009."""
        notes: list[str] = []
        fold_count = len(walk_forward.folds) if walk_forward else 0
        oos_sharpe: float | None = None
        if walk_forward and walk_forward.folds:
            sharpes = [
                f.result.metrics.get("sharpe")
                for f in walk_forward.folds
                if isinstance(f.result.metrics.get("sharpe"), int | float)
            ]
            if sharpes:
                oos_sharpe = float(np.mean(sharpes))
        else:
            notes.append("no walk-forward folds supplied")

        passed = fold_count >= min_folds
        if monte_carlo_stability is not None and monte_carlo_stability < 0.5:
            passed = False
            notes.append("monte carlo stability below threshold")

        return RobustnessSummary(
            walk_forward_folds=fold_count,
            out_of_sample_sharpe_mean=oos_sharpe,
            monte_carlo_stability=monte_carlo_stability,
            passed=passed,
            notes=notes,
        )

    def analyze_optimization(self, result: OptimizerResult) -> OptimizationAnalysis:
        """Parameter stability from optimizer trials — FR-010."""
        trials = result.trials
        if not trials:
            return OptimizationAnalysis(
                trial_count=0,
                best_metric=None,
                metric_std=None,
                stability_score=0.0,
                sensitivity={},
            )

        scores = [t.composite_score for t in trials if t.composite_score is not None]
        best = max(scores) if scores else None
        metric_std = float(np.std(scores)) if len(scores) > 1 else 0.0
        stability = 1.0 - min(metric_std, 1.0) if scores else 0.0

        sensitivity: dict[str, float] = {}
        param_names = set()
        for t in trials:
            param_names.update(t.parameters.keys())
        for pname in param_names:
            values = [t.parameters.get(pname) for t in trials if pname in t.parameters]
            numeric = [float(v) for v in values if isinstance(v, int | float)]
            if len(numeric) > 1:
                sensitivity[pname] = float(np.std(numeric))

        return OptimizationAnalysis(
            trial_count=len(trials),
            best_metric=best,
            metric_std=metric_std if scores else None,
            stability_score=round(stability, 4),
            sensitivity=sensitivity,
        )

    @staticmethod
    def reproducibility_hash(payload: Any) -> str:
        """Deterministic hash for reproducible results — FR-014."""
        serialized = json.dumps(_to_jsonable(payload), sort_keys=True, default=str)
        return hashlib.sha256(serialized.encode()).hexdigest()[:16]


def _to_jsonable(obj: Any) -> Any:
    if hasattr(obj, "__dataclass_fields__"):
        return {k: _to_jsonable(getattr(obj, k)) for k in obj.__dataclass_fields__}
    if isinstance(obj, dict):
        return {str(k): _to_jsonable(v) for k, v in obj.items()}
    if isinstance(obj, list | tuple):
        return [_to_jsonable(v) for v in obj]
    if isinstance(obj, np.floating | np.integer):
        return float(obj)
    if isinstance(obj, pd.Series | pd.DataFrame):
        return obj.to_dict()
    return obj
