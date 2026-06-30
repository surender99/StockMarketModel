"""Simulation order management — REQ-APS-OMS-STATE-001."""

from __future__ import annotations

from datetime import datetime, timezone

from athena_core.domain.backtest.orders import Order, OrderStatus, validate_order
from athena_core.domain.simulation.event_bus import SimulationEvent, SimulationEventBus, SimulationEventType


class SimOrderManager:
    """OMS with state machine, cancel, and modify — APS-OMS-STATE-001."""

    def __init__(self, bus: SimulationEventBus | None = None) -> None:
        self._bus = bus
        self._orders: dict[str, Order] = {}

    def create(self, order: Order) -> Order:
        errors = validate_order(order)
        if errors:
            msg = "; ".join(errors)
            raise ValueError(msg)
        self._orders[order.order_id] = order
        self._emit(order, "created")
        return order

    def get(self, order_id: str) -> Order | None:
        return self._orders.get(order_id)

    def submit(self, order_id: str) -> Order:
        order = self._require(order_id)
        order.submit()
        self._emit(order, "submitted")
        return order

    def cancel(self, order_id: str) -> Order:
        """Cancel a pending or submitted order — APS-OMS-CANCEL-001."""
        order = self._require(order_id)
        order.transition(OrderStatus.CANCELLED)
        self._emit(order, "cancelled")
        return order

    def modify_quantity(self, order_id: str, quantity: int) -> Order:
        """Modify order quantity before fill — APS-OMS-MODIFY-001."""
        order = self._require(order_id)
        if order.status not in (OrderStatus.PENDING, OrderStatus.SUBMITTED):
            msg = f"cannot modify order in status {order.status}"
            raise ValueError(msg)
        if quantity <= 0:
            msg = "quantity must be positive"
            raise ValueError(msg)
        order.quantity = quantity
        self._emit(order, "modified")
        return order

    def fill(self, order_id: str, price: float, qty: int, fill_date) -> Order:
        order = self._require(order_id)
        order.fill(price, qty, fill_date)
        self._emit(order, "filled")
        return order

    def _require(self, order_id: str) -> Order:
        order = self._orders.get(order_id)
        if order is None:
            msg = f"unknown order: {order_id}"
            raise KeyError(msg)
        return order

    def _emit(self, order: Order, action: str) -> None:
        if self._bus is None:
            return
        ts = datetime.combine(order.signal_date, datetime.min.time(), tzinfo=timezone.utc)
        self._bus.publish(
            SimulationEvent(
                SimulationEventType.ORDER,
                ts,
                {
                    "order_id": order.order_id,
                    "symbol": order.symbol,
                    "status": order.status.value,
                    "action": action,
                },
            )
        )
