"""Composition root bootstrap — ATH-REL-001 §02, §03, §04."""

from __future__ import annotations

import logging
from dataclasses import dataclass

from athena_core.application.config import AthenaConfig
from athena_core.application.container import ServiceContainer
from athena_core.domain.events import EventBus
from athena_core.domain.plugins import PluginRegistry
from athena_core.infrastructure.logging import configure_logging


@dataclass
class CoreContext:
    """Wired core framework services for runtime and SDK consumers."""

    config: AthenaConfig
    container: ServiceContainer
    plugin_registry: PluginRegistry
    event_bus: EventBus


def bootstrap_athena_core(config: AthenaConfig) -> CoreContext:
    """Build the Release-01 core framework context from configuration."""
    core = config.core
    configure_logging(
        level=getattr(logging, core.logging.level.upper(), logging.INFO),
        json_logs=core.logging.json_logs,
    )

    container = ServiceContainer()
    plugin_registry = PluginRegistry()
    event_bus = EventBus()

    container.register("config", lambda: config, singleton=True)
    container.register("plugin_registry", lambda: plugin_registry, singleton=True)
    container.register("event_bus", lambda: event_bus, singleton=True)

    return CoreContext(
        config=config,
        container=container,
        plugin_registry=plugin_registry,
        event_bus=event_bus,
    )
