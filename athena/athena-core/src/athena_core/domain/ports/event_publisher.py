"""Event publishing port — ATH-REL-001 §08-Contracts."""

from __future__ import annotations

from typing import Protocol

from athena_core.domain.events.base import DomainEvent


class EventPublisherPort(Protocol):
    """Publish domain events without coupling to infrastructure."""

    def publish(self, event: DomainEvent) -> list[object]: ...
