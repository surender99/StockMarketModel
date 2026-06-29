"""Feature selection — ATH-REL-011 §5.1, REQ-ML-FEATURES-001."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd


def correlation_filter(
    features: pd.DataFrame,
    *,
    threshold: float = 0.9,
) -> list[str]:
    """Remove highly correlated features — correlation filtering."""
    if features.empty or features.shape[1] <= 1:
        return list(features.columns)
    corr = features.corr().abs()
    upper = corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))
    drop: set[str] = set()
    for col in upper.columns:
        correlated = upper.index[upper[col] > threshold].tolist()
        drop.update(correlated)
    return [c for c in features.columns if c not in drop]


def importance_ranking(
    features: pd.DataFrame,
    target: pd.Series,
    *,
    top_k: int | None = None,
) -> list[tuple[str, float]]:
    """Rank features by absolute correlation with target."""
    if features.empty:
        return []
    scores: list[tuple[str, float]] = []
    for col in features.columns:
        aligned = pd.concat([features[col], target], axis=1).dropna()
        if len(aligned) < 2:
            scores.append((col, 0.0))
            continue
        corr = aligned.iloc[:, 0].corr(aligned.iloc[:, 1])
        scores.append((col, abs(float(corr)) if corr == corr else 0.0))
    scores.sort(key=lambda x: x[1], reverse=True)
    if top_k is not None:
        return scores[:top_k]
    return scores


def recursive_elimination(
    features: pd.DataFrame,
    target: pd.Series,
    *,
    n_features: int = 5,
) -> list[str]:
    """Greedy recursive feature elimination by correlation importance."""
    ranked = importance_ranking(features, target)
    return [name for name, _ in ranked[:n_features]]
