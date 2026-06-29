"""Portfolio risk budgets — ATH-REL-008 §5.4, REQ-PF-RISK-001."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from athena_core.domain.portfolio.models import PortfolioEvaluation


@dataclass(frozen=True)
class RiskBudget:
    """Portfolio-level risk limits — FR-006."""

    max_portfolio_heat: float = 0.25
    max_daily_loss_pct: float = 0.05
    max_gross_exposure: float = 1.5
    max_net_exposure: float = 1.0


def passes_risk_budget(
    evaluation: PortfolioEvaluation,
    *,
    budget: RiskBudget | None = None,
    daily_pnl_pct: float | None = None,
) -> bool:
    """True when portfolio metrics are within risk budget — REQ-PF-RISK-001."""
    budget = budget or RiskBudget()
    metrics = evaluation.metrics
    if metrics.portfolio_heat > budget.max_portfolio_heat:
        return False
    if metrics.gross_exposure > budget.max_gross_exposure:
        return False
    if abs(metrics.net_exposure) > budget.max_net_exposure:
        return False
    if daily_pnl_pct is not None and daily_pnl_pct < -budget.max_daily_loss_pct:
        return False
    return True


def risk_contributions(
    returns: pd.DataFrame,
    weights: dict[str, float],
) -> dict[str, float]:
    """Marginal risk contribution per symbol — ATH-REL-008 §5.4."""
    symbols = [s for s in weights if s in returns.columns]
    if len(symbols) < 2:
        return {s: weights.get(s, 0.0) for s in symbols}

    w = np.array([weights[s] for s in symbols], dtype=float)
    cov = returns[symbols].cov().to_numpy(dtype=float)
    port_var = float(w @ cov @ w)
    if port_var <= 0:
        n = len(symbols)
        return {s: 1.0 / n for s in symbols}

    marginal = cov @ w
    contrib = w * marginal / port_var
    return {sym: float(c) for sym, c in zip(symbols, contrib)}
