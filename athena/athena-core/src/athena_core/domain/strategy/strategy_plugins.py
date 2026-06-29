"""Strategy plugin registry — REQ-STRAT-REGISTRY-001, ATH-REL-006 §5.2."""

from __future__ import annotations

from collections.abc import Callable

from athena_core.domain.plugins import Plugin, PluginMetadata, PluginRegistry, PluginType
from athena_core.domain.strategy.builtin import builtin_strategy_registry
from athena_core.domain.strategy.config import StrategyConfig

StrategyFactory = Callable[[], StrategyConfig]


def build_strategy_plugin(
    strategy_id: str,
    *,
    version: str,
    name: str,
    description: str,
    factory: StrategyFactory,
) -> Plugin:
    """Wrap a strategy template factory as an AES-0202 StrategyProvider plugin."""
    return Plugin(
        id=strategy_id,
        version=version,
        plugin_type=PluginType.STRATEGY,
        metadata=PluginMetadata(name=name, description=description),
        configuration_schema={},
        execute=factory,
    )


def register_builtin_strategies(registry: PluginRegistry) -> int:
    """Register all built-in strategy templates — REQ-STRAT-REGISTRY-001."""
    plugins = [
        build_strategy_plugin(
            strategy_id,
            version=config.strategy.version,
            name=strategy_id.replace("_", " ").title(),
            description=config.strategy.description or f"Strategy: {strategy_id}",
            factory=lambda c=config: c.model_copy(deep=True),
        )
        for strategy_id, config in builtin_strategy_registry().items()
    ]
    return registry.discover(plugins)


def resolve_strategy(registry: PluginRegistry, strategy_id: str) -> StrategyConfig:
    """Resolve an active strategy plugin to a StrategyConfig template."""
    plugin = registry.get(strategy_id)
    if plugin.plugin_type != PluginType.STRATEGY:
        msg = f"plugin is not a strategy: {strategy_id}"
        raise ValueError(msg)
    if plugin.execute is None:
        msg = f"strategy plugin has no factory: {strategy_id}"
        raise ValueError(msg)
    config = plugin.execute()
    if not isinstance(config, StrategyConfig):
        msg = f"strategy plugin factory must return StrategyConfig: {strategy_id}"
        raise TypeError(msg)
    return config
