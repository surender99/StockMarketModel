"""Unified metadata registry."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from athena_metadata import benchmarks, datasets, indicators, parameters, patterns, strategies


@dataclass(frozen=True, slots=True)
class MetadataRegistry:
    """Aggregate view of Athena catalog metadata."""

    indicators: tuple[Any, ...]
    strategies: tuple[Any, ...]
    patterns: tuple[Any, ...]
    parameters: dict[str, Any]
    benchmarks: tuple[str, ...]
    datasets: tuple[str, ...]


def load_registry() -> MetadataRegistry:
    return MetadataRegistry(
        indicators=indicators.INDICATOR_CATALOG,
        strategies=strategies.STRATEGY_CATALOG,
        patterns=patterns.PATTERN_CATALOG,
        parameters=parameters.DEFAULT_PARAMETERS,
        benchmarks=benchmarks.BENCHMARK_IDS,
        datasets=datasets.DATASET_IDS,
    )


__all__ = ["MetadataRegistry", "load_registry"]
