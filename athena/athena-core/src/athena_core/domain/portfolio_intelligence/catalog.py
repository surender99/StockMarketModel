"""Portfolio Intelligence APS catalog — PHASE 7 PIP."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

PortfolioStatus = Literal["MVP", "Partial", "Deferred"]


@dataclass(frozen=True, slots=True)
class PortfolioCatalogEntry:
    aps_id: str
    name: str
    domain: str
    status: PortfolioStatus


PORTFOLIO_CATALOG: tuple[PortfolioCatalogEntry, ...] = (
    PortfolioCatalogEntry("APS-PORT-MANAGER-001", "Portfolio Manager", "Portfolio-Core", "MVP"),
    PortfolioCatalogEntry("APS-PORT-CONTEXT-001", "Portfolio Context", "Portfolio-Core", "MVP"),
    PortfolioCatalogEntry("APS-POS-FIXED-001", "Fixed Quantity", "Portfolio-Position-Sizing", "MVP"),
    PortfolioCatalogEntry("APS-POS-RISK-001", "Risk Percent Sizing", "Portfolio-Position-Sizing", "MVP"),
    PortfolioCatalogEntry("APS-RB-CORE-001", "Risk Budget Engine", "Risk-Budget", "MVP"),
    PortfolioCatalogEntry("APS-EXPOSURE-NET-001", "Net Exposure", "Exposure-Engine", "MVP"),
    PortfolioCatalogEntry("APS-EXPOSURE-GROSS-001", "Gross Exposure", "Exposure-Engine", "MVP"),
    PortfolioCatalogEntry("APS-PA-PERFORMANCE-001", "Portfolio Returns", "Portfolio-Analytics", "MVP"),
)


def list_mvp_portfolio() -> list[PortfolioCatalogEntry]:
    return [e for e in PORTFOLIO_CATALOG if e.status == "MVP"]
