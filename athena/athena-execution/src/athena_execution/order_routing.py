"""Order routing stub — ATH-IP-000032 Order-Routing MVP."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class RouteDecision:
    venue: str
    order_id: str


class OrderRouter:
    """Routes orders to a default paper venue until broker adapters land."""

    def __init__(self, default_venue: str = "paper") -> None:
        self._default_venue = default_venue

    def route(self, order: dict[str, Any]) -> RouteDecision:
        order_id = str(order.get("id") or order.get("order_id") or "unknown")
        return RouteDecision(venue=self._default_venue, order_id=order_id)
