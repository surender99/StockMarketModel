"""Composition root bootstrap — ATH-REL-001 §02, §03, §04; ATH-REL-002 data platform."""

from __future__ import annotations

import logging
from dataclasses import dataclass

from athena_core.application.config import AthenaConfig
from athena_core.application.container import ServiceContainer
from athena_core.application.data_bootstrap import DataContext, bootstrap_data_platform
from athena_core.domain.events import EventBus
from athena_core.domain.features.indicator_plugins import register_builtin_indicators
from athena_core.domain.patterns.pattern_plugins import register_builtin_patterns
from athena_core.domain.backtest.backtest_plugins import register_builtin_backtest_plugins
from athena_core.domain.strategy.strategy_plugins import register_builtin_strategies
from athena_core.domain.plugins import PluginRegistry
from athena_core.infrastructure.logging import configure_logging


@dataclass
class CoreContext:
    """Wired core framework services for runtime and SDK consumers."""

    config: AthenaConfig
    container: ServiceContainer
    plugin_registry: PluginRegistry
    event_bus: EventBus
    data: DataContext | None = None


def bootstrap_athena_core(config: AthenaConfig, *, wire_data: bool = True) -> CoreContext:
    """Build the Release-01 core framework context from configuration."""
    core = config.core
    configure_logging(
        level=getattr(logging, core.logging.level.upper(), logging.INFO),
        json_logs=core.logging.json_logs,
    )

    container = ServiceContainer()
    plugin_registry = PluginRegistry()
    register_builtin_indicators(plugin_registry)
    register_builtin_patterns(plugin_registry)
    register_builtin_strategies(plugin_registry)
    register_builtin_backtest_plugins(plugin_registry)
    event_bus = EventBus()
    data_ctx = bootstrap_data_platform(config) if wire_data else None

    container.register("config", lambda: config, singleton=True)
    container.register("plugin_registry", lambda: plugin_registry, singleton=True)
    container.register("event_bus", lambda: event_bus, singleton=True)
    if data_ctx is not None:
        container.register("data", lambda: data_ctx, singleton=True)

    return CoreContext(
        config=config,
        container=container,
        plugin_registry=plugin_registry,
        event_bus=event_bus,
        data=data_ctx,
    )
