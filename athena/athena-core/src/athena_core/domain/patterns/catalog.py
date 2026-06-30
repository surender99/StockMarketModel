"""Pattern APS catalog — REQ-APS-PAT-REGISTRY-001, ATH-REL-005."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from athena_core.domain.patterns.base import builtin_pattern_registry

PatternStatus = Literal["MVP", "Deferred"]


@dataclass(frozen=True, slots=True)
class PatternCatalogEntry:
    """Metadata for a built-in pattern detector wired to an APS spec."""

    pattern_id: str
    aps_id: str
    category: str
    status: PatternStatus


def build_pattern_catalog() -> tuple[PatternCatalogEntry, ...]:
    """Build catalog from registered builtin patterns."""
    candlestick_ids = {
        "hammer",
        "inverted_hammer",
        "doji",
        "bullish_engulfing",
        "bearish_engulfing",
        "morning_star",
        "evening_star",
        "harami",
        "piercing",
        "dark_cloud",
        "shooting_star",
    }
    entries: list[PatternCatalogEntry] = []
    for pattern_id in builtin_pattern_registry():
        category = "Candlestick-Patterns" if pattern_id in candlestick_ids else "Chart-Patterns"
        entries.append(
            PatternCatalogEntry(
                pattern_id=pattern_id,
                aps_id="APS-PAT-CANDLE-001" if category == "Candlestick-Patterns" else "APS-PAT-CHART-001",
                category=category,
                status="MVP",
            )
        )
    return tuple(entries)


PATTERN_CATALOG: tuple[PatternCatalogEntry, ...] = build_pattern_catalog()


def lookup_pattern_aps(pattern_id: str) -> PatternCatalogEntry | None:
    """Resolve APS metadata for a pattern id."""
    for entry in PATTERN_CATALOG:
        if entry.pattern_id == pattern_id:
            return entry
    return None
