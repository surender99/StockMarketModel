"""Analytics reporting engine — ATH-REL-009 §5.13, REQ-STAT-REPORT-001."""

from __future__ import annotations

import csv
import json
from io import StringIO
from pathlib import Path
from typing import Any

from athena_core.application.analytics_engine import AnalyticsReport


def export_report(
    report: AnalyticsReport,
    fmt: str = "json",
    *,
    output_path: str | Path | None = None,
) -> str:
    """Export analytics report — REQ-STAT-REPORT-001."""
    payload = report_to_dict(report)
    if fmt == "json":
        content = json.dumps(payload, indent=2, default=str)
    elif fmt == "csv":
        content = _to_csv(payload)
    elif fmt == "markdown":
        content = _to_markdown(payload)
    else:
        raise ValueError(f"Unsupported report format: {fmt}")

    if output_path is not None:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    return content


def report_to_dict(report: AnalyticsReport) -> dict[str, Any]:
    """Serialize analytics report to dict — FR-011."""
    return {
        "reproducibility_hash": report.reproducibility_hash,
        "performance": report.performance,
        "risk": {
            "max_drawdown": report.risk.max_drawdown,
            "average_drawdown": report.risk.average_drawdown,
            "max_drawdown_duration": report.risk.max_drawdown_duration,
            "volatility": report.risk.volatility,
            "downside_volatility": report.risk.downside_volatility,
            "var_95": report.risk.var_95,
            "cvar_95": report.risk.cvar_95,
            "tail_ratio": report.risk.tail_ratio,
        },
        "distribution": {
            "mean": report.distribution.mean,
            "median": report.distribution.median,
            "std_dev": report.distribution.std_dev,
            "skewness": report.distribution.skewness,
            "kurtosis": report.distribution.kurtosis,
            "count": report.distribution.count,
        },
        "confidence": _serialize_confidence(report),
        "hypothesis": _serialize_hypothesis(report),
        "correlation": report.correlation,
        "regression": _serialize_regression(report),
        "robustness": _serialize_robustness(report),
        "optimization": _serialize_optimization(report),
    }


def _serialize_confidence(report: AnalyticsReport) -> dict[str, Any] | None:
    if report.confidence is None:
        return None
    c = report.confidence
    return {
        "metric": c.metric_name,
        "point_estimate": c.point_estimate,
        "lower_bound": c.lower_bound,
        "upper_bound": c.upper_bound,
        "confidence": c.confidence,
        "method": c.method,
    }


def _serialize_hypothesis(report: AnalyticsReport) -> dict[str, Any] | None:
    if report.hypothesis is None:
        return None
    h = report.hypothesis
    return {
        "test": h.test_name,
        "statistic": h.statistic,
        "p_value": h.p_value,
        "significant": h.significant,
        "alpha": h.alpha,
    }


def _serialize_regression(report: AnalyticsReport) -> dict[str, Any] | None:
    if report.regression is None:
        return None
    r = report.regression
    return {
        "coefficients": r.coefficients,
        "intercept": r.intercept,
        "r_squared": r.r_squared,
        "adjusted_r_squared": r.adjusted_r_squared,
        "n_observations": r.n_observations,
    }


def _serialize_robustness(report: AnalyticsReport) -> dict[str, Any] | None:
    if report.robustness is None:
        return None
    rb = report.robustness
    return {
        "walk_forward_folds": rb.walk_forward_folds,
        "out_of_sample_sharpe_mean": rb.out_of_sample_sharpe_mean,
        "monte_carlo_stability": rb.monte_carlo_stability,
        "passed": rb.passed,
        "notes": rb.notes,
    }


def _serialize_optimization(report: AnalyticsReport) -> dict[str, Any] | None:
    if report.optimization is None:
        return None
    opt = report.optimization
    return {
        "trial_count": opt.trial_count,
        "best_metric": opt.best_metric,
        "metric_std": opt.metric_std,
        "stability_score": opt.stability_score,
        "sensitivity": opt.sensitivity,
    }


def _to_csv(payload: dict[str, Any]) -> str:
    buf = StringIO()
    writer = csv.writer(buf)
    writer.writerow(["section", "key", "value"])
    for section, data in payload.items():
        if isinstance(data, dict):
            for key, value in data.items():
                writer.writerow([section, key, value])
        else:
            writer.writerow(["root", section, data])
    return buf.getvalue()


def _to_markdown(payload: dict[str, Any]) -> str:
    lines = ["# Analytics Report", "", f"**Reproducibility:** `{payload.get('reproducibility_hash', '')}`", ""]
    perf = payload.get("performance", {})
    if perf:
        lines.extend(["## Performance", ""])
        for key, value in perf.items():
            if not isinstance(value, dict):
                lines.append(f"- **{key}:** {value}")
        lines.append("")
    risk = payload.get("risk", {})
    if risk:
        lines.extend(["## Risk", ""])
        for key, value in risk.items():
            lines.append(f"- **{key}:** {value}")
        lines.append("")
    return "\n".join(lines)
