"""Portfolio engine adapter implementing IPortfolioEngine."""
from __future__ import annotations

from athena_core.domain.portfolio.positions import OpenPosition


class PortfolioEngineFacade:
    """Delegates to athena-core portfolio — extraction path: ADR-0006."""

    def __init__(self) -> None:
        self._positions: list[OpenPosition] = []

    @property
    def positions(self) -> tuple[OpenPosition, ...]:
        return tuple(self._positions)
