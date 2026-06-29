"""Parquet OHLCV store — REQ-DATA-INGEST-001, REQ-DATA-VERSION-001."""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

import pandas as pd

from athena_core.application.errors import ImmutabilityViolationError
from athena_core.domain.data.versioning import compute_content_version
from athena_core.domain.ports.ohlcv_repository import OHLCVRepositoryPort
from athena_core.infrastructure.yfinance_client import validate_ohlcv

_SCHEMA = ["date", "open", "high", "low", "close", "volume", "symbol"]


class ParquetOHLCVStore(OHLCVRepositoryPort):
    """Local Parquet-backed OHLCV repository with atomic writes and metadata sidecar."""

    def __init__(
        self,
        base_path: Path | str,
        *,
        data_version: str = "v1",
        immutable_snapshots: bool = False,
    ) -> None:
        self._base = Path(base_path)
        self._base.mkdir(parents=True, exist_ok=True)
        self._data_version = data_version
        self._immutable = immutable_snapshots

    def _path(self, symbol: str) -> Path:
        safe = symbol.replace("/", "_")
        return self._base / safe / "bars.parquet"

    def _metadata_path(self, symbol: str) -> Path:
        return self._path(symbol).with_name("metadata.json")

    @staticmethod
    def _checksum(df: pd.DataFrame) -> str:
        payload = df[_SCHEMA].sort_values("date").to_csv(index=False).encode("utf-8")
        return hashlib.sha256(payload).hexdigest()

    def exists(self, symbol: str) -> bool:
        return self._path(symbol).is_file()

    def read_metadata(self, symbol: str) -> dict[str, Any] | None:
        path = self._metadata_path(symbol)
        if not path.is_file():
            return None
        data: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
        return data

    def read(
        self,
        symbol: str,
        start: date | None = None,
        end: date | None = None,
    ) -> pd.DataFrame:
        path = self._path(symbol)
        if not path.is_file():
            return pd.DataFrame(columns=_SCHEMA)
        df = pd.read_parquet(path)
        if start is not None:
            df = df[df["date"] >= start]
        if end is not None:
            df = df[df["date"] <= end]
        return df.reset_index(drop=True)

    def write(
        self,
        symbol: str,
        df: pd.DataFrame,
        *,
        source: str | None = None,
        ingestion_timestamp: datetime | None = None,
        data_version: str | None = None,
    ) -> int:
        validate_ohlcv(df)
        out = df[_SCHEMA].copy()
        path = self._path(symbol)
        path.parent.mkdir(parents=True, exist_ok=True)
        version = data_version or self._data_version
        if self._immutable and path.is_file():
            msg = "immutable snapshot already exists"
            start = out["date"].min() if not out.empty else date.today()
            end = out["date"].max() if not out.empty else date.today()
            raise ImmutabilityViolationError(symbol, start, end, msg)
        if path.is_file():
            existing = pd.read_parquet(path)
            merged = pd.concat([existing, out], ignore_index=True)
            merged = merged.drop_duplicates(subset=["date"], keep="last")
            merged = merged.sort_values("date").reset_index(drop=True)
            out = merged
        fd, tmp_name = tempfile.mkstemp(suffix=".parquet", dir=path.parent)
        os.close(fd)
        tmp = Path(tmp_name)
        try:
            out.to_parquet(tmp, compression="snappy", index=False)
            tmp.replace(path)
        finally:
            if tmp.exists():
                tmp.unlink(missing_ok=True)

        ts = ingestion_timestamp or datetime.now(UTC)
        checksum = self._checksum(out)
        meta = {
            "symbol": symbol,
            "row_count": len(out),
            "checksum_sha256": checksum,
            "data_version": version,
            "content_version": compute_content_version(checksum, version),
            "source": source or "unknown",
            "ingestion_timestamp": ts.isoformat(),
            "immutable": self._immutable,
        }
        self._metadata_path(symbol).write_text(json.dumps(meta, indent=2), encoding="utf-8")
        return len(out)
