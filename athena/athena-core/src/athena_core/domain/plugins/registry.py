"""Plugin registry — AES-0202, ATH-REL-001 §03."""

from __future__ import annotations

from collections.abc import Iterable

from athena_core.domain.errors import PluginError
from athena_core.domain.plugins.base import Plugin, PluginLifecycle, PluginType


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
        plugin = self.get(plugin_id)
        plugin.lifecycle = PluginLifecycle.ACTIVE

    def disable(self, plugin_id: str) -> None:
        plugin = self.get(plugin_id)
        plugin.lifecycle = PluginLifecycle.DISABLED

    def list(
        self,
        plugin_type: PluginType | None = None,
        *,
        active_only: bool = False,
    ) -> list[Plugin]:
        plugins = list(self._plugins.values())
        if plugin_type is not None:
            plugins = [plugin for plugin in plugins if plugin.plugin_type == plugin_type]
        if active_only:
            plugins = [plugin for plugin in plugins if plugin.lifecycle == PluginLifecycle.ACTIVE]
        return plugins

    def register_many(self, plugins: Iterable[Plugin], *, activate: bool = True) -> None:
        for plugin in plugins:
            self.register(plugin, activate=activate)

    def discover(self, plugins: Iterable[Plugin], *, activate: bool = True) -> int:
        """Register plugins that are not already present; returns count added."""
        added = 0
        for plugin in plugins:
            if plugin.id in self._plugins:
                continue
            self.register(plugin, activate=activate)
            added += 1
        return added
