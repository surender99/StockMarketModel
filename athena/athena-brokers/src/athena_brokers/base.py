"""Broker plugin protocol."""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class BrokerPlugin(Protocol):
    """Minimal broker adapter contract."""

    broker_id: str

    def connect(self, credentials: dict[str, str]) -> None: ...

    def place_order(self, order: dict[str, Any]) -> str: ...

    def disconnect(self) -> None: ...


__all__ = ["BrokerPlugin"]
