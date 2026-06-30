"""In-process event bus — APS-004, ATH-REL-001 §04."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from athena_os.errors import EventError

EventHandler = Callable[["DomainEvent"], Any]


def _utc_now() -> datetime:
    return datetime.now(tz=timezone.utc)


@dataclass(frozen=True, slots=True)
class DomainEvent:
    """Immutable domain event envelope."""

    event_type: str
    payload: dict[str, Any] = field(default_factory=dict)
    event_id: str = field(default_factory=lambda: uuid4().hex)
    occurred_at: datetime = field(default_factory=_utc_now)
    correlation_id: str | None = None


class EventBus:
    """Synchronous publish/subscribe bus for domain events."""

    def __init__(self) -> None:
        self._handlers: dict[str, list[EventHandler]] = defaultdict(list)

    def subscribe(self, event_type: str, handler: EventHandler) -> None:
        self._handlers[event_type].append(handler)

    def unsubscribe(self, event_type: str, handler: EventHandler) -> None:
        handlers = self._handlers.get(event_type, [])
        if handler in handlers:
            handlers.remove(handler)

    def publish(self, event: DomainEvent) -> list[Any]:
        results: list[Any] = []
        for handler in list(self._handlers.get(event.event_type, [])):
            try:
                results.append(handler(event))
            except Exception as exc:  # noqa: BLE001
                msg = f"event handler failed for {event.event_type}"
                raise EventError(
                    msg,
                    context={"event_type": event.event_type, "handler": handler.__name__},
                ) from exc
        return results

    def clear(self, event_type: str | None = None) -> None:
        if event_type is None:
            self._handlers.clear()
            return
        self._handlers.pop(event_type, None)

    def handler_count(self, event_type: str | None = None) -> int:
        if event_type is None:
            return sum(len(items) for items in self._handlers.values())
        return len(self._handlers.get(event_type, []))
