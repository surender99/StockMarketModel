"""Simulation event bus — PHASE 6 unified event model."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from collections import defaultdict
from collections.abc import Callable
from typing import Any


class SimulationEventType(str, Enum):
    MARKET = "market"
    ORDER = "order"
    PORTFOLIO = "portfolio"
    CORPORATE_ACTION = "corporate_action"
    TIMER = "timer"


@dataclass(frozen=True, slots=True)
class SimulationEvent:
    """Unified simulation event — APS-REPLAY-EVENT-001 / Simulation Event Bus."""

    event_type: SimulationEventType
    timestamp: datetime
    payload: dict[str, Any] = field(default_factory=dict)


Handler = Callable[[SimulationEvent], None]


class SimulationEventBus:
    """In-process event bus for deterministic replay and live dispatch."""

    def __init__(self) -> None:
        self._events: list[SimulationEvent] = []
        self._handlers: dict[SimulationEventType, list[Handler]] = defaultdict(list)

    def subscribe(self, event_type: SimulationEventType, handler: Handler) -> None:
        self._handlers[event_type].append(handler)

    def publish(self, event: SimulationEvent) -> None:
        self._events.append(event)
        self._dispatch(event)

    def dispatch(self, event: SimulationEvent) -> None:
        """Invoke subscribers without recording the event."""
        self._dispatch(event)

    def drain(self) -> list[SimulationEvent]:
        events = list(self._events)
        self._events.clear()
        return events

    def replay(self, events: list[SimulationEvent]) -> None:
        for event in events:
            self.publish(event)

    @property
    def history(self) -> tuple[SimulationEvent, ...]:
        return tuple(self._events)

    def _dispatch(self, event: SimulationEvent) -> None:
        for handler in self._handlers[event.event_type]:
            handler(event)
