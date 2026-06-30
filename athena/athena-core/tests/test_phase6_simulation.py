"""PHASE-6 Simulation code depth tests."""

from __future__ import annotations

from datetime import date, datetime, timezone

import pandas as pd

from athena_core.domain.backtest.orders import Order, OrderSide, OrderType
from athena_core.domain.simulation.event_bus import SimulationEvent, SimulationEventBus, SimulationEventType
from athena_core.domain.simulation.market_simulator import MarketSimulator
from athena_core.domain.simulation.monte_carlo_runner import MonteCarloRunner
from athena_core.domain.simulation.oms import SimOrderManager


def _sample_order() -> Order:
    return Order(
        order_id="sim-1",
        symbol="TEST",
        side=OrderSide.BUY,
        order_type=OrderType.MARKET,
        quantity=100,
        signal_date=date(2024, 6, 1),
    )


def test_req_aps_oms_state_001_order_lifecycle() -> None:
    """REQ-APS-OMS-STATE-001 — submit and fill transitions."""
    oms = SimOrderManager()
    order = oms.create(_sample_order())
    oms.submit(order.order_id)
    oms.fill(order.order_id, 50.0, 100, date(2024, 6, 2))
    filled = oms.get(order.order_id)
    assert filled is not None
    assert filled.status.value == "filled"


def test_req_aps_oms_cancel_001_cancel_submitted() -> None:
    """REQ-APS-OMS-CANCEL-001 — cancel a submitted order."""
    oms = SimOrderManager()
    order = oms.create(_sample_order())
    oms.submit(order.order_id)
    oms.cancel(order.order_id)
    cancelled = oms.get(order.order_id)
    assert cancelled is not None
    assert cancelled.status.value == "cancelled"


def test_req_aps_oms_modify_001_modify_quantity() -> None:
    """REQ-APS-OMS-MODIFY-001 — modify quantity before fill."""
    oms = SimOrderManager()
    order = oms.create(_sample_order())
    oms.modify_quantity(order.order_id, 50)
    updated = oms.get(order.order_id)
    assert updated is not None
    assert updated.quantity == 50


def test_req_aps_market_core_001_market_quote() -> None:
    """REQ-APS-MARKET-CORE-001 — market state with bid/ask spread."""
    market = MarketSimulator(spread_bps=10.0)
    ts = datetime(2024, 6, 1, 9, 30, tzinfo=timezone.utc)
    quote = market.update("TEST", 100.0, ts)
    assert quote.last == 100.0
    assert quote.bid < quote.last < quote.ask
    assert market.quote("TEST") == quote


def test_req_aps_mc_returns_001_return_sampling() -> None:
    """REQ-APS-MC-RETURNS-001 — Monte Carlo return sampling."""
    dates = pd.date_range("2020-01-01", periods=60, freq="B")
    equity = pd.DataFrame({"equity": 100_000 * (1 + pd.Series(range(60)) * 0.001)}, index=dates)
    result = MonteCarloRunner().run_return_sampling(equity, n_simulations=200, seed=7)
    assert result.simulations == 200
    assert result.percentile_5 <= result.median_return <= result.percentile_95


def test_req_aps_replay_event_001_event_bus_integration() -> None:
    """REQ-APS-REPLAY-EVENT-001 — OMS and market publish through event bus."""
    bus = SimulationEventBus()
    received: list[SimulationEvent] = []
    bus.subscribe(SimulationEventType.ORDER, received.append)
    bus.subscribe(SimulationEventType.MARKET, received.append)

    oms = SimOrderManager(bus)
    market = MarketSimulator(bus=bus)
    ts = datetime(2024, 6, 1, 10, 0, tzinfo=timezone.utc)

    order = oms.create(_sample_order())
    oms.submit(order.order_id)
    market.update("TEST", 101.5, ts)

    assert len(received) == 3
    assert received[0].event_type == SimulationEventType.ORDER
    assert received[1].event_type == SimulationEventType.ORDER
    assert received[2].event_type == SimulationEventType.MARKET
    assert received[2].payload["symbol"] == "TEST"

    drained = bus.drain()
    bus.replay(drained)
    assert len(bus.history) == len(drained)
