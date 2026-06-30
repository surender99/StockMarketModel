"""Strategy APS tests — PHASE-5 Strategies."""

from __future__ import annotations

from athena_core.domain.strategy.builtin import builtin_strategy_registry
from athena_core.domain.strategy.catalog import STRATEGY_CATALOG, lookup_strategy_aps


def test_strategy_catalog_covers_builtin_registry() -> None:
    """APS-STRAT-REGISTRY-001 — catalog matches builtin strategy registry."""
    builtin_ids = set(builtin_strategy_registry())
    catalog_ids = {e.strategy_id for e in STRATEGY_CATALOG}
    assert catalog_ids == builtin_ids


def test_strategy_catalog_lookup() -> None:
    """APS-STRAT-FRAME-001 — strategy templates resolve APS metadata."""
    entry = lookup_strategy_aps("ema_crossover")
    assert entry is not None
    assert entry.aps_id == "APS-STRAT-REGISTRY-001"
