"""ML platform manager — ATH-REL-011 §5.1, FR-012."""

from __future__ import annotations

from typing import Any

import pandas as pd

from athena_core.application.ml_scorer import MLSignalScorer
from athena_core.domain.ml.context import MLContext, ModelMetadata
from athena_core.domain.ml.dataset_builder import DatasetSplit, build_dataset_splits
from athena_core.domain.ml.drift import DriftReport, detect_drift
from athena_core.domain.ml.evaluation import ClassificationMetrics, evaluate_classifier
from athena_core.domain.ml.feature_selection import (
    correlation_filter,
    importance_ranking,
    recursive_elimination,
)
from athena_core.domain.ml.hyperparameter import HyperparameterResult, grid_search
from athena_core.domain.ml.ml_plugins import MLRegistry, build_ml_registry
from athena_core.domain.ml.model_registry import ModelRegistry
from athena_core.domain.ml.training import TrainingResult, train_supervised


class MLManager:
    """Orchestrate ML platform workflows — extends MLSignalScorer."""

    def __init__(
        self,
        *,
        registry: ModelRegistry | None = None,
        module_registry: MLRegistry | None = None,
        scorer: MLSignalScorer | None = None,
    ) -> None:
        self._registry = registry or ModelRegistry()
        self._modules = module_registry or build_ml_registry()
        self._scorer = scorer

    @property
    def model_registry(self) -> ModelRegistry:
        return self._registry

    @property
    def module_registry(self) -> MLRegistry:
        return self._modules

    def prepare_dataset(
        self,
        data: pd.DataFrame,
        context: MLContext,
    ) -> list[DatasetSplit]:
        """Build dataset splits per context — REQ-ML-DATASET-001."""
        method = context.split_method  # type: ignore[arg-type]
        return build_dataset_splits(data, method=method)

    def select_features(
        self,
        features: pd.DataFrame,
        target: pd.Series,
        *,
        method: str = "importance",
        top_k: int = 10,
    ) -> list[str]:
        """Feature selection pipeline — REQ-ML-FEATURES-001."""
        filtered = correlation_filter(features)
        subset = features[filtered]
        if method == "rfe":
            return recursive_elimination(subset, target, n_features=top_k)
        ranked = importance_ranking(subset, target, top_k=top_k)
        return [name for name, _ in ranked]

    def train(
        self,
        features: pd.DataFrame,
        target: pd.Series,
        *,
        model_id: str = "default",
    ) -> TrainingResult:
        """Train and register model — REQ-ML-TRAINING-001."""
        result = train_supervised(features, target)
        metadata = ModelMetadata(
            model_id=model_id,
            version="0.1.0",
            algorithm=result.model_type,
            features=tuple(result.feature_names),
            metrics=result.metrics,
        )
        self._registry.register(model_id, "0.1.0", artifact_path=f"models/{model_id}/0.1.0", metadata=metadata)
        return result

    def evaluate(
        self,
        y_true: pd.Series,
        y_pred: pd.Series,
        *,
        y_score: pd.Series | None = None,
        feature_importance: dict[str, float] | None = None,
    ) -> ClassificationMetrics:
        return evaluate_classifier(y_true, y_pred, y_score=y_score, feature_importance=feature_importance)

    def optimize_hyperparameters(
        self,
        param_grid: dict[str, list[Any]],
        objective,
    ) -> HyperparameterResult:
        return grid_search(param_grid, objective)

    def check_drift(
        self,
        reference: pd.DataFrame,
        current: pd.DataFrame,
        **kwargs,
    ) -> DriftReport:
        return detect_drift(reference, current, **kwargs)

    def integrate_scorer(self, scorer: MLSignalScorer) -> None:
        """Wire existing MLSignalScorer — extend don't duplicate."""
        self._scorer = scorer
