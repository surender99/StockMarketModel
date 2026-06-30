"""Plugin registry — athena-os wrapper mapping errors to athena-core types."""

from __future__ import annotations

from collections.abc import Iterable

from athena_os.errors import PluginError as OSPluginError
from athena_os.plugins import Plugin, PluginLifecycle, PluginType
from athena_os.plugins import PluginRegistry as _PluginRegistry

from athena_core.domain.errors import PluginError

__all__ = ["PluginRegistry"]


def _map_plugin_error(fn):  # type: ignore[no-untyped-def]
    def wrapper(*args, **kwargs):  # type: ignore[no-untyped-def]
        try:
            return fn(*args, **kwargs)
        except OSPluginError as exc:
            raise PluginError(str(exc), context=exc.context) from exc

    return wrapper


class PluginRegistry(_PluginRegistry):
    @_map_plugin_error
    def register(self, plugin: Plugin, *, activate: bool = True) -> None:
        super().register(plugin, activate=activate)

    @_map_plugin_error
    def unregister(self, plugin_id: str) -> Plugin:
        return super().unregister(plugin_id)

    @_map_plugin_error
    def get(self, plugin_id: str) -> Plugin:
        return super().get(plugin_id)

    def register_many(self, plugins: Iterable[Plugin], *, activate: bool = True) -> None:
        for plugin in plugins:
            self.register(plugin, activate=activate)

    def discover(self, plugins: Iterable[Plugin], *, activate: bool = True) -> int:
        added = 0
        for plugin in plugins:
            if plugin.id in self._plugins:  # noqa: SLF001
                continue
            self.register(plugin, activate=activate)
            added += 1
        return added
