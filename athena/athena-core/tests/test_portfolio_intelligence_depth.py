"""PHASE 7 portfolio intelligence code depth tests."""

from __future__ import annotations

from datetime import date

import pandas as pd

from athena_core.domain.portfolio.models import PortfolioState
from athena_core.domain.portfolio.positions import OpenPosition
from athena_core.domain.portfolio_intelligence.decision_pipeline import (
    PortfolioDecisionContext,
    PortfolioDecisionPipeline,
    TradeRecommendation,
    list_decision_stages,
)
from athena_core.domain.portfolio_intelligence.optimizer_waves import (
    OptimizerWave,
    OptimizerWaveRegistry,
    list_optimizer_waves,
    list_wave_aps,
)
from athena_core.domain.portfolio_intelligence.risk_attribution import (
    compute_risk_attribution,
    marginal_risk_contributions,
    sector_risk_attribution,
)


def test_decision_pipeline_stages_defined() -> None:
    stages = list_decision_stages()
    assert len(stages) == 7
    assert stages[0] == "trade_recommendations"
    assert stages[-1] == "execution_proposal"


def test_decision_pipeline_end_to_end() -> None:
    state = PortfolioState(cash=10_000.0)
    state.positions["A"] = OpenPosition(
        symbol="A",
        side="long",
        entry_date=date(2024, 1, 2),
        entry_price=100.0,
        quantity=50,
        entry_fees=0.0,
    )
    returns = pd.DataFrame(
        {
            "A": [0.01, -0.01, 0.02, 0.005, -0.005],
            "B": [0.005, -0.005, 0.01, 0.002, -0.002],
        }
    )
    ctx = PortfolioDecisionContext(
        portfolio_id="pf-1",
        state=state,
        marks={"A": 100.0, "B": 50.0},
        recommendations=[
            TradeRecommendation(symbol="A", side="buy", conviction=0.5),
            TradeRecommendation(symbol="B", side="buy", conviction=0.5),
        ],
        returns=returns,
        sector_map={"A": "tech", "B": "finance"},
    )
    result = PortfolioDecisionPipeline().run(ctx)
    assert result.success
    assert len(result.stages) == 7
    assert result.artifacts["portfolio_construction"]["weights"]
    assert isinstance(result.proposals, list)


def test_optimizer_wave_stubs() -> None:
    waves = list_optimizer_waves()
    assert len(waves) == 5
    assert OptimizerWave.FOUNDATION in waves
    assert len(list_wave_aps(OptimizerWave.OPTIMIZATION)) >= 3

    registry = OptimizerWaveRegistry()
    results = registry.execute_all_stubs()
    assert len(results) == 5
    assert all(r.status == "stub_ok" for r in results)
    assert results[0].wave == OptimizerWave.FOUNDATION


def test_risk_attribution_enhancements() -> None:
    returns = pd.DataFrame(
        {
            "A": [0.01, -0.02, 0.015, 0.005, -0.01],
            "B": [0.005, -0.01, 0.01, 0.002, -0.005],
        }
    )
    weights = {"A": 0.6, "B": 0.4}
    marginal = marginal_risk_contributions(returns, weights)
    assert set(marginal) == {"A", "B"}

    sectors = sector_risk_attribution(returns, weights, {"A": "tech", "B": "finance"})
    assert abs(sum(sectors.values()) - 1.0) < 0.01

    attribution = compute_risk_attribution(
        returns,
        weights,
        sector_map={"A": "tech", "B": "finance"},
    )
    assert attribution.portfolio_volatility > 0
    assert len(attribution.symbols) == 2
    assert abs(sum(s.percent_of_risk for s in attribution.symbols) - 1.0) < 0.01
    assert attribution.diversification_ratio is not None
