"""Research pipeline stage registry — ATH-REL-010 §5.1."""

from __future__ import annotations

from athena_core.domain.plugins import Plugin, PluginMetadata, PluginRegistry, PluginType

PIPELINE_STAGES: dict[str, str] = {
    "feature_generation": "Generate features from OHLCV data",
    "indicator_execution": "Execute registered indicators",
    "strategy_evaluation": "Evaluate strategy signals and backtest",
    "result_storage": "Persist experiment results",
}


def list_pipeline_stages() -> dict[str, str]:
    """Return registered research pipeline stage ids."""
    return dict(PIPELINE_STAGES)


def register_builtin_research_plugins(registry: PluginRegistry) -> int:
    """Register research pipeline stages — ATH-REL-010 §5.4."""
    plugins: list[Plugin] = []
    for stage_id, description in PIPELINE_STAGES.items():
        plugins.append(
            Plugin(
                id=f"research:{stage_id}",
                version="0.1.0",
                plugin_type=PluginType.REPORT,
                metadata=PluginMetadata(name=stage_id, description=description),
                configuration_schema={"stage": stage_id},
                execute=None,
            )
        )
    return registry.discover(plugins)
