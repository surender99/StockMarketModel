"""Parquet OHLCV store — REQ-DATA-INGEST-001."""

from __future__ import annotations

import os
import tempfile
from datetime import date
from pathlib import Path

import pandas as pd

from athena_core.domain.ports.ohlcv_repository import OHLCVRepositoryPort
from athena_core.infrastructure.yfinance_client import validate_ohlcv

_SCHEMA = ["date", "open", "high", "low", "close", "volume", "symbol"]


class ParquetOHLCVStore(OHLCVRepositoryPort):
    """Local Parquet-backed OHLCV repository with atomic writes."""

    def __init__(self, base_path: Path | str) -> None:
        self._base = Path(base_path)
        self._base.mkdir(parents=True, exist_ok=True)

    def _path(self, symbol: str) -> Path:
        safe = symbol.replace("/", "_")
        return self._base / safe / "bars.parquet"

    def exists(self, symbol: str) -> bool:
        return self._path(symbol).is_file()

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

    def write(self, symbol: str, df: pd.DataFrame) -> int:
        validate_ohlcv(df)
        out = df[_SCHEMA].copy()
        path = self._path(symbol)
        path.parent.mkdir(parents=True, exist_ok=True)
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
        return len(out)
