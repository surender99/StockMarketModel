"""Simulation APS catalog — PHASE 6 SBP."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

SimStatus = Literal["MVP", "Partial", "Deferred"]


@dataclass(frozen=True, slots=True)
class SimulationCatalogEntry:
    aps_id: str
    name: str
    domain: str
    status: SimStatus


SIMULATION_CATALOG: tuple[SimulationCatalogEntry, ...] = (
    SimulationCatalogEntry("APS-SIM-CORE-001", "Simulation Core", "Simulation-Core", "Partial"),
    SimulationCatalogEntry("APS-EXEC-SLIPPAGE-001", "Slippage Models", "Execution-Engine", "MVP"),
    SimulationCatalogEntry("APS-EXEC-PARTIAL-001", "Partial Fill", "Execution-Engine", "Partial"),
    SimulationCatalogEntry("APS-PORT-POS-001", "Simulated Positions", "Portfolio-Simulator", "MVP"),
    SimulationCatalogEntry("APS-PORT-PNL-001", "P and L", "Portfolio-Simulator", "MVP"),
    SimulationCatalogEntry("APS-BROKER-FEES-001", "Brokerage Fees", "Brokerage-Simulator", "MVP"),
    SimulationCatalogEntry("APS-WF-SPLIT-001", "Time Splits", "Walk-Forward", "MVP"),
    SimulationCatalogEntry("APS-WF-ROLLING-001", "Rolling Window", "Walk-Forward", "MVP"),
    SimulationCatalogEntry("APS-REPLAY-CANDLE-001", "Candle Replay", "Replay-Engine", "Partial"),
    SimulationCatalogEntry("APS-REPLAY-EVENT-001", "Event Replay", "Replay-Engine", "Partial"),
    SimulationCatalogEntry("APS-SIM-REPORT-JOURNAL-001", "Trade Journal", "Simulation-Reporting", "MVP"),
    SimulationCatalogEntry("APS-SIM-REPORT-SUMMARY-001", "Simulation Summary", "Simulation-Reporting", "MVP"),
)


def list_mvp_simulation() -> list[SimulationCatalogEntry]:
    return [e for e in SIMULATION_CATALOG if e.status == "MVP"]
