"""Pattern plugin registry — REQ-PAT-REGISTRY-001, ATH-REL-005 §01."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import pandas as pd

from athena_core.domain.patterns.base import PatternDetector, builtin_pattern_registry
from athena_core.domain.patterns.series import compute_pattern_series
from athena_core.domain.patterns.types import PatternEvent
from athena_core.domain.plugins import Plugin, PluginMetadata, PluginRegistry, PluginType

PatternFn = Callable[[pd.DataFrame], list[PatternEvent]]


def build_pattern_plugin(
    pattern_id: str,
    *,
    version: str,
    name: str,
    description: str,
    detect_fn: PatternFn,
) -> Plugin:
    """Wrap a pattern detector as an AES-0202 PatternProvider plugin."""
    return Plugin(
        id=pattern_id,
        version=version,
        plugin_type=PluginType.PATTERN,
        metadata=PluginMetadata(name=name, description=description),
        configuration_schema={},
        execute=detect_fn,
    )


def register_builtin_patterns(registry: PluginRegistry) -> int:
    """Register all built-in pattern detectors — REQ-PAT-REGISTRY-001."""
    plugins = [
        build_pattern_plugin(
            pattern_id,
            version="0.1.0",
            name=pattern_id.replace("_", " ").title(),
            description=f"Pattern detector: {pattern_id}",
            detect_fn=detect_fn,
        )
        for pattern_id, detect_fn in builtin_pattern_registry().items()
    ]
    return registry.discover(plugins)


def resolve_pattern(registry: PluginRegistry, pattern_id: str) -> PatternFn:
    """Resolve an active pattern plugin execute callable."""
    plugin = registry.get(pattern_id)
    if plugin.plugin_type != PluginType.PATTERN:
        msg = f"plugin is not a pattern: {pattern_id}"
        raise ValueError(msg)
    if plugin.execute is None:
        msg = f"pattern plugin has no execute callable: {pattern_id}"
        raise ValueError(msg)
    return plugin.execute  # type: ignore[return-value]


def pattern_to_feature_frame(
    ohlcv: pd.DataFrame,
    pattern_id: str,
    *,
    registry: PluginRegistry | None = None,
) -> pd.DataFrame:
    """Build feature frame for a pattern via PluginRegistry or PatternDetector."""
    detector: PatternDetector | None = None
    if registry is not None:
        detect_fn = resolve_pattern(registry, pattern_id)
        detector = PatternDetector({pattern_id: detect_fn})
    return compute_pattern_series(ohlcv, pattern_id, detector=detector)
