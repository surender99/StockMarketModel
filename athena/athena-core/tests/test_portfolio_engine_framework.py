"""Portfolio management engine framework tests — ATH-REL-008."""

from __future__ import annotations

from datetime import date

import pandas as pd

from athena_core.application.bootstrap import bootstrap_athena_core
from athena_core.application.config import AthenaConfig
from athena_core.application.portfolio_analytics import compute_portfolio_analytics
from athena_core.application.portfolio_manager import PortfolioManager
from athena_core.application.portfolio_optimizer import (
    inverse_volatility_weights,
    minimum_variance_weights,
)
from athena_core.domain.plugins import PluginRegistry, PluginType
from athena_core.domain.portfolio import (
    PortfolioConfig,
    PortfolioState,
    compute_allocation_weights,
    list_allocation_models,
    passes_risk_budget,
    register_builtin_portfolio_plugins,
    risk_contributions,
)
from athena_core.domain.portfolio.positions import OpenPosition
from athena_core.domain.portfolio.risk_budget import RiskBudget


def test_req_pf_allocation_001_equal_weight() -> None:
    """REQ-PF-ALLOCATION-001 — equal weight allocation model."""
    weights = compute_allocation_weights("equal_weight", ["A", "B", "C"])
    assert len(weights) == 3
    assert abs(sum(weights.values()) - 1.0) < 1e-9
    assert all(abs(w - 1 / 3) < 1e-9 for w in weights.values())


def test_req_pf_allocation_001_market_cap_weight() -> None:
    """REQ-PF-ALLOCATION-001 — market cap weighted allocation."""
    weights = compute_allocation_weights(
        "market_cap",
        ["A", "B"],
        market_caps={"A": 100.0, "B": 300.0},
    )
    assert abs(weights["A"] - 0.25) < 1e-9
    assert abs(weights["B"] - 0.75) < 1e-9


def test_req_pf_allocation_001_risk_weight() -> None:
    """REQ-PF-ALLOCATION-001 — inverse volatility risk weights."""
    weights = compute_allocation_weights(
        "risk_weight",
        ["A", "B"],
        volatilities={"A": 0.2, "B": 0.1},
    )
    assert weights["B"] > weights["A"]


def test_req_pf_allocation_001_custom_weights() -> None:
    weights = compute_allocation_weights(
        "custom",
        ["A", "B"],
        custom_weights={"A": 0.7, "B": 0.3},
    )
    assert abs(weights["A"] - 0.7) < 1e-9
    assert abs(weights["B"] - 0.3) < 1e-9


def test_allocation_models_registered() -> None:
    """ATH-REL-008 §5.1 — allocation models registered in PluginRegistry."""
    registry = PluginRegistry()
    register_builtin_portfolio_plugins(registry)
    models = registry.list(plugin_type=PluginType.REPORT, active_only=True)
    ids = {p.id for p in models}
    assert "allocation:equal_weight" in ids
    assert "allocation:market_cap" in ids
    assert len(list_allocation_models()) == 5


def test_bootstrap_registers_portfolio_plugins() -> None:
    ctx = bootstrap_athena_core(AthenaConfig())
    models = ctx.plugin_registry.list(plugin_type=PluginType.REPORT, active_only=True)
    ids = {p.id for p in models}
    assert any(i.startswith("allocation:") for i in ids)


def test_req_pf_risk_001_risk_budget() -> None:
    """REQ-PF-RISK-001 — portfolio risk budget enforcement."""
    from athena_core.application.portfolio_engine import PortfolioEngine

    portfolio = PortfolioState(cash=0.0)
    portfolio.positions["X"] = OpenPosition(
        symbol="X",
        side="long",
        entry_date=date(2024, 1, 2),
        entry_price=100.0,
        quantity=100,
        entry_fees=0.0,
    )
    evaluation = PortfolioEngine().evaluate(portfolio, {"X": 100.0})
    assert passes_risk_budget(evaluation, budget=RiskBudget(max_gross_exposure=2.0))
    assert not passes_risk_budget(
        evaluation,
        budget=RiskBudget(max_gross_exposure=0.5),
    )


def test_risk_contributions_sum_to_one() -> None:
    returns = pd.DataFrame(
        {
            "A": [0.01, -0.02, 0.015, 0.005, -0.01],
            "B": [0.005, -0.01, 0.01, 0.002, -0.005],
        }
    )
    weights = {"A": 0.6, "B": 0.4}
    contrib = risk_contributions(returns, weights)
    assert abs(sum(contrib.values()) - 1.0) < 0.01


