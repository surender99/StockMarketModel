"""Portfolio state and exposure models — AES-0900, REQ-PF-001, REQ-PF-003."""

from __future__ import annotations

from dataclasses import dataclass, field

from athena_core.domain.portfolio.positions import OpenPosition


@dataclass
class PortfolioState:
    """Mutable portfolio snapshot — cash plus open positions."""

    cash: float
    positions: dict[str, OpenPosition] = field(default_factory=dict)

    def position_count(self) -> int:
        return len(self.positions)

    def equity(self, marks: dict[str, float]) -> float:
        mtm = sum(
            pos.quantity * marks.get(sym, pos.entry_price) for sym, pos in self.positions.items()
        )
        return self.cash + mtm

    def invested_notional(self, marks: dict[str, float]) -> float:
        return sum(
            pos.market_value(marks.get(sym, pos.entry_price)) for sym, pos in self.positions.items()
        )


@dataclass(frozen=True)
class PositionExposure:
    """Per-symbol exposure breakdown — REQ-PF-003."""

    symbol: str
    weight: float
    notional: float
    unrealized_pnl: float
    sector: str | None = None


@dataclass(frozen=True)
class ExposureMetrics:
    """Portfolio-level exposure and heat — REQ-PF-002, REQ-PF-003."""

    gross_exposure: float
    net_exposure: float
    cash_weight: float
    position_count: int
    portfolio_heat: float
    sector_weights: dict[str, float]
    largest_position_weight: float


@dataclass(frozen=True)
class PortfolioEvaluation:
    """Full portfolio analytics snapshot — AES-0900."""

    equity: float
    cash: float
    exposures: list[PositionExposure]
    metrics: ExposureMetrics
