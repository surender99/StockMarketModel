"""Portfolio allocation model registry — ATH-REL-008 §5.1."""

from __future__ import annotations

from athena_core.domain.portfolio.allocation import ALLOCATION_MODELS
from athena_core.domain.plugins import Plugin, PluginMetadata, PluginRegistry, PluginType


def list_allocation_models() -> dict[str, str]:
    """Return registered allocation model ids and descriptions."""
    return dict(ALLOCATION_MODELS)


def register_builtin_portfolio_plugins(registry: PluginRegistry) -> int:
    """Register allocation models as report plugins — ATH-REL-008 §5.1."""
    plugins: list[Plugin] = []
    for model_id, description in ALLOCATION_MODELS.items():
        plugins.append(
            Plugin(
                id=f"allocation:{model_id}",
                version="0.1.0",
                plugin_type=PluginType.REPORT,
                metadata=PluginMetadata(name=model_id, description=description),
                configuration_schema={"allocation_model": model_id},
                execute=None,
            )
        )
    return registry.discover(plugins)
