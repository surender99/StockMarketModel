"""Dashboard framework tests — ATH-REL-013."""

from __future__ import annotations

import pandas as pd

from athena_dashboard.charts import build_bar_chart, build_candlestick_data, build_heatmap
from athena_dashboard.dashboards import (
    build_portfolio_dashboard,
    build_research_dashboard,
    build_risk_dashboard,
    build_strategy_dashboard,
    list_dashboard_modules,
)


def test_req_dash_chart_001_candlestick() -> None:
    """REQ-DASH-CHART-001 — chart engine."""
    ohlcv = pd.DataFrame(
        {"open": [1, 2], "high": [3, 4], "low": [0.5, 1.5], "close": [2, 3], "volume": [100, 200]}
    )
    rows = build_candlestick_data(ohlcv)
    assert len(rows) == 2
    assert rows[0]["close"] == 2.0


def test_req_dash_core_001_modules() -> None:
    """REQ-DASH-CORE-001 — dashboard framework."""
    modules = list_dashboard_modules()
    assert "portfolio" in modules
    assert len(modules) >= 8


def test_req_dash_portfolio_001_dashboard() -> None:
    """REQ-DASH-PORTFOLIO-001 — portfolio dashboard."""
    layout = build_portfolio_dashboard({"sharpe": 1.5, "weights": {"A": 0.6}})
    assert layout.dashboard_id == "portfolio"
    assert len(layout.panels) >= 2


def test_req_dash_research_001_dashboard() -> None:
    """REQ-DASH-RESEARCH-001 — research dashboard."""
    layout = build_research_dashboard([{"experiment_id": "e1", "sharpe": 1.2}])
    assert layout.panels[0].panel_type == "table"


def test_dashboard_charts_helpers() -> None:
    """Chart helpers produce valid payloads."""
    heatmap = build_heatmap(pd.DataFrame({"a": [1, 2], "b": [3, 4]}))
    assert heatmap["labels"]
    bar = build_bar_chart(["A", "B"], [1.0, 2.0])
    assert bar["values"] == [1.0, 2.0]
    risk = build_risk_dashboard({"var": 0.05})
    assert risk.panels[0].data["value"] == 0.05
    strategy = build_strategy_dashboard({"candidates": []})
    assert strategy.dashboard_id == "strategy"
