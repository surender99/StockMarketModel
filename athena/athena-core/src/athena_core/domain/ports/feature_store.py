"""Feature store port — REQ-FEAT-STORE-001."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date
from typing import Any

import pandas as pd


@dataclass(frozen=True, slots=True)
class FeatureCacheMiss:
    """Explicit cache miss — REQ-FEAT-STORE-001."""

    reason: str


@dataclass(frozen=True, slots=True)
class FeatureCacheHit:
    """Cached feature values aligned to stored dates."""

    data: pd.DataFrame
    path: str


FeatureReadResult = FeatureCacheHit | FeatureCacheMiss


class FeatureStorePort(ABC):
    """Get/put computed features keyed by symbol, feature_id, params, data_version."""

    @abstractmethod
    def get(
        self,
        symbol: str,
        feature_id: str,
        params: dict[str, Any],
        data_version: str,
        start: date | None = None,
        end: date | None = None,
    ) -> FeatureReadResult:
        """Read cached feature or return explicit miss."""

    @abstractmethod
    def put(
        self,
        symbol: str,
        feature_id: str,
        params: dict[str, Any],
        data_version: str,
        data: pd.DataFrame,
    ) -> str:
        """Persist feature values; return storage path."""
