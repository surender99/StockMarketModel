"""Training framework — ATH-REL-011 §5.4, REQ-ML-TRAINING-001."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

import numpy as np
import pandas as pd

TrainingMode = Literal["supervised", "unsupervised", "reinforcement_ready"]


@dataclass
class TrainingResult:
    """Training output bundle."""

    model_type: str
    mode: TrainingMode
    feature_names: list[str]
    metrics: dict[str, float]
    coefficients: dict[str, float] = field(default_factory=dict)
    intercept: float = 0.0

    def predict_proba(self, features: pd.DataFrame) -> np.ndarray:
        """Logistic-style probability from linear scores."""
        if features.empty:
            return np.array([])
        cols = [c for c in self.feature_names if c in features.columns]
        x = features[cols].fillna(0.0).to_numpy()
        weights = np.array([self.coefficients.get(c, 0.0) for c in cols])
        logits = x @ weights + self.intercept
        return 1.0 / (1.0 + np.exp(-logits))


def train_supervised(
    features: pd.DataFrame,
    target: pd.Series,
    *,
    mode: TrainingMode = "supervised",
) -> TrainingResult:
    """Train a lightweight logistic-style model — extends MLSignalScorer pattern."""
    aligned = pd.concat([features, target], axis=1).dropna()
    if aligned.empty or aligned.shape[1] < 2:
        return TrainingResult(
            model_type="logistic_stub",
            mode=mode,
            feature_names=list(features.columns),
            metrics={"accuracy": 0.0},
        )

    x_cols = list(features.columns)
    x = aligned[x_cols].to_numpy(dtype=float)
    y = aligned.iloc[:, -1].to_numpy(dtype=float)
    x_bias = np.column_stack([np.ones(len(x)), x])
    try:
        coeffs, _, _, _ = np.linalg.lstsq(x_bias, y, rcond=None)
    except np.linalg.LinAlgError:
        coeffs = np.zeros(x_bias.shape[1])
    intercept = float(coeffs[0])
    weights = {col: float(coeffs[i + 1]) for i, col in enumerate(x_cols)}
    preds = x_bias @ coeffs
    pred_labels = (preds >= 0.5).astype(float)
    accuracy = float(np.mean(pred_labels == y)) if len(y) else 0.0
    return TrainingResult(
        model_type="logistic_stub",
        mode=mode,
        feature_names=x_cols,
        metrics={"accuracy": accuracy, "samples": float(len(y))},
        coefficients=weights,
        intercept=intercept,
    )


def train_unsupervised(features: pd.DataFrame) -> dict[str, Any]:
    """Cluster centroids stub for unsupervised mode."""
    if features.empty:
        return {"centroids": [], "n_clusters": 0}
    mean = features.mean().to_dict()
    return {"centroids": [mean], "n_clusters": 1}
