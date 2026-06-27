"""Plugin registry — AES-0202 stub."""

from __future__ import annotations

from athena_core.domain.plugins.base import Plugin, PluginType


class PluginRegistry:
    """In-memory plugin registry for future indicator/pattern/strategy plugins."""

    def __init__(self) -> None:
        self._plugins: dict[str, Plugin] = {}

    def register(self, plugin: Plugin) -> None:
        if plugin.id in self._plugins:
            msg = f"plugin already registered: {plugin.id}"
            raise ValueError(msg)
        self._plugins[plugin.id] = plugin

    def get(self, plugin_id: str) -> Plugin:
        plugin = self._plugins.get(plugin_id)
        if plugin is None:
            msg = f"unknown plugin: {plugin_id}"
            raise KeyError(msg)
        return plugin

    def list(self, plugin_type: PluginType | None = None) -> list[Plugin]:
        plugins = list(self._plugins.values())
        if plugin_type is None:
            return plugins
        return [plugin for plugin in plugins if plugin.plugin_type == plugin_type]
