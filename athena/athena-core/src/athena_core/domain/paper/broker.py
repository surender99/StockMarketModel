"""Paper broker — ATH-REL-014, REQ-PAPER-BROKER-001."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from athena_core.domain.paper.orders import OrderSide, OrderStatus, PaperOrder
from athena_core.domain.paper.portfolio import PaperPortfolio
from athena_core.domain.paper.positions import PaperPosition


@dataclass
class PaperAccount:
    """Paper trading account."""

    account_id: str
    portfolio: PaperPortfolio
    orders: list[PaperOrder] = field(default_factory=list)


class PaperBroker:
    """Simulated broker — REQ-PAPER-BROKER-001."""

    def __init__(self, account_id: str, initial_cash: float = 100_000.0) -> None:
        self.account = PaperAccount(
            account_id=account_id,
            portfolio=PaperPortfolio(cash=initial_cash),
        )

    def submit_order(self, order: PaperOrder, *, fill_price: float) -> PaperOrder:
        portfolio = self.account.portfolio
        cost = fill_price * order.quantity
        if order.side == OrderSide.BUY and cost > portfolio.cash:
            order.status = OrderStatus.REJECTED
            self.account.orders.append(order)
            return order
        if order.side == OrderSide.SELL:
            pos = portfolio.get_position(order.symbol)
            if pos is None or pos.quantity < order.quantity:
                order.status = OrderStatus.REJECTED
                self.account.orders.append(order)
                return order
        order.status = OrderStatus.FILLED
        order.fill_price = fill_price
        self._apply_fill(order)
        self.account.orders.append(order)
        return order

    def _apply_fill(self, order: PaperOrder) -> None:
        portfolio = self.account.portfolio
        assert order.fill_price is not None
        cost = order.fill_price * order.quantity
        if order.side == OrderSide.BUY:
            portfolio.cash -= cost
            pos = portfolio.positions.get(order.symbol)
            if pos is None:
                portfolio.positions[order.symbol] = PaperPosition(
                    order.symbol, order.quantity, order.fill_price
                )
            else:
                pos.update(order.quantity, order.fill_price)
        else:
            portfolio.cash += cost
            pos = portfolio.positions.get(order.symbol)
            if pos:
                pos.update(-order.quantity, order.fill_price)
                if pos.quantity == 0:
                    del portfolio.positions[order.symbol]

    def snapshot(self) -> dict[str, Any]:
        return {
            "account_id": self.account.account_id,
            "cash": self.account.portfolio.cash,
            "positions": {
                s: {"quantity": p.quantity, "avg_price": p.avg_price}
                for s, p in self.account.portfolio.positions.items()
            },
            "order_count": len(self.account.orders),
        }
