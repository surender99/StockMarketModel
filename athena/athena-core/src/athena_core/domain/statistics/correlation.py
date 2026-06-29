"""Correlation analysis — ATH-REL-009 §5.7, REQ-STAT-CORR-001."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np
import pandas as pd

CorrelationMethod = Literal["pearson", "spearman", "kendall"]


@dataclass(frozen=True)
class CorrelationResult:
    """Pairwise or matrix correlation output — FR-007."""

    method: str
    matrix: pd.DataFrame
    pairwise: dict[tuple[str, str], float]


def correlation_matrix(
    data: pd.DataFrame,
    *,
    method: CorrelationMethod = "pearson",
) -> CorrelationResult:
    """Compute correlation matrix — REQ-STAT-CORR-001."""
    numeric = data.select_dtypes(include=[np.number])
    if numeric.empty:
        return CorrelationResult(method=method, matrix=pd.DataFrame(), pairwise={})

    if method == "pearson":
        mat = numeric.corr(method="pearson")
    elif method == "spearman":
        mat = numeric.corr(method="spearman")
    else:
        mat = numeric.corr(method="kendall")

    pairwise: dict[tuple[str, str], float] = {}
    cols = list(mat.columns)
    for i, a in enumerate(cols):
        for b in cols[i + 1 :]:
            val = mat.loc[a, b]
            if np.isfinite(val):
                pairwise[(a, b)] = float(val)

    return CorrelationResult(method=method, matrix=mat, pairwise=pairwise)


def cross_correlation(
    series_a: pd.Series,
    series_b: pd.Series,
    *,
    max_lag: int = 5,
) -> dict[int, float]:
    """Cross-correlation at lags -max_lag..max_lag."""
    a = series_a.astype(float).dropna()
    b = series_b.astype(float).dropna()
    aligned = pd.concat([a, b], axis=1, join="inner")
    if aligned.empty:
        return {}
    x = aligned.iloc[:, 0].to_numpy()
    y = aligned.iloc[:, 1].to_numpy()
    x = (x - x.mean()) / (x.std() or 1.0)
    y = (y - y.mean()) / (y.std() or 1.0)
    n = len(x)
    result: dict[int, float] = {}
    for lag in range(-max_lag, max_lag + 1):
        if lag >= 0:
            corr = float(np.dot(x[: n - lag], y[lag:]) / n) if lag < n else 0.0
        else:
            corr = float(np.dot(x[-lag:], y[: n + lag]) / n) if -lag < n else 0.0
        result[lag] = corr
    return result
