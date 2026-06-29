"""Paper portfolio — ATH-REL-014."""

from __future__ import annotations

from dataclasses import dataclass, field

from athena_core.domain.paper.positions import PaperPosition


@dataclass
class PaperPortfolio:
    """Paper portfolio state."""

    cash: float
    positions: dict[str, PaperPosition] = field(default_factory=dict)

    def equity(self, prices: dict[str, float] | None = None) -> float:
        total = self.cash
        for symbol, pos in self.positions.items():
            price = prices.get(symbol, pos.avg_price) if prices else pos.avg_price
            total += pos.quantity * price
        return total

    def get_position(self, symbol: str) -> PaperPosition | None:
        return self.positions.get(symbol)
