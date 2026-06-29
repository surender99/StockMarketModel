"""Dataset registry port — REQ-DATA-REGISTRY-001, ATH-REL-002 §10."""

from __future__ import annotations

from abc import ABC, abstractmethod

from athena_core.domain.data.registry import DatasetDescriptor, DatasetKind


class DatasetRegistryPort(ABC):
    """Catalog of versioned datasets on local storage."""

    @abstractmethod
    def register(self, descriptor: DatasetDescriptor) -> None:
        """Add or update a dataset catalog entry."""

    @abstractmethod
    def get(self, dataset_id: str) -> DatasetDescriptor | None:
        """Return a descriptor by id, or None if unknown."""

    @abstractmethod
    def list_datasets(self, *, kind: DatasetKind | None = None) -> list[DatasetDescriptor]:
        """List registered datasets, optionally filtered by kind."""
