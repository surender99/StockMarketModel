"""Statistics domain exports — ATH-REL-009."""

from athena_core.domain.statistics.context import StatisticsContext
from athena_core.domain.statistics.correlation import CorrelationResult, correlation_matrix, cross_correlation
from athena_core.domain.statistics.distribution import DistributionSummary, compute_distribution
from athena_core.domain.statistics.hypothesis import (
    HypothesisTestResult,
    mann_whitney_u_test,
    student_t_test,
    welch_t_test,
)
from athena_core.domain.statistics.regression import RegressionResult, linear_regression
from athena_core.domain.statistics.registry import StatisticsRegistry
from athena_core.domain.statistics.risk_metrics import RiskMetrics, compute_risk_metrics
from athena_core.domain.statistics.statistics_plugins import (
    build_statistics_registry,
    list_analytics_modules,
    list_report_formats,
    register_builtin_statistics_plugins,
)

__all__ = [
    "CorrelationResult",
    "DistributionSummary",
    "HypothesisTestResult",
    "RegressionResult",
    "RiskMetrics",
    "StatisticsContext",
    "StatisticsRegistry",
    "build_statistics_registry",
    "compute_distribution",
    "compute_risk_metrics",
    "correlation_matrix",
    "cross_correlation",
    "linear_regression",
    "list_analytics_modules",
    "list_report_formats",
    "mann_whitney_u_test",
    "register_builtin_statistics_plugins",
    "student_t_test",
    "welch_t_test",
]
