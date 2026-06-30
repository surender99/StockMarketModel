"""Risk attribution — APS-PA-RISK-001."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from athena_core.domain.portfolio.risk_budget import risk_contributions


@dataclass(frozen=True, slots=True)
class SymbolRiskAttribution:
    """Per-symbol risk decomposition."""

    symbol: str
    weight: float
    marginal_contribution: float
    component_contribution: float
    percent_of_risk: float


@dataclass(frozen=True, slots=True)
class RiskAttributionResult:
    """Portfolio risk attribution snapshot — APS-PA-RISK-001."""

    portfolio_volatility: float
    symbols: tuple[SymbolRiskAttribution, ...]
    sector_attribution: dict[str, float]
    diversification_ratio: float | None


def marginal_risk_contributions(
    returns: pd.DataFrame,
    weights: dict[str, float],
) -> dict[str, float]:
    """Marginal contribution to portfolio variance per symbol."""
    symbols = [s for s in weights if s in returns.columns]
    if len(symbols) < 2:
        return {s: 0.0 for s in symbols}

    w = np.array([weights[s] for s in symbols], dtype=float)
    cov = returns[symbols].cov().to_numpy(dtype=float)
    port_var = float(w @ cov @ w)
    if port_var <= 0:
        return {s: 0.0 for s in symbols}

    marginal = cov @ w
    return {sym: float(m / np.sqrt(port_var)) for sym, m in zip(symbols, marginal)}


def sector_risk_attribution(
    returns: pd.DataFrame,
    weights: dict[str, float],
    sector_map: dict[str, str],
) -> dict[str, float]:
    """Aggregate component risk contributions by sector."""
    contrib = risk_contributions(returns, weights)
    sectors: dict[str, float] = {}
    for symbol, value in contrib.items():
        sector = sector_map.get(symbol, "unknown")
        sectors[sector] = sectors.get(sector, 0.0) + value
    return sectors


def compute_risk_attribution(
    returns: pd.DataFrame,
    weights: dict[str, float],
    *,
    sector_map: dict[str, str] | None = None,
) -> RiskAttributionResult:
    """Full risk attribution decomposition — APS-PA-RISK-001."""
    symbols = [s for s in weights if s in returns.columns]
    if not symbols:
        return RiskAttributionResult(
            portfolio_volatility=0.0,
            symbols=(),
            sector_attribution={},
            diversification_ratio=None,
        )

    w = np.array([weights[s] for s in symbols], dtype=float)
    cov = returns[symbols].cov().to_numpy(dtype=float)
    port_var = float(w @ cov @ w)
    port_vol = float(np.sqrt(port_var)) if port_var > 0 else 0.0

    component = risk_contributions(returns, weights)
    marginal = marginal_risk_contributions(returns, weights)

    symbol_rows: list[SymbolRiskAttribution] = []
    for sym in symbols:
        comp = component.get(sym, 0.0)
        symbol_rows.append(
            SymbolRiskAttribution(
                symbol=sym,
                weight=weights[sym],
                marginal_contribution=marginal.get(sym, 0.0),
                component_contribution=comp,
                percent_of_risk=comp,
            )
        )

    sectors = sector_risk_attribution(returns, weights, sector_map or {})

    div_ratio: float | None = None
    asset_vols = returns[symbols].std()
    weighted_vol_sum = float(sum(weights[s] * asset_vols[s] for s in symbols))
    if weighted_vol_sum > 0 and port_vol > 0:
        div_ratio = weighted_vol_sum / port_vol

    return RiskAttributionResult(
        portfolio_volatility=port_vol,
        symbols=tuple(symbol_rows),
        sector_attribution=sectors,
        diversification_ratio=div_ratio,
    )
