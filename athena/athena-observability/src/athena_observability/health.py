"""Health check stubs."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class HealthStatus:
    service: str
    healthy: bool
    detail: str = "ok"


def check_health(service: str = "athena") -> HealthStatus:
    return HealthStatus(service=service, healthy=True)


__all__ = ["HealthStatus", "check_health"]
