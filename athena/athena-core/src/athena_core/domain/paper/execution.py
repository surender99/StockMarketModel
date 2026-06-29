"""Execution simulator — ATH-REL-014, REQ-PAPER-EXECUTION-001."""

from __future__ import annotations

from dataclasses import dataclass

from athena_core.domain.paper.orders import PaperOrder


@dataclass
class ExecutionSimulator:
    """Simulate order fills with slippage."""

    slippage_bps: float = 5.0

    def simulate_fill(self, order: PaperOrder, market_price: float) -> float:
        slip = market_price * (self.slippage_bps / 10_000)
        if order.limit_price is not None:
            return order.limit_price
        return market_price + slip if order.side.value == "buy" else market_price - slip
