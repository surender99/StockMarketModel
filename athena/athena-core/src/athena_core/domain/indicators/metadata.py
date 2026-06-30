"""Indicator metadata store — APS-IND-METADATA-001."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from athena_core.domain.indicators.catalog import IndicatorCatalogEntry, INDICATOR_CATALOG

IndicatorComplexity = Literal["O(n)", "O(n·p)", "O(n·log n)"]


@dataclass(frozen=True, slots=True)
class IndicatorMetadata:
    """Extended metadata beyond catalog registration."""

    entry: IndicatorCatalogEntry
    description: str = ""
    formula: str = ""
    complexity_time: IndicatorComplexity = "O(n)"
    complexity_space: IndicatorComplexity = "O(n)"
    references: tuple[str, ...] = field(default_factory=tuple)
    author: str = "Athena Contributors"


def build_metadata_store() -> dict[str, IndicatorMetadata]:
    """Build metadata records for all catalog entries."""
    store: dict[str, IndicatorMetadata] = {}
    for entry in INDICATOR_CATALOG:
        store[entry.plugin_id] = IndicatorMetadata(
            entry=entry,
            description=f"{entry.name} ({entry.aps_id})",
            formula=entry.name,
        )
    return store


def lookup_metadata(plugin_id: str) -> IndicatorMetadata | None:
    """Resolve metadata for a plugin id."""
    return build_metadata_store().get(plugin_id)
