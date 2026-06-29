"""Observability framework tests — ATH-REL-019."""

from __future__ import annotations

from athena_core.application.observability_manager import ObservabilityManager


def test_req_obs_metrics_001() -> None:
    """REQ-OBS-METRICS-001 — metrics."""
    mgr = ObservabilityManager()
    mgr.metrics.record("latency", 42.0)
    assert len(mgr.metrics.query("latency")) == 1


def test_req_obs_tracing_001() -> None:
    """REQ-OBS-TRACING-001 — tracing."""
    mgr = ObservabilityManager()
    mgr.instrument("backtest")
    assert mgr.tracer._spans[0].duration_ms == 1.0


def test_req_obs_alert_001() -> None:
    """REQ-OBS-ALERT-001 — alerting."""
    mgr = ObservabilityManager()
    mgr.alerts.add_rule("error_rate", 0.05)
    fired = mgr.alerts.evaluate({"error_rate": 0.1})
    assert len(fired) == 1


def test_req_obs_sla_001() -> None:
    """REQ-OBS-SLA-001 — SLA/SLO reporting."""
    mgr = ObservabilityManager()
    report = mgr.slo.report("athena-api", 99, 100, target=0.95)
    assert report.met
