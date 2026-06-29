"""Machine learning domain — ATH-REL-011."""

from athena_core.domain.ml.context import MLContext, ModelMetadata
from athena_core.domain.ml.dataset_builder import DatasetSplit, build_dataset_splits
from athena_core.domain.ml.drift import DriftReport, detect_drift
from athena_core.domain.ml.evaluation import ClassificationMetrics, evaluate_classifier
from athena_core.domain.ml.feature_selection import (
    correlation_filter,
    importance_ranking,
    recursive_elimination,
)
from athena_core.domain.ml.hyperparameter import (
    HyperparameterResult,
    bayesian_search,
    grid_search,
    random_search,
)
from athena_core.domain.ml.ml_plugins import (
    build_ml_registry,
    list_ml_modules,
    register_builtin_ml_plugins,
)
from athena_core.domain.ml.model_registry import ModelRegistry, ModelVersion
from athena_core.domain.ml.training import TrainingResult, train_supervised

__all__ = [
    "ClassificationMetrics",
    "DatasetSplit",
    "DriftReport",
    "HyperparameterResult",
    "MLContext",
    "ModelMetadata",
    "ModelRegistry",
    "ModelVersion",
    "TrainingResult",
    "bayesian_search",
    "build_dataset_splits",
    "build_ml_registry",
    "correlation_filter",
    "detect_drift",
    "evaluate_classifier",
    "grid_search",
    "importance_ranking",
    "list_ml_modules",
    "random_search",
    "recursive_elimination",
    "register_builtin_ml_plugins",
    "train_supervised",
]
