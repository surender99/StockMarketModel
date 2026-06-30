"""Pattern metadata store — APS-PAT-REGISTRY-META-001."""

from __future__ import annotations

from dataclasses import dataclass, field

from athena_core.domain.patterns.catalog import PATTERN_APS_CATALOG, PatternApsCatalogEntry


@dataclass(frozen=True, slots=True)
class PatternMetadata:
    """Extended metadata beyond APS catalog registration."""

    entry: PatternApsCatalogEntry
    description: str = ""
    references: tuple[str, ...] = field(default_factory=tuple)


def build_metadata_store() -> dict[str, PatternMetadata]:
    """Build metadata records keyed by APS id."""
    store: dict[str, PatternMetadata] = {}
    for entry in PATTERN_APS_CATALOG:
        store[entry.aps_id] = PatternMetadata(
            entry=entry,
            description=f"{entry.name} ({entry.domain})",
        )
    return store


def lookup_metadata(aps_id: str) -> PatternMetadata | None:
    """Resolve metadata for an APS id."""
    return build_metadata_store().get(aps_id)
