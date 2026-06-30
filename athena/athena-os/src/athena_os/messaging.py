"""Message broker stubs — APS-008."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

MessageHandler = Callable[[dict[str, Any]], None]


@dataclass
class Message:
    topic: str
    payload: dict[str, Any] = field(default_factory=dict)
    headers: dict[str, str] = field(default_factory=dict)


class MessageBroker:
    """In-process pub/sub message broker."""

    def __init__(self) -> None:
        self._handlers: dict[str, list[MessageHandler]] = defaultdict(list)
        self._queue: list[Message] = []

    def subscribe(self, topic: str, handler: MessageHandler) -> None:
        self._handlers[topic].append(handler)

    def publish(self, message: Message) -> None:
        self._queue.append(message)
        for handler in list(self._handlers.get(message.topic, [])):
            handler(message.payload)

    def drain(self) -> list[Message]:
        messages = list(self._queue)
        self._queue.clear()
        return messages
