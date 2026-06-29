"""Paper notifications — ATH-REL-014."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass
class PaperNotification:
    message: str
    level: str = "info"
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))


class PaperNotifier:
    """In-memory notification bus for paper trading."""

    def __init__(self) -> None:
        self._messages: list[PaperNotification] = []

    def notify(self, message: str, *, level: str = "info") -> None:
        self._messages.append(PaperNotification(message=message, level=level))

    def drain(self) -> list[PaperNotification]:
        msgs = list(self._messages)
        self._messages.clear()
        return msgs
