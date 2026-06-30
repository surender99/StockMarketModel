"""Pattern APS tests — PHASE-4 Patterns."""

from __future__ import annotations

from athena_core.domain.patterns.base import builtin_pattern_registry
from athena_core.domain.patterns.catalog import PATTERN_CATALOG, lookup_pattern_aps


def test_pattern_catalog_covers_builtin_registry() -> None:
    """APS-PAT-REGISTRY-001 — catalog matches builtin pattern registry."""
    builtin_ids = set(builtin_pattern_registry())
    catalog_ids = {e.pattern_id for e in PATTERN_CATALOG}
    assert catalog_ids == builtin_ids


def test_pattern_catalog_assigns_category() -> None:
    """APS-PAT-CANDLE-001 / APS-PAT-CHART-001 — patterns have category metadata."""
    hammer = lookup_pattern_aps("hammer")
    assert hammer is not None
    assert hammer.category == "Candlestick-Patterns"
    double_top = lookup_pattern_aps("double_top")
    assert double_top is not None
    assert double_top.category == "Chart-Patterns"
