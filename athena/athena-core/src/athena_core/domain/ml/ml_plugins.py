"""ML plugin registration — ATH-REL-011 §5.1."""

from __future__ import annotations

from athena_core.domain.plugins import Plugin, PluginMetadata, PluginRegistry, PluginType

ML_MODULES: dict[str, str] = {
    "feature_selection": "Correlation filter, importance ranking, RFE",
    "dataset_builder": "Train/val/test, time-series, walk-forward splits",
    "model_registry": "Model storage, versioning, metadata",
    "training": "Supervised, unsupervised, reinforcement-ready",
    "hyperparameter": "Grid, random, Bayesian optimization",
    "evaluation": "Accuracy, precision, recall, ROC, PR",
    "drift": "Feature, concept, data drift detection",
}


class MLRegistry:
    """Registry of ML module descriptors — FR-015."""

    def __init__(self) -> None:
        self._modules: dict[str, str] = {}

    def register(self, module_id: str, description: str) -> None:
        self._modules[module_id] = description

    def list_modules(self) -> dict[str, str]:
        return dict(self._modules)


def build_ml_registry() -> MLRegistry:
    registry = MLRegistry()
    for mid, desc in ML_MODULES.items():
        registry.register(mid, desc)
    return registry


def register_builtin_ml_plugins(registry: PluginRegistry) -> int:
    """Register ML modules as model plugins."""
    plugins: list[Plugin] = []
    for module_id, description in ML_MODULES.items():
        plugins.append(
            Plugin(
                id=f"ml:{module_id}",
                version="0.1.0",
                plugin_type=PluginType.ML_MODEL,
                metadata=PluginMetadata(name=module_id, description=description),
                configuration_schema={"module": module_id},
                execute=None,
            )
        )
    return registry.discover(plugins)


def list_ml_modules() -> dict[str, str]:
    return dict(ML_MODULES)
