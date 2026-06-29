"""Statistics analytics plugin registration — ATH-REL-009 §5.1."""

from __future__ import annotations

from athena_core.domain.plugins import Plugin, PluginMetadata, PluginRegistry, PluginType
from athena_core.domain.statistics.registry import StatisticsRegistry

ANALYTICS_MODULES: dict[str, str] = {
    "performance": "Performance metrics (CAGR, Sharpe, win rate)",
    "risk": "Risk metrics (VaR, CVaR, drawdown)",
    "distribution": "Descriptive statistics (mean, skew, kurtosis)",
    "hypothesis": "Statistical hypothesis tests",
    "correlation": "Pearson, Spearman, Kendall correlation",
    "regression": "Linear regression analysis",
    "confidence": "Bootstrap confidence intervals",
    "monte_carlo": "Monte Carlo robustness simulation",
    "robustness": "Walk-forward and out-of-sample validation",
    "optimization": "Parameter sensitivity and stability",
    "reporting": "Structured report generation",
}

REPORT_FORMATS: dict[str, str] = {
    "json": "JSON structured report",
    "csv": "CSV tabular export",
    "markdown": "Markdown human-readable report",
}


def build_statistics_registry() -> StatisticsRegistry:
    """Populate default statistics registry — FR-015."""
    registry = StatisticsRegistry()
    for mid, desc in ANALYTICS_MODULES.items():
        registry.register_metric(mid, desc)
    for tid, desc in {
        "student_t": "Student t-test",
        "welch_t": "Welch unequal variance t-test",
        "mann_whitney_u": "Mann-Whitney U test",
    }.items():
        registry.register_test(tid, desc)
    for fmt, desc in REPORT_FORMATS.items():
        registry.register_report_format(fmt, desc)
    return registry


def register_builtin_statistics_plugins(registry: PluginRegistry) -> int:
    """Register analytics modules as report plugins — ATH-REL-009 §5.1."""
    plugins: list[Plugin] = []
    for module_id, description in ANALYTICS_MODULES.items():
        plugins.append(
            Plugin(
                id=f"analytics:{module_id}",
                version="0.1.0",
                plugin_type=PluginType.REPORT,
                metadata=PluginMetadata(name=module_id, description=description),
                configuration_schema={"module": module_id},
                execute=None,
            )
        )
    for fmt_id, description in REPORT_FORMATS.items():
        plugins.append(
            Plugin(
                id=f"report:{fmt_id}",
                version="0.1.0",
                plugin_type=PluginType.REPORT,
                metadata=PluginMetadata(name=fmt_id, description=description),
                configuration_schema={"format": fmt_id},
                execute=None,
            )
        )
    return registry.discover(plugins)


def list_analytics_modules() -> dict[str, str]:
    return dict(ANALYTICS_MODULES)


def list_report_formats() -> dict[str, str]:
    return dict(REPORT_FORMATS)
