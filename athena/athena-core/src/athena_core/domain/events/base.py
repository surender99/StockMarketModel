"""Domain event base types — ATH-REL-001 §04-Event-Bus."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import uuid4

from athena_core.domain.common.time import utc_now


@dataclass(frozen=True, slots=True)
class DomainEvent:
    """Immutable domain event envelope."""

    event_type: str
    payload: dict[str, Any] = field(default_factory=dict)
    event_id: str = field(default_factory=lambda: uuid4().hex)
    occurred_at: datetime = field(default_factory=utc_now)
    correlation_id: str | None = None
