"""Paper trading framework tests — ATH-REL-014."""

from __future__ import annotations

from athena_core.application.paper_trading_engine import PaperTradingEngine
from athena_core.domain.paper.orders import OrderSide, OrderStatus
from athena_core.domain.paper.risk import PaperRiskControls


def test_req_paper_broker_001_account() -> None:
    """REQ-PAPER-BROKER-001 — paper broker."""
    engine = PaperTradingEngine(initial_cash=10_000.0)
    snap = engine.broker.snapshot()
    assert snap["cash"] == 10_000.0


def test_req_paper_orders_001_submit() -> None:
    """REQ-PAPER-ORDERS-001 — paper orders."""
    engine = PaperTradingEngine(initial_cash=10_000.0)
    order = engine.place_order("AAPL", OrderSide.BUY, 10, 100.0)
    assert order.status == OrderStatus.FILLED
    assert engine.broker.account.portfolio.positions["AAPL"].quantity == 10


def test_req_paper_positions_001_tracking() -> None:
    """REQ-PAPER-POSITIONS-001 — positions."""
    engine = PaperTradingEngine(initial_cash=20_000.0)
    engine.place_order("MSFT", OrderSide.BUY, 5, 200.0)
    pos = engine.broker.account.portfolio.get_position("MSFT")
    assert pos is not None
    assert pos.quantity == 5


def test_req_paper_execution_001_simulator() -> None:
    """REQ-PAPER-EXECUTION-001 — execution simulator."""
    engine = PaperTradingEngine()
    order = engine.place_order("X", OrderSide.BUY, 1, 50.0)
    assert order.fill_price is not None
    assert order.fill_price >= 50.0


def test_req_paper_risk_001_controls() -> None:
    """REQ-PAPER-RISK-001 — risk controls."""
    engine = PaperTradingEngine(
        initial_cash=1_000.0,
        risk=PaperRiskControls(max_order_value=500.0),
    )
    order = engine.place_order("BIG", OrderSide.BUY, 100, 100.0)
    assert order.status == OrderStatus.REJECTED
