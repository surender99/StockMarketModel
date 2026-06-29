"""Dataset builder — ATH-REL-011 §5.2, REQ-ML-DATASET-001."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import pandas as pd

SplitMethod = Literal["holdout", "time_series", "walk_forward"]


@dataclass(frozen=True)
class DatasetSplit:
    """Train/validation/test partition."""

    train: pd.DataFrame
    validation: pd.DataFrame
    test: pd.DataFrame
    method: SplitMethod
    fold_index: int | None = None


def build_dataset_splits(
    data: pd.DataFrame,
    *,
    method: SplitMethod = "time_series",
    train_ratio: float = 0.7,
    val_ratio: float = 0.15,
    n_folds: int = 3,
) -> list[DatasetSplit]:
    """Build dataset splits — train/val/test, time-series, walk-forward."""
    if data.empty:
        return [DatasetSplit(data, data, data, method)]

    if method == "holdout":
        return [_holdout_split(data, train_ratio, val_ratio, method)]

    if method == "time_series":
        return [_time_series_split(data, train_ratio, val_ratio, method)]

    return _walk_forward_splits(data, n_folds, val_ratio, method)


def _holdout_split(
    data: pd.DataFrame,
    train_ratio: float,
    val_ratio: float,
    method: SplitMethod,
) -> DatasetSplit:
    n = len(data)
    train_end = int(n * train_ratio)
    val_end = int(n * (train_ratio + val_ratio))
    return DatasetSplit(
        train=data.iloc[:train_end],
        validation=data.iloc[train_end:val_end],
        test=data.iloc[val_end:],
        method=method,
    )


def _time_series_split(
    data: pd.DataFrame,
    train_ratio: float,
    val_ratio: float,
    method: SplitMethod,
) -> DatasetSplit:
    return _holdout_split(data, train_ratio, val_ratio, method)


def _walk_forward_splits(
    data: pd.DataFrame,
    n_folds: int,
    val_ratio: float,
    method: SplitMethod,
) -> list[DatasetSplit]:
    n = len(data)
    fold_size = max(1, n // (n_folds + 1))
    splits: list[DatasetSplit] = []
    for fold in range(n_folds):
        train_end = fold_size * (fold + 1)
        val_end = min(n, train_end + max(1, int(fold_size * val_ratio)))
        test_end = min(n, val_end + fold_size)
        splits.append(
            DatasetSplit(
                train=data.iloc[:train_end],
                validation=data.iloc[train_end:val_end],
                test=data.iloc[val_end:test_end],
                method=method,
                fold_index=fold,
            )
        )
    return splits
