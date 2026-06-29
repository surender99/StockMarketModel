"""File-backed dataset registry — REQ-DATA-REGISTRY-001, ATH-REL-002 §10."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from athena_core.domain.data.registry import DatasetDescriptor, DatasetKind
from athena_core.domain.ports.dataset_registry import DatasetRegistryPort


class FileDatasetRegistry(DatasetRegistryPort):
    """JSON index of dataset descriptors under a base directory."""

    def __init__(self, registry_path: Path | str) -> None:
        self._base = Path(registry_path)
        self._base.mkdir(parents=True, exist_ok=True)
        self._index_path = self._base / "index.json"
        if not self._index_path.is_file():
            self._write_index([])

    def _read_index(self) -> list[dict[str, Any]]:
        raw = json.loads(self._index_path.read_text(encoding="utf-8"))
        entries = raw.get("datasets", []) if isinstance(raw, dict) else raw
        return list(entries)

    def _write_index(self, entries: list[dict[str, Any]]) -> None:
        payload = {"datasets": entries}
        self._index_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    @staticmethod
    def _to_dict(descriptor: DatasetDescriptor) -> dict[str, Any]:
        return {
            "dataset_id": descriptor.dataset_id,
            "kind": descriptor.kind.value,
            "path": descriptor.path,
            "data_version": descriptor.data_version,
            "content_version": descriptor.content_version,
            "checksum_sha256": descriptor.checksum_sha256,
            "symbol": descriptor.symbol,
            "source": descriptor.source,
            "row_count": descriptor.row_count,
            "registered_at": descriptor.registered_at.replace(tzinfo=UTC).isoformat(),
        }

    @staticmethod
    def _from_dict(data: dict[str, Any]) -> DatasetDescriptor:
        registered = datetime.fromisoformat(str(data["registered_at"]))
        if registered.tzinfo is None:
            registered = registered.replace(tzinfo=UTC)
        return DatasetDescriptor(
            dataset_id=str(data["dataset_id"]),
            kind=DatasetKind(str(data["kind"])),
            path=str(data["path"]),
            data_version=str(data["data_version"]),
            content_version=str(data["content_version"]),
            checksum_sha256=str(data["checksum_sha256"]),
            symbol=str(data.get("symbol", "")),
            source=str(data.get("source", "")),
            row_count=int(data.get("row_count", 0)),
            registered_at=registered,
        )

    def register(self, descriptor: DatasetDescriptor) -> None:
        entries = self._read_index()
        payload = self._to_dict(descriptor)
        replaced = False
        for idx, item in enumerate(entries):
            if item.get("dataset_id") == descriptor.dataset_id:
                entries[idx] = payload
                replaced = True
                break
        if not replaced:
            entries.append(payload)
        self._write_index(entries)

    def get(self, dataset_id: str) -> DatasetDescriptor | None:
        for item in self._read_index():
            if item.get("dataset_id") == dataset_id:
                return self._from_dict(item)
        return None

    def list_datasets(self, *, kind: DatasetKind | None = None) -> list[DatasetDescriptor]:
        descriptors = [self._from_dict(item) for item in self._read_index()]
        if kind is None:
            return descriptors
        return [item for item in descriptors if item.kind == kind]
