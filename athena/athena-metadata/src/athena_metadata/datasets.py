"""Dataset metadata identifiers."""

from athena_core.domain.data.registry import DatasetKind

DATASET_IDS: tuple[str, ...] = tuple(k.value for k in DatasetKind)

__all__ = ["DATASET_IDS", "DatasetKind"]
