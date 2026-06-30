"""Strategy APS catalog — REQ-APS-STRAT-REGISTRY-001, ATH-REL-006."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from athena_core.domain.strategy.builtin import builtin_strategy_registry

StrategyStatus = Literal["MVP", "Deferred"]


@dataclass(frozen=True, slots=True)
class StrategyCatalogEntry:
    """Metadata for a built-in strategy template wired to an APS spec."""

    strategy_id: str
    aps_id: str
    name: str
    status: StrategyStatus


def build_strategy_catalog() -> tuple[StrategyCatalogEntry, ...]:
    """Build catalog from registered builtin strategies."""
    return tuple(
        StrategyCatalogEntry(
            strategy_id=strategy_id,
            aps_id="APS-STRAT-REGISTRY-001",
            name=config.strategy.description or strategy_id.replace("_", " ").title(),
            status="MVP",
        )
        for strategy_id, config in builtin_strategy_registry().items()
    )


STRATEGY_CATALOG: tuple[StrategyCatalogEntry, ...] = build_strategy_catalog()


def lookup_strategy_aps(strategy_id: str) -> StrategyCatalogEntry | None:
    """Resolve APS metadata for a strategy id."""
    for entry in STRATEGY_CATALOG:
        if entry.strategy_id == strategy_id:
            return entry
    return None
