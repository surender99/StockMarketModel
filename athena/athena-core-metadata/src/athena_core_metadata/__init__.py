"""Core metadata catalogs — facade over athena-core."""

from athena_core.domain.indicators.catalog import INDICATOR_CATALOG
from athena_core.domain.patterns.catalog import PATTERN_CATALOG
from athena_core.domain.strategy.catalog import STRATEGY_CATALOG

__all__ = ["INDICATOR_CATALOG", "PATTERN_CATALOG", "STRATEGY_CATALOG"]
