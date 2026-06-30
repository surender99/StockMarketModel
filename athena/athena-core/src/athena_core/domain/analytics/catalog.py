"""Quantitative Analytics APS catalog — PHASE 8 QARIP."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

AnalyticsStatus = Literal["MVP", "Partial", "Deferred"]


@dataclass(frozen=True, slots=True)
class AnalyticsCatalogEntry:
    aps_id: str
    name: str
    domain: str
    status: AnalyticsStatus


ANALYTICS_CATALOG: tuple[AnalyticsCatalogEntry, ...] = (
    AnalyticsCatalogEntry("APS-STAT-CORE-001", "Statistics Core Framework", "Statistics-Engine", "MVP"),
    AnalyticsCatalogEntry("APS-STAT-DESCRIPTIVE-001", "Descriptive Statistics", "Statistics-Engine", "MVP"),
    AnalyticsCatalogEntry("APS-STAT-MOMENTS-001", "Statistical Moments", "Statistics-Engine", "MVP"),
    AnalyticsCatalogEntry("APS-RISK-DRAWDOWN-001", "Drawdown Analysis", "Risk-Intelligence", "MVP"),
    AnalyticsCatalogEntry("APS-PERF-CAGR-001", "CAGR", "Performance-Analytics", "MVP"),
    AnalyticsCatalogEntry("APS-PERF-SHARPE-001", "Sharpe Ratio", "Performance-Analytics", "MVP"),
    AnalyticsCatalogEntry("APS-PERF-SORTINO-001", "Sortino Ratio", "Performance-Analytics", "MVP"),
    AnalyticsCatalogEntry("APS-PERF-PROFITFACTOR-001", "Profit Factor", "Performance-Analytics", "MVP"),
)


def list_mvp_analytics() -> list[AnalyticsCatalogEntry]:
    return [e for e in ANALYTICS_CATALOG if e.status == "MVP"]
