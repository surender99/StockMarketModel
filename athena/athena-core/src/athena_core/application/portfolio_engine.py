"""Portfolio evaluation engine — AES-0900, REQ-PF-001, REQ-PF-002, REQ-PF-003."""

from __future__ import annotations

import pandas as pd

from athena_core.application.portfolio_risk import (
    PortfolioLimits,
    PortfolioRiskService,
    RebalanceOrder,
)
from athena_core.domain.portfolio import (
    ExposureMetrics,
    PortfolioEvaluation,
    PortfolioState,
    PositionExposure,
)


class PortfolioEngine:
    """Evaluate portfolio state: exposure, sector weights, heat, and risk controls."""

    def __init__(self) -> None:
        self._risk = PortfolioRiskService()

    def evaluate(
        self,
        portfolio: PortfolioState,
        marks: dict[str, float],
        *,
        sector_map: dict[str, str] | None = None,
        risk_per_position: dict[str, float] | None = None,
    ) -> PortfolioEvaluation:
        """Compute portfolio analytics for current marks — REQ-PF-001."""
        equity = portfolio.equity(marks)
        if equity <= 0:
            return PortfolioEvaluation(
                equity=equity,
                cash=portfolio.cash,
                exposures=[],
                metrics=ExposureMetrics(
                    gross_exposure=0.0,
                    net_exposure=0.0,
                    cash_weight=1.0,
                    position_count=0,
                    portfolio_heat=0.0,
                    sector_weights={},
                    largest_position_weight=0.0,
                ),
            )

        sectors = sector_map or {}
        risks = risk_per_position or {}
        exposures: list[PositionExposure] = []
        sector_notionals: dict[str, float] = {}
        gross = 0.0
        heat = 0.0
        largest_weight = 0.0

        for symbol, position in portfolio.positions.items():
            mark = marks.get(symbol, position.entry_price)
            notional = position.market_value(mark)
            weight = notional / equity
            gross += abs(notional)
            largest_weight = max(largest_weight, weight)
            sector = sectors.get(symbol)
            if sector:
                sector_notionals[sector] = sector_notionals.get(sector, 0.0) + notional
            risk_pct = risks.get(symbol, abs(mark - position.entry_price) / mark if mark else 0.0)
            heat += weight * risk_pct
            exposures.append(
                PositionExposure(
                    symbol=symbol,
                    weight=weight,
                    notional=notional,
                    unrealized_pnl=position.unrealized_pnl(mark),
                    sector=sector,
                )
            )

        cash_weight = portfolio.cash / equity
        sector_weights = {s: n / equity for s, n in sector_notionals.items()}
        net_exposure = sum(e.notional for e in exposures) / equity

        metrics = ExposureMetrics(
            gross_exposure=gross / equity,
            net_exposure=net_exposure,
            cash_weight=cash_weight,
            position_count=len(exposures),
            portfolio_heat=heat,
            sector_weights=sector_weights,
            largest_position_weight=largest_weight,
        )
        return PortfolioEvaluation(
            equity=equity,
            cash=portfolio.cash,
            exposures=exposures,
            metrics=metrics,
        )

    def suggest_rebalance(
        self,
        portfolio: PortfolioState,
        marks: dict[str, float],
        target_weights: dict[str, float],
        *,
        limits: PortfolioLimits | None = None,
    ) -> list[RebalanceOrder]:
        """Rebalancing orders when drift exceeds threshold — REQ-PF-002."""
        return self._risk.suggest_rebalance(portfolio, marks, target_weights, limits=limits)

    def apply_rebalance(
        self,
        portfolio: PortfolioState,
        marks: dict[str, float],
        orders: list[RebalanceOrder],
    ) -> None:
        """Apply rebalance orders in-place — REQ-PF-002."""
        self._risk.apply_rebalance_orders(portfolio, marks, orders)

    def passes_entry_limits(
        self,
        evaluation: PortfolioEvaluation,
        candidate_symbol: str,
        candidate_weight: float,
        returns: pd.DataFrame,
        *,
        limits: PortfolioLimits | None = None,
        candidate_sector: str | None = None,
    ) -> bool:
        """Correlation and exposure gate for new entries — AES-0901."""
        limits = limits or PortfolioLimits()
        if self._risk.violates_correlation_limit(returns, candidate_symbol, limits=limits):
            return False
        return self._risk.passes_exposure_limits(
            evaluation,
            limits=limits,
            candidate_symbol=candidate_symbol,
            candidate_weight=candidate_weight,
            candidate_sector=candidate_sector,
        )
