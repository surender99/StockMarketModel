"""Machine learning platform framework tests — ATH-REL-011."""

from __future__ import annotations

import pandas as pd

from athena_core.application.bootstrap import bootstrap_athena_core
from athena_core.application.config import AthenaConfig
from athena_core.application.ml_manager import MLManager
from athena_core.domain.ml import (
    bayesian_search,
    build_dataset_splits,
    build_ml_registry,
    correlation_filter,
    detect_drift,
    evaluate_classifier,
    grid_search,
    importance_ranking,
    list_ml_modules,
    random_search,
    register_builtin_ml_plugins,
    train_supervised,
)
from athena_core.domain.ml.context import MLContext
from athena_core.domain.ml.model_registry import ModelRegistry
from athena_core.domain.plugins import PluginType


def _sample_data(n: int = 100) -> tuple[pd.DataFrame, pd.Series]:
    features = pd.DataFrame(
        {
            "f1": range(n),
            "f2": [i * 0.5 for i in range(n)],
            "f3": [i % 3 for i in range(n)],
        }
    )
    target = pd.Series([1 if i > 50 else 0 for i in range(n)], name="label")
    return features, target


def test_req_ml_dataset_001_splits() -> None:
    """REQ-ML-DATASET-001 — dataset splits."""
    data = pd.DataFrame({"x": range(100)})
    splits = build_dataset_splits(data, method="time_series")
    assert len(splits) == 1
    assert len(splits[0].train) > 0
    wf = build_dataset_splits(data, method="walk_forward", n_folds=2)
    assert len(wf) == 2


def test_req_ml_features_001_selection() -> None:
    """REQ-ML-FEATURES-001 — feature selection."""
    features, target = _sample_data()
    kept = correlation_filter(features, threshold=0.99)
    assert len(kept) >= 1
    ranked = importance_ranking(features, target, top_k=2)
    assert len(ranked) == 2


def test_req_ml_training_001_supervised() -> None:
    """REQ-ML-TRAINING-001 — supervised training."""
    features, target = _sample_data()
    result = train_supervised(features, target)
    assert result.metrics["accuracy"] >= 0.0
    assert len(result.feature_names) == 3


def test_req_ml_registry_001_model_registry() -> None:
    """REQ-ML-REGISTRY-001 — model registry."""
    from athena_core.domain.ml.context import ModelMetadata

    registry = ModelRegistry()
    meta = ModelMetadata("m1", "0.1.0", "logistic_stub", ("f1",), {"accuracy": 0.8})
    registry.register("m1", "0.1.0", "models/m1", meta)
    assert registry.get("m1") is not None
    assert registry.list_models() == ["m1"]


def test_req_ml_evaluation_001_metrics() -> None:
    """REQ-ML-EVALUATION-001 — evaluation metrics."""
    y_true = pd.Series([1, 0, 1, 0, 1])
    y_pred = pd.Series([1, 0, 0, 0, 1])
    metrics = evaluate_classifier(y_true, y_pred)
    assert metrics.accuracy == 0.8
    assert 0.0 <= metrics.precision <= 1.0


def test_req_ml_drift_001_detection() -> None:
    """REQ-ML-DRIFT-001 — drift detection."""
    ref = pd.DataFrame({"x": [1.0, 2.0, 3.0]})
    cur = pd.DataFrame({"x": [10.0, 11.0, 12.0]})
    report = detect_drift(ref, cur, threshold=0.1)
    assert report.drift_detected


def test_req_ml_optimizer_001_hyperparameter() -> None:
    """REQ-ML-OPTIMIZER-001 — hyperparameter search."""
    result = grid_search(
        {"lr": [0.01, 0.1], "depth": [2, 4]},
        lambda p: p["lr"] * p["depth"],
    )
    assert result.score > 0
    rand = random_search({"lr": (0.0, 1.0)}, lambda p: p["lr"], n_trials=5)
    assert rand.method == "random_search"
    bayes = bayesian_search({"lr": (0.0, 1.0)}, lambda p: p["lr"], n_trials=3)
    assert bayes.method == "bayesian_search"


def test_ml_manager_orchestration() -> None:
    """FR-012 — MLManager orchestration."""
    features, target = _sample_data()
    mgr = MLManager()
    ctx = MLContext("ds1", list(features.columns), "label")
    splits = mgr.prepare_dataset(pd.concat([features, target], axis=1), ctx)
    assert splits
    selected = mgr.select_features(features, target, top_k=2)
    assert len(selected) == 2
    result = mgr.train(features[selected], target, model_id="test_model")
    assert result.metrics["accuracy"] >= 0.0


def test_ml_plugins_registered() -> None:
    """FR-015 — ML plugins in bootstrap."""
    ctx = bootstrap_athena_core(AthenaConfig())
    ml_plugins = ctx.plugin_registry.list(PluginType.ML_MODEL)
    assert len(ml_plugins) >= 7
    assert "feature_selection" in list_ml_modules()
    assert len(build_ml_registry().list_modules()) == 7
