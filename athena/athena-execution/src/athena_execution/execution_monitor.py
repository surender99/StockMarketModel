"""Execution lifecycle monitor — ATH-IP-000033 Execution-Monitor MVP."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum


class ExecutionState(StrEnum):
    PENDING = "pending"
    SUBMITTED = "submitted"
    FILLED = "filled"
    REJECTED = "rejected"


@dataclass
class ExecutionRecord:
    order_id: str
    state: ExecutionState = ExecutionState.PENDING
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class ExecutionMonitor:
    """Tracks order execution state transitions in memory."""

    def __init__(self) -> None:
        self._records: dict[str, ExecutionRecord] = {}

    def track(self, order_id: str) -> ExecutionRecord:
        record = ExecutionRecord(order_id=order_id)
        self._records[order_id] = record
        return record

    def transition(self, order_id: str, state: ExecutionState) -> ExecutionRecord:
        record = self._records.setdefault(order_id, ExecutionRecord(order_id=order_id))
        record.state = state
        record.updated_at = datetime.now(timezone.utc)
        return record

    def get(self, order_id: str) -> ExecutionRecord | None:
        return self._records.get(order_id)
