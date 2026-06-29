"""Multi-portfolio manager — ATH-REL-008 §5.1, §5.12."""

from __future__ import annotations

import uuid
from typing import Any

import pandas as pd

from athena_core.application.portfolio_engine import PortfolioEngine
from athena_core.domain.portfolio.allocation import compute_allocation_weights
from athena_core.domain.portfolio.context import PortfolioConfig, PortfolioContext
from athena_core.domain.portfolio.models import PortfolioState
from athena_core.domain.portfolio.risk_budget import passes_risk_budget
from athena_core.domain.portfolio.snapshot import PortfolioSnapshot


class PortfolioManager:
    """Manage multiple portfolios — FR-001, FR-014."""

    def __init__(self, engine: PortfolioEngine | None = None) -> None:
        self._engine = engine or PortfolioEngine()
        self._portfolios: dict[str, PortfolioContext] = {}
        self._snapshots: list[PortfolioSnapshot] = []

    def create_portfolio(
        self,
        name: str,
        *,
        config: PortfolioConfig | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> PortfolioContext:
        """Create a new managed portfolio — FR-001."""
        cfg = config or PortfolioConfig()
        portfolio_id = str(uuid.uuid4())
        ctx = PortfolioContext(
            portfolio_id=portfolio_id,
            name=name,
            config=cfg,
            state=PortfolioState(cash=cfg.initial_capital),
            metadata=dict(metadata or {}),
        )
        self._portfolios[portfolio_id] = ctx
        return ctx

    def get(self, portfolio_id: str) -> PortfolioContext:
        if portfolio_id not in self._portfolios:
            raise KeyError(f"Portfolio not found: {portfolio_id}")
        return self._portfolios[portfolio_id]

    def list_portfolios(self) -> list[str]:
        return sorted(self._portfolios)

    def target_weights(
        self,
        portfolio_id: str,
        symbols: list[str],
        *,
        market_caps: dict[str, float] | None = None,
        volatilities: dict[str, float] | None = None,
        custom_weights: dict[str, float] | None = None,
    ) -> dict[str, float]:
        """Compute target weights from portfolio allocation model — FR-002, FR-003."""
        ctx = self.get(portfolio_id)
        return compute_allocation_weights(
            ctx.config.allocation_model,
            symbols,
            market_caps=market_caps,
            volatilities=volatilities,
            custom_weights=custom_weights,
        )

    def evaluate(
        self,
        portfolio_id: str,
        marks: dict[str, float],
        *,
        sector_map: dict[str, str] | None = None,
    ):
        ctx = self.get(portfolio_id)
        return self._engine.evaluate(ctx.state, marks, sector_map=sector_map)

    def passes_risk_budget(
        self,
        portfolio_id: str,
        marks: dict[str, float],
        *,
        daily_pnl_pct: float | None = None,
    ) -> bool:
        """Check portfolio against configured risk budget — FR-006."""
        ctx = self.get(portfolio_id)
        evaluation = self._engine.evaluate(ctx.state, marks)
        return passes_risk_budget(
            evaluation,
            budget=ctx.config.risk_budget,
            daily_pnl_pct=daily_pnl_pct,
        )

    def suggest_rebalance(
        self,
        portfolio_id: str,
        marks: dict[str, float],
        target_weights: dict[str, float],
    ):
        ctx = self.get(portfolio_id)
        return self._engine.suggest_rebalance(ctx.state, marks, target_weights)

    def snapshot(
        self,
        portfolio_id: str,
        marks: dict[str, float],
        *,
        sector_map: dict[str, str] | None = None,
    ) -> PortfolioSnapshot:
        """Capture immutable portfolio snapshot — FR-014."""
        ctx = self.get(portfolio_id)
        evaluation = self._engine.evaluate(ctx.state, marks, sector_map=sector_map)
        snap = PortfolioSnapshot.capture(
            portfolio_id,
            ctx.state,
            version=ctx.version,
            evaluation=evaluation,
        )
        ctx.version += 1
        self._snapshots.append(snap)
        return snap

    def snapshot_history(self, portfolio_id: str) -> list[PortfolioSnapshot]:
        return [s for s in self._snapshots if s.portfolio_id == portfolio_id]

    def reserve_capital(self, portfolio_id: str, amount: float) -> float:
        """Reserve capital from free cash — FR-009."""
        ctx = self.get(portfolio_id)
        available = ctx.free_cash
        reserved = min(max(amount, 0.0), available)
        ctx.state.cash -= reserved
        return reserved

    def release_capital(self, portfolio_id: str, amount: float) -> None:
        """Return reserved capital to portfolio cash — FR-009."""
        ctx = self.get(portfolio_id)
        ctx.state.cash += max(amount, 0.0)

    def rolling_correlation(
        self,
        returns: pd.DataFrame,
        symbol_a: str,
        symbol_b: str,
        *,
        window: int = 20,
    ) -> pd.Series:
        """Rolling pairwise correlation — FR-008."""
        if symbol_a not in returns.columns or symbol_b not in returns.columns:
            return pd.Series(dtype=float)
        return returns[symbol_a].rolling(window).corr(returns[symbol_b]).dropna()
