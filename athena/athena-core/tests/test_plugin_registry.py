"""Plugin registry tests — AES-0202."""

from __future__ import annotations

import pytest

from athena_core.domain.errors import PluginError
from athena_core.domain.plugins import Plugin, PluginLifecycle, PluginMetadata, PluginRegistry, PluginType


def test_register_and_get_plugin() -> None:
    registry = PluginRegistry()
    plugin = Plugin(
        id="ema",
        version="1.0.0",
        plugin_type=PluginType.INDICATOR,
        metadata=PluginMetadata(name="EMA", description="Exponential moving average"),
        configuration_schema={"period": {"type": "integer", "minimum": 1}},
        execute=lambda df, params: df["close"].ewm(span=params["period"]).mean(),
    )
    registry.register(plugin)
    assert registry.get("ema") is plugin
    assert plugin.lifecycle == PluginLifecycle.ACTIVE


def test_list_filters_by_type() -> None:
    registry = PluginRegistry()
    registry.register(
        Plugin(
            id="ema",
            version="1.0.0",
            plugin_type=PluginType.INDICATOR,
            metadata=PluginMetadata(name="EMA"),
        )
    )
    registry.register(
        Plugin(
            id="ema_cross",
            version="1.0.0",
            plugin_type=PluginType.STRATEGY,
            metadata=PluginMetadata(name="EMA Crossover"),
        )
    )
    indicators = registry.list(PluginType.INDICATOR)
    assert [p.id for p in indicators] == ["ema"]
    assert len(registry.list()) == 2


def test_duplicate_registration_raises() -> None:
    registry = PluginRegistry()
    plugin = Plugin(
        id="sma",
        version="1.0.0",
        plugin_type=PluginType.INDICATOR,
        metadata=PluginMetadata(name="SMA"),
    )
    registry.register(plugin)
    with pytest.raises(PluginError, match="already registered"):
        registry.register(plugin)


def test_unknown_plugin_raises() -> None:
    registry = PluginRegistry()
    with pytest.raises(PluginError, match="unknown plugin"):
        registry.get("missing")
