"""Plugin registry — AES-0202 stub."""

from athena_core.domain.plugins.base import Plugin, PluginLifecycle, PluginMetadata, PluginType
from athena_core.domain.plugins.registry import PluginRegistry

__all__ = ["Plugin", "PluginLifecycle", "PluginMetadata", "PluginRegistry", "PluginType"]
