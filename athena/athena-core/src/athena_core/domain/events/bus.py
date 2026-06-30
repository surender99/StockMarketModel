"""In-process event bus — delegates to athena-os (APS-004)."""

from __future__ import annotations

from typing import Any

from athena_os.event_bus import DomainEvent, EventHandler
from athena_os.event_bus import EventBus as _EventBus
from athena_os.errors import EventError

from athena_core.domain.errors import AthenaError, ErrorCode

__all__ = ["DomainEvent", "EventBus", "EventHandler"]


class EventBus(_EventBus):
    """Athena-core EventBus — maps athena-os EventError to AthenaError for backward compatibility."""

    def publish(self, event: DomainEvent) -> list[Any]:
        try:
            return super().publish(event)
        except EventError as exc:
            raise AthenaError(
                str(exc),
                code=ErrorCode.EVENT,
                context=exc.context,
            ) from exc
