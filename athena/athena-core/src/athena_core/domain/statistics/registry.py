"""Statistics module registry — ATH-REL-009 §5.1."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class StatisticsRegistry:
    """Registry for analytics modules and report formats — FR-015."""

    metrics: dict[str, str] = field(default_factory=dict)
    tests: dict[str, str] = field(default_factory=dict)
    report_formats: dict[str, str] = field(default_factory=dict)
    _handlers: dict[str, Callable[..., Any]] = field(default_factory=dict)

    def register_metric(self, metric_id: str, description: str) -> None:
        self.metrics[metric_id] = description

    def register_test(self, test_id: str, description: str) -> None:
        self.tests[test_id] = description

    def register_report_format(self, fmt_id: str, description: str) -> None:
        self.report_formats[fmt_id] = description

    def register_handler(self, handler_id: str, handler: Callable[..., Any]) -> None:
        self._handlers[handler_id] = handler

    def get_handler(self, handler_id: str) -> Callable[..., Any] | None:
        return self._handlers.get(handler_id)

    def list_metrics(self) -> dict[str, str]:
        return dict(self.metrics)

    def list_tests(self) -> dict[str, str]:
        return dict(self.tests)

    def list_report_formats(self) -> dict[str, str]:
        return dict(self.report_formats)
