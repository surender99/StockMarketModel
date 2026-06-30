"""Research workspace — facade over athena-core research domain."""

from __future__ import annotations

from athena_core.domain.research.catalog import QREP_CATALOG, QrepCatalogEntry
from athena_core.domain.research.context import ResearchProject


class ResearchWorkspace:
    """Non-production research context — see PROMOTION-WORKFLOW.md."""

    def __init__(self) -> None:
        self._catalog: tuple[QrepCatalogEntry, ...] = QREP_CATALOG
        self._projects: dict[str, ResearchProject] = {}

    @property
    def catalog(self) -> tuple[QrepCatalogEntry, ...]:
        return self._catalog

    def list_projects(self) -> list[ResearchProject]:
        return list(self._projects.values())