def test_req_pf_snapshot_001_immutable_snapshot() -> None:
    """REQ-PF-SNAPSHOT-001 — immutable portfolio snapshots."""
    manager = PortfolioManager()
    ctx = manager.create_portfolio("Fund A", config=PortfolioConfig(initial_capital=100_000.0))
    snap = manager.snapshot(ctx.portfolio_id, {})
    assert snap.portfolio_id == ctx.portfolio_id
    assert snap.state.cash == 100_000.0
    ctx.state.cash = 50_000.0
    assert snap.state.cash == 100_000.0
    assert len(manager.snapshot_history(ctx.portfolio_id)) == 1


def test_portfolio_manager_multi_portfolio_fr_001() -> None:
    """FR-001 — support multiple portfolios."""
    manager = PortfolioManager()
    a = manager.create_portfolio("Alpha")
    b = manager.create_portfolio("Beta")
    assert a.portfolio_id != b.portfolio_id
    assert len(manager.list_portfolios()) == 2


def test_portfolio_manager_target_weights_fr_003() -> None:
    manager = PortfolioManager()
    ctx = manager.create_portfolio(
        "Equal",
        config=PortfolioConfig(allocation_model="equal_weight"),
    )
    weights = manager.target_weights(ctx.portfolio_id, ["A", "B", "C"])
    assert abs(weights["A"] - 1 / 3) < 1e-9


def test_portfolio_manager_rebalance_fr_004() -> None:
    manager = PortfolioManager()
    ctx = manager.create_portfolio("Rebal", config=PortfolioConfig(initial_capital=0.0))
    ctx.state.positions["A"] = OpenPosition(
        symbol="A",
        side="long",
        entry_date=date(2024, 1, 2),
        entry_price=100.0,
        quantity=80,
        entry_fees=0.0,
    )
    ctx.state.positions["B"] = OpenPosition(
        symbol="B",
        side="long",
        entry_date=date(2024, 1, 2),
        entry_price=100.0,
        quantity=20,
        entry_fees=0.0,
    )
    orders = manager.suggest_rebalance(ctx.portfolio_id, {"A": 100.0, "B": 100.0}, {"A": 0.5, "B": 0.5})
    assert orders
    assert any(o.symbol == "A" and o.side == "sell" for o in orders)


def test_portfolio_optimizer_fr_005() -> None:
    """FR-005 — portfolio optimization MVP."""
    returns = pd.DataFrame(
        {
            "A": [0.01, -0.01, 0.02, 0.005, -0.005],
            "B": [0.005, -0.005, 0.01, 0.002, -0.002],
        }
    )
    inv_vol = inverse_volatility_weights(returns)
    min_var = minimum_variance_weights(returns)
    assert abs(sum(inv_vol.values()) - 1.0) < 1e-9
    assert abs(sum(min_var.values()) - 1.0) < 1e-9


def test_portfolio_analytics_fr_007() -> None:
    """FR-007 — portfolio analytics calculations."""
    returns = pd.DataFrame(
        {
            "A": [0.01, 0.02, -0.01, 0.015, 0.005],
            "B": [0.005, 0.01, -0.005, 0.01, 0.002],
        }
    )
    weights = {"A": 0.5, "B": 0.5}
    analytics = compute_portfolio_analytics(returns, weights)
    assert analytics.total_return != 0.0
    assert analytics.volatility >= 0.0
    assert analytics.max_drawdown <= 0.0


def test_portfolio_manager_rolling_correlation_fr_008() -> None:
    returns = pd.DataFrame(
        {
            "A": [0.01, 0.02, 0.01, 0.02, 0.01, 0.02] * 5,
            "B": [0.01, 0.02, 0.01, 0.02, 0.01, 0.02] * 5,
        }
    )
    manager = PortfolioManager()
    rolling = manager.rolling_correlation(returns, "A", "B", window=5)
    assert not rolling.empty
    assert rolling.iloc[-1] > 0.9


def test_cash_management_fr_009() -> None:
    manager = PortfolioManager()
    ctx = manager.create_portfolio("Cash", config=PortfolioConfig(initial_capital=100_000.0))
    reserved = manager.reserve_capital(ctx.portfolio_id, 10_000.0)
    assert reserved == 10_000.0
    assert ctx.state.cash == 90_000.0
    manager.release_capital(ctx.portfolio_id, 5_000.0)
    assert ctx.state.cash == 95_000.0
