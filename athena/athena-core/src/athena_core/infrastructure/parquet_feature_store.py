"""Parquet feature store — REQ-FEAT-STORE-001."""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

import pandas as pd

from athena_core.domain.ports.feature_store import (
    FeatureCacheHit,
    FeatureCacheMiss,
    FeatureReadResult,
    FeatureStorePort,
)


def params_hash(params: dict[str, Any]) -> str:
    """SHA256 truncated hash of sorted JSON params — REQ-FEAT-STORE-001."""
    payload = json.dumps(params, sort_keys=True, default=str)
    return hashlib.sha256(payload.encode()).hexdigest()[:16]


class ParquetFeatureStore(FeatureStorePort):
    """Local Parquet feature store with metadata sidecar."""

    def __init__(self, base_path: Path | str, compression: str = "snappy") -> None:
        self._base = Path(base_path)
        self._base.mkdir(parents=True, exist_ok=True)
        self._compression = compression

    def _dir(self, symbol: str, feature_id: str, phash: str) -> Path:
        safe = symbol.replace("/", "_")
        return self._base / safe / feature_id / phash

    def _parquet_path(self, symbol: str, feature_id: str, phash: str) -> Path:
        return self._dir(symbol, feature_id, phash) / "values.parquet"

    def _meta_path(self, symbol: str, feature_id: str, phash: str) -> Path:
        return self._dir(symbol, feature_id, phash) / "metadata.json"

    def get(
        self,
        symbol: str,
        feature_id: str,
        params: dict[str, Any],
        data_version: str,
        start: date | None = None,
        end: date | None = None,
    ) -> FeatureReadResult:
        phash = params_hash(params)
        meta_path = self._meta_path(symbol, feature_id, phash)
        parquet_path = self._parquet_path(symbol, feature_id, phash)
        if not meta_path.is_file() or not parquet_path.is_file():
            return FeatureCacheMiss(reason="no_cache_entry")
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        if meta.get("data_version") != data_version:
            return FeatureCacheMiss(reason="data_version_mismatch")
        df = pd.read_parquet(parquet_path)
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"]).dt.date
            if start is not None:
                df = df[df["date"] >= start]
            if end is not None:
                df = df[df["date"] <= end]
        return FeatureCacheHit(data=df.reset_index(drop=True), path=str(parquet_path.parent))

    def put(
        self,
        symbol: str,
        feature_id: str,
        params: dict[str, Any],
        data_version: str,
        data: pd.DataFrame,
    ) -> str:
        phash = params_hash(params)
        target_dir = self._dir(symbol, feature_id, phash)
        target_dir.mkdir(parents=True, exist_ok=True)
        meta_path = self._meta_path(symbol, feature_id, phash)
        parquet_path = self._parquet_path(symbol, feature_id, phash)

        if meta_path.is_file():
            existing = json.loads(meta_path.read_text(encoding="utf-8"))
            if existing.get("data_version") != data_version:
                msg = (
                    f"Refusing overwrite: stored version {existing.get('data_version')} "
                    f"!= requested {data_version}"
                )
                raise ValueError(msg)

        out = data.copy()
        if "date" in out.columns:
            out["date"] = pd.to_datetime(out["date"]).dt.date

        fd, tmp_name = tempfile.mkstemp(suffix=".parquet", dir=target_dir)
        os.close(fd)
        tmp = Path(tmp_name)
        try:
            out.to_parquet(str(tmp), compression=self._compression, index=False)  # type: ignore[call-overload]
            tmp.replace(parquet_path)
        finally:
            if tmp.exists() and tmp != parquet_path:
                tmp.unlink(missing_ok=True)

        meta = {
            "feature_id": feature_id,
            "params": params,
            "data_version": data_version,
            "created_at": datetime.now(UTC).isoformat(),
            "row_count": len(out),
        }
        meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")
        return str(target_dir)
