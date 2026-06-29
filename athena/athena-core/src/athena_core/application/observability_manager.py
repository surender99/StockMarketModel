"""Observability manager — ATH-REL-019."""

from __future__ import annotations

from athena_core.domain.observability import (
    AlertManager,
    MetricsCollector,
    SLOReporter,
    Tracer,
)


class ObservabilityManager:
    """Orchestrate observability workflows."""

    def __init__(self) -> None:
        self.metrics = MetricsCollector()
        self.tracer = Tracer()
        self.alerts = AlertManager()
        self.slo = SLOReporter()

    def instrument(self, operation: str, trace_id: str = "trace-1") -> None:
        span = self.tracer.start_span(trace_id, operation)
        self.metrics.record("operation_count", 1.0, operation=operation)
        self.tracer.end_span(span, duration_ms=1.0)
