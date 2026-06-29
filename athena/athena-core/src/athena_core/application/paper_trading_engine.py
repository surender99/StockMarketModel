"""Paper trading engine — ATH-REL-014, FR-012."""

from __future__ import annotations

from athena_core.domain.paper.broker import PaperBroker
from athena_core.domain.paper.execution import ExecutionSimulator
from athena_core.domain.paper.notifications import PaperNotifier
from athena_core.domain.paper.orders import OrderSide, PaperOrder
from athena_core.domain.paper.risk import PaperRiskControls


class PaperTradingEngine:
    """Orchestrate paper trading workflows."""

    def __init__(
        self,
        account_id: str = "paper-001",
        *,
        initial_cash: float = 100_000.0,
        risk: PaperRiskControls | None = None,
    ) -> None:
        self.broker = PaperBroker(account_id, initial_cash=initial_cash)
        self.executor = ExecutionSimulator()
        self.risk = risk or PaperRiskControls()
        self.notifier = PaperNotifier()

    def place_order(
        self,
        symbol: str,
        side: OrderSide,
        quantity: float,
        market_price: float,
    ) -> PaperOrder:
        order = PaperOrder(symbol=symbol, side=side, quantity=quantity)
        fill_price = self.executor.simulate_fill(order, market_price)
        equity = self.broker.account.portfolio.equity({symbol: market_price})
        ok, reason = self.risk.validate(order, equity, fill_price)
        if not ok:
            from athena_core.domain.paper.orders import OrderStatus

            order.status = OrderStatus.REJECTED
            self.notifier.notify(f"Order rejected: {reason}", level="warning")
            self.broker.account.orders.append(order)
            return order
        filled = self.broker.submit_order(order, fill_price=fill_price)
        self.notifier.notify(f"Filled {side} {quantity} {symbol} @ {fill_price:.2f}")
        return filled
