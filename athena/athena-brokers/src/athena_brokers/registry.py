"""Broker plugin registry."""

from __future__ import annotations

from athena_brokers.base import BrokerPlugin


class BrokerRegistry:
    def __init__(self) -> None:
        self._brokers: dict[str, BrokerPlugin] = {}

    def register(self, plugin: BrokerPlugin) -> None:
        self._brokers[plugin.broker_id] = plugin

    def get(self, broker_id: str) -> BrokerPlugin | None:
        return self._brokers.get(broker_id)

    def list_ids(self) -> list[str]:
        return sorted(self._brokers)


__all__ = ["BrokerRegistry"]
