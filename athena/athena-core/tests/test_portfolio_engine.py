"""Portfolio engine tests — REQ-PF-001, REQ-PF-002, REQ-PF-003."""

from __future__ import annotations

from datetime import date

from athena_core.application.portfolio_engine import PortfolioEngine
from athena_core.domain.portfolio import PortfolioState
from athena_core.domain.portfolio.positions import OpenPosition


def test_portfolio_equity_and_exposure_req_pf_001() -> None:
    portfolio = PortfolioState(cash=50_000.0)
    portfolio.positions["AAA"] = OpenPosition(
        symbol="AAA",
        side="long",
        entry_date=date(2024, 1, 2),
        entry_price=100.0,
        quantity=100,
        entry_fees=10.0,
    )
    portfolio.positions["BBB"] = OpenPosition(
        symbol="BBB",
        side="long",
        entry_date=date(2024, 1, 2),
        entry_price=200.0,
        quantity=50,
        entry_fees=10.0,
    )
    marks = {"AAA": 110.0, "BBB": 190.0}
    evaluation = PortfolioEngine().evaluate(
        portfolio,
        marks,
        sector_map={"AAA": "Tech", "BBB": "Finance"},
    )
    assert evaluation.equity == 50_000.0 + 11_000.0 + 9_500.0
    assert evaluation.metrics.position_count == 2
    assert evaluation.metrics.cash_weight < 1.0
    assert "Tech" in evaluation.metrics.sector_weights
    assert evaluation.metrics.largest_position_weight > 0


def test_portfolio_heat_and_concentration_req_pf_003() -> None:
    portfolio = PortfolioState(cash=0.0)
    portfolio.positions["X"] = OpenPosition(
        symbol="X",
        side="long",
        entry_date=date(2024, 1, 2),
        entry_price=100.0,
        quantity=100,
        entry_fees=0.0,
        stop_price=90.0,
    )
    evaluation = PortfolioEngine().evaluate(
        portfolio,
        {"X": 100.0},
        risk_per_position={"X": 0.1},
    )
    assert evaluation.metrics.gross_exposure == 1.0
    assert evaluation.metrics.portfolio_heat > 0


def test_empty_portfolio_req_pf_002() -> None:
    portfolio = PortfolioState(cash=100_000.0)
    evaluation = PortfolioEngine().evaluate(portfolio, {})
    assert evaluation.equity == 100_000.0
    assert evaluation.metrics.cash_weight == 1.0
    assert evaluation.metrics.position_count == 0


def test_rebalance_suggestions_req_pf_002() -> None:
    portfolio = PortfolioState(cash=0.0)
    portfolio.positions["A"] = OpenPosition(
        symbol="A",
        side="long",
        entry_date=date(2024, 1, 2),
        entry_price=100.0,
        quantity=80,
        entry_fees=0.0,
    )
    portfolio.positions["B"] = OpenPosition(
        symbol="B",
        side="long",
        entry_date=date(2024, 1, 2),
        entry_price=100.0,
        quantity=20,
        entry_fees=0.0,
    )
    marks = {"A": 100.0, "B": 100.0}
    engine = PortfolioEngine()
    orders = engine.suggest_rebalance(
        portfolio,
        marks,
        {"A": 0.5, "B": 0.5},
    )
    assert orders
    assert any(o.symbol == "A" and o.side == "sell" for o in orders)


def test_correlation_limit_blocks_entry() -> None:
    import pandas as pd

    portfolio = PortfolioState(cash=50_000.0)
    portfolio.positions["A"] = OpenPosition(
        symbol="A",
        side="long",
        entry_date=date(2024, 1, 2),
        entry_price=100.0,
        quantity=50,
        entry_fees=0.0,
    )
    evaluation = PortfolioEngine().evaluate(portfolio, {"A": 100.0})
    returns = pd.DataFrame({"A": [0.01, 0.02, 0.01, 0.02, 0.01], "B": [0.01, 0.02, 0.01, 0.02, 0.01]})
    from athena_core.application.portfolio_risk import PortfolioLimits

    allowed = PortfolioEngine().passes_entry_limits(
        evaluation,
        "B",
        0.1,
        returns,
        limits=PortfolioLimits(max_correlation=0.5),
    )
    assert not allowed
