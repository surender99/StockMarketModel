"""Paper risk controls — ATH-REL-014, REQ-PAPER-RISK-001."""

from __future__ import annotations

from dataclasses import dataclass

from athena_core.domain.paper.orders import PaperOrder, OrderSide


@dataclass
class PaperRiskControls:
    """Pre-trade risk checks."""

    max_position_pct: float = 0.25
    max_order_value: float = 50_000.0

    def validate(self, order: PaperOrder, portfolio_equity: float, fill_price: float) -> tuple[bool, str]:
        order_value = order.quantity * fill_price
        if order_value > self.max_order_value:
            return False, "order exceeds max order value"
        if order.side == OrderSide.BUY and portfolio_equity > 0:
            if order_value / portfolio_equity > self.max_position_pct:
                return False, "order exceeds max position size"
        return True, "ok"
