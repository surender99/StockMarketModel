"""Strategy APS tests — PHASE-5 SIP."""

from __future__ import annotations

from athena_core.domain.strategy.builtin import builtin_strategy_registry
from athena_core.domain.strategy.catalog import (
    STRATEGY_APS_CATALOG,
    STRATEGY_CATALOG,
    list_mvp_strategy_aps,
    lookup_strategy_aps,
    lookup_strategy_aps_by_id,
)
from athena_core.domain.strategy.pipeline import StrategyPipeline, StrategyPipelineStage
from athena_core.domain.strategy.types import SignalDirection, TradeSignal


def test_strategy_aps_catalog_size() -> None:
    """PHASE-5 SIP — catalog covers expanded APS set."""
    assert len(STRATEGY_APS_CATALOG) >= 50
    mvp = list_mvp_strategy_aps()
    assert len(mvp) >= 20


def test_strategy_aps_catalog_lookup() -> None:
    """APS-STRAT-CORE-001 — APS metadata resolves by id."""
    entry = lookup_strategy_aps_by_id("APS-STRAT-CORE-001")
    assert entry is not None
    assert entry.domain == "Strategy-Framework"
    assert entry.status == "MVP"


def test_strategy_catalog_covers_builtin_registry() -> None:
    """APS-STRAT-REGISTRY-001 — catalog matches builtin strategy registry."""
    builtin_ids = set(builtin_strategy_registry())
    catalog_ids = {e.strategy_id for e in STRATEGY_CATALOG}
    assert catalog_ids == builtin_ids


def test_strategy_catalog_lookup() -> None:
    """APS-TEMPLATE-TREND-001 — strategy templates resolve APS metadata."""
    entry = lookup_strategy_aps("ema_crossover")
    assert entry is not None
    assert entry.aps_id == "APS-TEMPLATE-TREND-001"


def test_strategy_intelligence_pipeline_runs() -> None:
    """APS-STRAT-PIPELINE-001 — pipeline executes layered decision stages."""
    pipeline = StrategyPipeline(min_confidence=0.5)
    signals = [
        TradeSignal(SignalDirection.BUY, 0.8, "strong"),
        TradeSignal(SignalDirection.BUY, 0.3, "weak"),
    ]
    results = pipeline.run(signals)
    assert len(results) == len(StrategyPipelineStage)
    qualified = pipeline.decide(signals)
    assert len(qualified) == 1
    assert qualified[0].confidence == 0.8
