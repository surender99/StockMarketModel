"""Observability and monitoring — ATH-REL-019."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass
class MetricPoint:
    name: str
    value: float
    labels: dict[str, str] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass
class Span:
    trace_id: str
    span_id: str
    operation: str
    duration_ms: float


@dataclass
class Alert:
    name: str
    severity: str
    message: str
    fired_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass
class SLOReport:
    service: str
    slo_target: float
    actual: float
    window_hours: int = 24

    @property
    def met(self) -> bool:
        return self.actual >= self.slo_target


class MetricsCollector:
    """Metrics collection — REQ-OBS-METRICS-001."""

    def __init__(self) -> None:
        self._points: list[MetricPoint] = []

    def record(self, name: str, value: float, **labels: str) -> None:
        self._points.append(MetricPoint(name=name, value=value, labels=labels))

    def query(self, name: str) -> list[MetricPoint]:
        return [p for p in self._points if p.name == name]


class Tracer:
    """Distributed tracing — REQ-OBS-TRACING-001."""

    def __init__(self) -> None:
        self._spans: list[Span] = []

    def start_span(self, trace_id: str, operation: str) -> Span:
        span = Span(trace_id=trace_id, span_id=f"span-{len(self._spans)}", operation=operation, duration_ms=0)
        self._spans.append(span)
        return span

    def end_span(self, span: Span, duration_ms: float) -> None:
        span.duration_ms = duration_ms


class AlertManager:
    """Alerting — REQ-OBS-ALERT-001."""

    def __init__(self) -> None:
        self._alerts: list[Alert] = []
        self._rules: dict[str, float] = {}

    def add_rule(self, metric: str, threshold: float) -> None:
        self._rules[metric] = threshold

    def evaluate(self, metrics: dict[str, float]) -> list[Alert]:
        fired: list[Alert] = []
        for metric, threshold in self._rules.items():
            value = metrics.get(metric, 0)
            if value > threshold:
                alert = Alert(name=metric, severity="warning", message=f"{metric}={value} > {threshold}")
                fired.append(alert)
                self._alerts.append(alert)
        return fired


class SLOReporter:
    """SLA/SLO reporting — REQ-OBS-SLA-001."""

    def report(self, service: str, successes: int, total: int, target: float = 0.99) -> SLOReport:
        actual = successes / total if total else 0.0
        return SLOReport(service=service, slo_target=target, actual=actual)
