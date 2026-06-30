"""PHASE-4/5 APS catalog tests."""

from __future__ import annotations

from athena_core.domain.patterns.base import builtin_pattern_registry
from athena_core.domain.patterns.catalog import (
    PATTERN_APS_CATALOG,
    PATTERN_CATALOG,
    list_mvp_patterns,
    lookup_by_aps_id,
    lookup_pattern_aps,
)
from athena_core.domain.strategy.catalog import STRATEGY_APS_CATALOG, list_mvp_strategy_aps


def test_phase4_aps_catalog_count() -> None:
    """PHASE-4 MSP — expanded pattern APS catalog published."""
    assert len(PATTERN_APS_CATALOG) == 164


def test_phase4_mvp_builtin_patterns_mapped() -> None:
    """APS-PAT-REGISTRY-CORE-001 — builtin patterns map to candlestick/chart APS."""
    builtin_ids = set(builtin_pattern_registry())
    catalog_ids = {e.pattern_id for e in PATTERN_CATALOG}
    assert catalog_ids == builtin_ids
    hammer = lookup_pattern_aps("hammer")
    assert hammer is not None
    assert hammer.aps_id == "APS-CS-HAMMER-001"
    assert hammer.category == "Candlestick-Engine"


def test_phase4_unique_aps_ids() -> None:
    """APS-PAT-REGISTRY-DISCOVERY-001 — each APS id is unique."""
    aps_ids = [e.aps_id for e in PATTERN_APS_CATALOG]
    assert len(aps_ids) == len(set(aps_ids))


def test_phase4_mvp_pattern_specs() -> None:
    """PHASE-4 MSP — MVP candlestick and chart specs registered."""
    mvp = list_mvp_patterns()
    assert len(mvp) == 16
    assert lookup_by_aps_id("APS-CS-HAMMER-001") is not None
    assert lookup_by_aps_id("APS-CP-DOUBLETOP-001") is not None


def test_phase5_aps_catalog_count() -> None:
    """PHASE-5 SIP — expanded strategy APS catalog published."""
    assert len(STRATEGY_APS_CATALOG) == 169


def test_phase5_mvp_strategy_aps_present() -> None:
    """APS-STRAT-CORE-001 — MVP strategy APS specs registered."""
    mvp = list_mvp_strategy_aps()
    assert len(mvp) >= 10
    assert any(e.aps_id == "APS-STRAT-CORE-001" for e in mvp)
