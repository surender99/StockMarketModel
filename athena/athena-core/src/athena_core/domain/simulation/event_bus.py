"""Simulation event bus — PHASE 6 unified event model."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
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


class SimulationEventBus:
    """In-process event bus for deterministic replay."""

    def __init__(self) -> None:
        self._events: list[SimulationEvent] = []

    def publish(self, event: SimulationEvent) -> None:
        self._events.append(event)

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
