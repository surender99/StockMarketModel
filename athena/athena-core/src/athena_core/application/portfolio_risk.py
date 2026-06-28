"""Portfolio limits and rebalancing — AES-0901, REQ-PF-002."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from athena_core.domain.portfolio import PortfolioEvaluation, PortfolioState
from athena_core.domain.portfolio.positions import OpenPosition


@dataclass(frozen=True)
class PortfolioLimits:
    """Risk and concentration limits — AES-0901."""

    max_position_weight: float = 0.25
    max_sector_weight: float = 0.40
    max_correlation: float = 0.85
    rebalance_threshold: float = 0.05


@dataclass(frozen=True)
class RebalanceOrder:
    """Suggested trade to move toward target weights — REQ-PF-002."""

    symbol: str
    side: str
    weight_delta: float
    notional_delta: float


class PortfolioRiskService:
    """Correlation and exposure checks plus rebalancing — REQ-PF-002, AES-0901."""

    def correlation_matrix(self, returns: pd.DataFrame) -> pd.DataFrame:
        """Pairwise return correlations for portfolio symbols."""
        if returns.empty or returns.shape[1] < 2:
            return pd.DataFrame()
        return returns.corr()

    def max_pairwise_correlation(self, returns: pd.DataFrame) -> float:
        corr = self.correlation_matrix(returns)
        if corr.empty:
            return 0.0
        values = corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool)).stack()
        if values.empty:
            return 0.0
        arr = values.to_numpy(dtype=float)
        return float(np.max(arr))

    def violates_correlation_limit(
        self,
        returns: pd.DataFrame,
        candidate_symbol: str,
        *,
        limits: PortfolioLimits,
    ) -> bool:
        """True when *candidate_symbol* would exceed max pairwise correlation."""
        if candidate_symbol not in returns.columns or returns.shape[1] < 2:
            return False
        corr = self.correlation_matrix(returns)
        if candidate_symbol not in corr.columns:
            return False
        others = [c for c in corr.columns if c != candidate_symbol]
        if not others:
            return False
        subset = corr.loc[[candidate_symbol], others]
        max_corr = float(subset.abs().to_numpy(dtype=float).max())
        return max_corr > limits.max_correlation

    def passes_exposure_limits(
        self,
        evaluation: PortfolioEvaluation,
        *,
        limits: PortfolioLimits,
        candidate_symbol: str | None = None,
        candidate_weight: float = 0.0,
        candidate_sector: str | None = None,
    ) -> bool:
        """Check position and sector caps — AES-0901."""
        largest = evaluation.metrics.largest_position_weight
        if candidate_symbol is not None:
            largest = max(largest, candidate_weight)
        if largest > limits.max_position_weight:
            return False

        sector_weights = dict(evaluation.metrics.sector_weights)
        if candidate_sector and candidate_weight > 0:
            sector_weights[candidate_sector] = (
                sector_weights.get(candidate_sector, 0.0) + candidate_weight
            )
        return not (sector_weights and max(sector_weights.values()) > limits.max_sector_weight)

    def suggest_rebalance(
        self,
        portfolio: PortfolioState,
        marks: dict[str, float],
        target_weights: dict[str, float],
        *,
        limits: PortfolioLimits | None = None,
    ) -> list[RebalanceOrder]:
        """Orders to reduce drift beyond rebalance threshold — REQ-PF-002."""
        limits = limits or PortfolioLimits()
        equity = portfolio.equity(marks)
        if equity <= 0:
            return []

        current: dict[str, float] = {}
        for symbol, position in portfolio.positions.items():
            mark = marks.get(symbol, position.entry_price)
            current[symbol] = position.market_value(mark) / equity

        symbols = sorted(set(current) | set(target_weights))
        orders: list[RebalanceOrder] = []
        for symbol in symbols:
            cur = current.get(symbol, 0.0)
            tgt = target_weights.get(symbol, 0.0)
            delta = tgt - cur
            if abs(delta) < limits.rebalance_threshold:
                continue
            side = "buy" if delta > 0 else "sell"
            orders.append(
                RebalanceOrder(
                    symbol=symbol,
                    side=side,
                    weight_delta=round(delta, 6),
                    notional_delta=round(delta * equity, 2),
                )
            )
        return orders

    def apply_rebalance_orders(
        self,
        portfolio: PortfolioState,
        marks: dict[str, float],
        orders: list[RebalanceOrder],
    ) -> None:
        """Execute rebalance orders in-place (MVP integer shares)."""
        for order in orders:
            mark = marks.get(order.symbol)
            if mark is None or mark <= 0:
                continue
            position = portfolio.positions.get(order.symbol)
            if order.side == "sell" and position is not None:
                qty = min(
                    position.quantity,
                    max(int(abs(order.notional_delta) / mark), 1),
                )
                proceeds = qty * mark
                portfolio.cash += proceeds
                position.quantity -= qty
                if position.quantity <= 0:
                    portfolio.positions.pop(order.symbol, None)
            elif order.side == "buy":
                qty = int(abs(order.notional_delta) / mark)
                if qty <= 0:
                    continue
                cost = qty * mark
                if cost > portfolio.cash:
                    qty = int(portfolio.cash / mark)
                    cost = qty * mark
                if qty <= 0:
                    continue
                portfolio.cash -= cost
                if position is None:
                    from datetime import date

                    portfolio.positions[order.symbol] = OpenPosition(
                        symbol=order.symbol,
                        side="long",
                        entry_date=date.today(),
                        entry_price=mark,
                        quantity=qty,
                        entry_fees=0.0,
                    )
                else:
                    total_qty = position.quantity + qty
                    position.entry_price = (
                        position.entry_price * position.quantity + mark * qty
                    ) / total_qty
                    position.quantity = total_qty
