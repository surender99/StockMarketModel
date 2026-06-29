"""Descriptive distribution analysis — ATH-REL-009 §5.5, REQ-STAT-DIST-001."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class DistributionSummary:
    """Descriptive statistics for a numeric series — FR-002."""

    mean: float
    median: float
    mode: float | None
    variance: float
    std_dev: float
    skewness: float
    kurtosis: float
    q25: float
    q50: float
    q75: float
    min_value: float
    max_value: float
    count: int


def compute_distribution(series: pd.Series | np.ndarray) -> DistributionSummary:
    """Compute descriptive statistics — REQ-STAT-DIST-001."""
    arr = np.asarray(series, dtype=float)
    arr = arr[np.isfinite(arr)]
    if arr.size == 0:
        return DistributionSummary(
            mean=0.0,
            median=0.0,
            mode=None,
            variance=0.0,
            std_dev=0.0,
            skewness=0.0,
            kurtosis=0.0,
            q25=0.0,
            q50=0.0,
            q75=0.0,
            min_value=0.0,
            max_value=0.0,
            count=0,
        )

    mean = float(arr.mean())
    std = float(arr.std(ddof=1)) if arr.size > 1 else 0.0
    variance = float(arr.var(ddof=1)) if arr.size > 1 else 0.0
    median = float(np.median(arr))
    q25, q50, q75 = (float(x) for x in np.quantile(arr, [0.25, 0.5, 0.75]))

    mode_val: float | None = None
    if arr.size >= 1:
        rounded, counts = np.unique(np.round(arr, decimals=6), return_counts=True)
        if counts.size:
            mode_val = float(rounded[int(counts.argmax())])

    skew = float(_skewness(arr)) if arr.size > 2 else 0.0
    kurt = float(_excess_kurtosis(arr)) if arr.size > 3 else 0.0

    return DistributionSummary(
        mean=mean,
        median=median,
        mode=mode_val,
        variance=variance,
        std_dev=std,
        skewness=skew,
        kurtosis=kurt,
        q25=q25,
        q50=q50,
        q75=q75,
        min_value=float(arr.min()),
        max_value=float(arr.max()),
        count=int(arr.size),
    )


def _skewness(arr: np.ndarray) -> float:
    n = arr.size
    if n < 3:
        return 0.0
    m = arr.mean()
    s = arr.std(ddof=1)
    if s == 0:
        return 0.0
    return float(np.sum(((arr - m) / s) ** 3) * n / ((n - 1) * (n - 2)))


def _excess_kurtosis(arr: np.ndarray) -> float:
    n = arr.size
    if n < 4:
        return 0.0
    m = arr.mean()
    s = arr.std(ddof=1)
    if s == 0:
        return 0.0
    m4 = np.sum((arr - m) ** 4) / n
    return float(m4 / (s**4) - 3.0)
