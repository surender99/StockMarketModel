"""Research lifecycle events — PHASE 9 QREP, APS-EXP-EVENTS-001."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class ResearchEventType(str, Enum):
    """Event-driven research lifecycle — QREP CTO recommendation."""

    PROJECT_CREATED = "project_created"
    EXPERIMENT_STARTED = "experiment_started"
    EXPERIMENT_CONFIGURED = "experiment_configured"
    DATASET_SNAPSHOT_CREATED = "dataset_snapshot_created"
    FEATURE_SET_REGISTERED = "feature_set_registered"
    HYPOTHESIS_VALIDATED = "hypothesis_validated"
    EXPERIMENT_COMPLETED = "experiment_completed"
    REPORT_GENERATED = "report_generated"


@dataclass(frozen=True, slots=True)
class ResearchEvent:
    event_type: ResearchEventType
    timestamp: datetime
    payload: dict[str, Any] = field(default_factory=dict)


class ResearchEventBus:
    """In-process research event bus — APS-EXP-EVENTS-001."""

    def __init__(self) -> None:
        self._events: list[ResearchEvent] = []
        self._history: list[ResearchEvent] = []

    def publish(self, event: ResearchEvent) -> None:
        self._events.append(event)
        self._history.append(event)

    def drain(self) -> list[ResearchEvent]:
        drained = list(self._events)
        self._events.clear()
        return drained

    @property
    def history(self) -> list[ResearchEvent]:
        return list(self._history)

    def replay(self, events: list[ResearchEvent]) -> None:
        for event in events:
            self.publish(event)
