"""Backtest execution model registry — ATH-REL-007 §5.1."""

from __future__ import annotations

from athena_core.domain.backtest.execution import FillModel
from athena_core.domain.backtest.slippage import SlippageModel
from athena_core.domain.plugins import Plugin, PluginMetadata, PluginRegistry, PluginType

_BUILTIN_FILL_MODELS: dict[str, str] = {
    FillModel.CURRENT_BAR_CLOSE: "Fill at current bar close",
    FillModel.NEXT_BAR_OPEN: "Fill at next bar open",
    FillModel.MARKET: "Market order at bar close",
}

_BUILTIN_SLIPPAGE_MODELS: dict[str, str] = {
    SlippageModel.PERCENTAGE: "Percentage slippage",
    SlippageModel.FIXED: "Fixed tick slippage",
    SlippageModel.ATR_BASED: "ATR-scaled slippage",
    SlippageModel.VOLUME_BASED: "Volume participation slippage",
}


def list_fill_models() -> dict[str, str]:
    """Return registered fill model ids and descriptions."""
    return dict(_BUILTIN_FILL_MODELS)


def list_slippage_models() -> dict[str, str]:
    """Return registered slippage model ids and descriptions."""
    return dict(_BUILTIN_SLIPPAGE_MODELS)


def register_builtin_backtest_plugins(registry: PluginRegistry) -> int:
    """Register execution and slippage models as report plugins — ATH-REL-007 §5.1."""
    plugins: list[Plugin] = []
    for model_id, description in _BUILTIN_FILL_MODELS.items():
        plugins.append(
            Plugin(
                id=f"fill:{model_id}",
                version="0.1.0",
                plugin_type=PluginType.REPORT,
                metadata=PluginMetadata(name=model_id, description=description),
                configuration_schema={"fill_model": model_id},
                execute=None,
            )
        )
    for model_id, description in _BUILTIN_SLIPPAGE_MODELS.items():
        plugins.append(
            Plugin(
                id=f"slippage:{model_id}",
                version="0.1.0",
                plugin_type=PluginType.REPORT,
                metadata=PluginMetadata(name=model_id, description=description),
                configuration_schema={"slippage_model": model_id},
                execute=None,
            )
        )
    return registry.discover(plugins)
