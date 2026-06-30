"""PHASE 6/7/8 APS catalog tests."""

from __future__ import annotations

from athena_core.domain.analytics.catalog import ANALYTICS_CATALOG, list_mvp_analytics
from athena_core.domain.portfolio_intelligence.catalog import PORTFOLIO_CATALOG, list_mvp_portfolio
from athena_core.domain.simulation.catalog import SIMULATION_CATALOG, list_mvp_simulation
from athena_core.domain.simulation.event_bus import SimulationEvent, SimulationEventBus, SimulationEventType
from datetime import datetime, timezone


def test_simulation_catalog_mvp_entries() -> None:
    mvp = list_mvp_simulation()
    assert len(mvp) >= 5
    assert len(SIMULATION_CATALOG) >= 10


def test_portfolio_catalog_mvp_entries() -> None:
    mvp = list_mvp_portfolio()
    assert len(mvp) >= 5
    assert len(PORTFOLIO_CATALOG) >= 8


def test_analytics_catalog_mvp_entries() -> None:
    mvp = list_mvp_analytics()
    assert len(mvp) >= 5
    assert len(ANALYTICS_CATALOG) >= 8


def test_simulation_event_bus_replay() -> None:
    bus = SimulationEventBus()
    evt = SimulationEvent(
        SimulationEventType.MARKET,
        datetime(2020, 1, 1, tzinfo=timezone.utc),
        {"symbol": "TEST"},
    )
    bus.publish(evt)
    drained = bus.drain()
    assert len(drained) == 1
    bus.replay(drained)
    assert len(bus.history) == 1
