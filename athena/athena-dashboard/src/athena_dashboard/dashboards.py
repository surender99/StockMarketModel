"""Dashboard framework modules — ATH-REL-013."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


DASHBOARD_MODULES: dict[str, str] = {
    "core": "Dashboard framework",
    "chart": "Chart engine",
    "portfolio": "Portfolio dashboard",
    "strategy": "Strategy dashboard",
    "risk": "Risk dashboard",
    "research": "Research dashboard",
    "reports": "Reporting dashboard",
    "alerts": "Alert dashboard",
}


@dataclass
class DashboardPanel:
    """Single dashboard panel."""

    panel_id: str
    title: str
    panel_type: str
    data: dict[str, Any] = field(default_factory=dict)


@dataclass
class DashboardLayout:
    """Dashboard layout with panels."""

    dashboard_id: str
    title: str
    panels: list[DashboardPanel] = field(default_factory=list)

    def add_panel(self, panel: DashboardPanel) -> None:
        self.panels.append(panel)


def list_dashboard_modules() -> dict[str, str]:
    return dict(DASHBOARD_MODULES)


def build_portfolio_dashboard(metrics: dict[str, float]) -> DashboardLayout:
    """Portfolio dashboard — REQ-DASH-PORTFOLIO-001."""
    layout = DashboardLayout("portfolio", "Portfolio Dashboard")
    layout.add_panel(
        DashboardPanel("equity", "Equity Curve", "line", {"metrics": metrics})
    )
    layout.add_panel(
        DashboardPanel("allocation", "Allocation", "pie", {"weights": metrics.get("weights", {})})
    )
    return layout


def build_research_dashboard(experiments: list[dict[str, Any]]) -> DashboardLayout:
    """Research dashboard — REQ-DASH-RESEARCH-001."""
    layout = DashboardLayout("research", "Research Dashboard")
    layout.add_panel(
        DashboardPanel("experiments", "Experiments", "table", {"rows": experiments})
    )
    return layout


def build_risk_dashboard(risk_metrics: dict[str, float]) -> DashboardLayout:
    """Risk dashboard."""
    layout = DashboardLayout("risk", "Risk Dashboard")
    layout.add_panel(
        DashboardPanel("var", "Value at Risk", "metric", {"value": risk_metrics.get("var", 0)})
    )
    return layout


def build_strategy_dashboard(scan_payload: dict[str, Any]) -> DashboardLayout:
    """Strategy dashboard."""
    layout = DashboardLayout("strategy", "Strategy Dashboard")
    layout.add_panel(
        DashboardPanel("candidates", "Scan Candidates", "table", scan_payload)
    )
    return layout
