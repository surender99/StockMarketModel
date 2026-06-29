"""Evaluation engine — ATH-REL-011 §5.6, REQ-ML-EVALUATION-001."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class ClassificationMetrics:
    """Classification evaluation metrics."""

    accuracy: float
    precision: float
    recall: float
    f1: float
    roc_auc: float
    pr_auc: float
    feature_importance: dict[str, float]


def evaluate_classifier(
    y_true: pd.Series,
    y_pred: pd.Series,
    *,
    y_score: pd.Series | None = None,
    feature_importance: dict[str, float] | None = None,
) -> ClassificationMetrics:
    """Compute accuracy, precision, recall, ROC, PR metrics."""
    aligned = pd.concat([y_true, y_pred], axis=1).dropna()
    if aligned.empty:
        return ClassificationMetrics(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, feature_importance or {})

    yt = aligned.iloc[:, 0].astype(float).to_numpy()
    yp = aligned.iloc[:, 1].astype(float).to_numpy()
    accuracy = float(np.mean(yt == yp))
    tp = float(np.sum((yp == 1) & (yt == 1)))
    fp = float(np.sum((yp == 1) & (yt == 0)))
    fn = float(np.sum((yp == 0) & (yt == 1)))
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

    roc_auc = _roc_auc(yt, y_score) if y_score is not None else accuracy
    pr_auc = _pr_auc(yt, y_score) if y_score is not None else precision
    return ClassificationMetrics(
        accuracy=accuracy,
        precision=precision,
        recall=recall,
        f1=f1,
        roc_auc=roc_auc,
        pr_auc=pr_auc,
        feature_importance=feature_importance or {},
    )


def _roc_auc(y_true: np.ndarray, y_score: pd.Series) -> float:
    scores = y_score.reindex(range(len(y_true))).fillna(0.5).to_numpy()
    order = np.argsort(scores)
    ranks = np.empty_like(order, dtype=float)
    ranks[order] = np.arange(len(scores))
    pos = y_true == 1
    n_pos = pos.sum()
    n_neg = len(y_true) - n_pos
    if n_pos == 0 or n_neg == 0:
        return 0.5
    rank_sum = ranks[pos].sum()
    return float((rank_sum - n_pos * (n_pos - 1) / 2) / (n_pos * n_neg))


def _pr_auc(y_true: np.ndarray, y_score: pd.Series) -> float:
    scores = y_score.reindex(range(len(y_true))).fillna(0.5).to_numpy()
    thresholds = np.linspace(0, 1, 11)
    precisions: list[float] = []
    for t in thresholds:
        pred = (scores >= t).astype(float)
        tp = np.sum((pred == 1) & (y_true == 1))
        fp = np.sum((pred == 1) & (y_true == 0))
        precisions.append(tp / (tp + fp) if (tp + fp) > 0 else 0.0)
    return float(np.mean(precisions))
