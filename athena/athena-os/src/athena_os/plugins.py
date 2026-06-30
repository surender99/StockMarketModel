"""Plugin framework — APS-003, AES-0202."""

from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from athena_os.errors import PluginError


class PluginType(StrEnum):
    INDICATOR = "indicator"
    PATTERN = "pattern"
    STRATEGY = "strategy"
    RISK = "risk"
    REPORT = "report"
    ML_MODEL = "ml_model"


class PluginLifecycle(StrEnum):
    REGISTERED = "registered"
    ACTIVE = "active"
    DISABLED = "disabled"


@dataclass(frozen=True)
class PluginMetadata:
    name: str
    description: str = ""
    author: str = ""


@dataclass
class Plugin:
    id: str
    version: str
    plugin_type: PluginType
    metadata: PluginMetadata
    configuration_schema: dict[str, Any] = field(default_factory=dict)
    execute: Callable[..., Any] | None = None
    lifecycle: PluginLifecycle = PluginLifecycle.REGISTERED


class PluginRegistry:
    """In-memory plugin registry with lifecycle management."""

    def __init__(self) -> None:
        self._plugins: dict[str, Plugin] = {}

    def register(self, plugin: Plugin, *, activate: bool = True) -> None:
        if plugin.id in self._plugins:
            msg = f"plugin already registered: {plugin.id}"
            raise PluginError(msg, context={"plugin_id": plugin.id})
        if activate:
            plugin.lifecycle = PluginLifecycle.ACTIVE
        self._plugins[plugin.id] = plugin

    def unregister(self, plugin_id: str) -> Plugin:
        plugin = self._plugins.pop(plugin_id, None)
        if plugin is None:
            msg = f"unknown plugin: {plugin_id}"
            raise PluginError(msg, context={"plugin_id": plugin_id})
        return plugin

    def get(self, plugin_id: str) -> Plugin:
        plugin = self._plugins.get(plugin_id)
        if plugin is None:
            msg = f"unknown plugin: {plugin_id}"
            raise PluginError(msg, context={"plugin_id": plugin_id})
        return plugin

    def activate(self, plugin_id: str) -> None:
        self.get(plugin_id).lifecycle = PluginLifecycle.ACTIVE

    def disable(self, plugin_id: str) -> None:
        self.get(plugin_id).lifecycle = PluginLifecycle.DISABLED

    def list(
        self,
        plugin_type: PluginType | None = None,
        *,
        active_only: bool = False,
    ) -> list[Plugin]:
        plugins = list(self._plugins.values())
        if plugin_type is not None:
            plugins = [p for p in plugins if p.plugin_type == plugin_type]
        if active_only:
            plugins = [p for p in plugins if p.lifecycle == PluginLifecycle.ACTIVE]
        return plugins

    def register_many(self, plugins: Iterable[Plugin], *, activate: bool = True) -> None:
        for plugin in plugins:
            self.register(plugin, activate=activate)

    def discover(self, plugins: Iterable[Plugin], *, activate: bool = True) -> int:
        added = 0
        for plugin in plugins:
            if plugin.id in self._plugins:
                continue
            self.register(plugin, activate=activate)
            added += 1
        return added
