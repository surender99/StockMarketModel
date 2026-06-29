"""Feature orchestration — REQ-FEAT-STORE-001, ATH-REL-003."""

from __future__ import annotations

from datetime import date
from typing import Any

import pandas as pd
import structlog

from athena_core.application.config import FeatureStoreConfig
from athena_core.domain.features.caching import FeatureCachePolicy
from athena_core.domain.features.indicator_plugins import resolve_indicator
from athena_core.domain.ports.feature_store import FeatureCacheMiss, FeatureStorePort
from athena_core.domain.ports.ohlcv_repository import OHLCVRepositoryPort
from athena_core.domain.plugins import PluginRegistry

log = structlog.get_logger(__name__)


class FeatureService:
    """Compute-on-miss / read-on-hit feature access — REQ-FEAT-STORE-001."""

    def __init__(
        self,
        feature_store: FeatureStorePort,
        ohlcv_repo: OHLCVRepositoryPort,
        config: FeatureStoreConfig,
        *,
        plugin_registry: PluginRegistry | None = None,
    ) -> None:
        self._store = feature_store
        self._ohlcv = ohlcv_repo
        self._config = config
        self._registry = plugin_registry
        self._compute_count = 0

    @property
    def compute_count(self) -> int:
        """Number of indicator computations performed (for cache-hit tests)."""
        return self._compute_count

    def get_feature(
        self,
        symbol: str,
        feature_id: str,
        params: dict[str, Any],
        start: date | None = None,
        end: date | None = None,
    ) -> pd.DataFrame:
        policy = self._config.cache_policy
        cached = None
        if policy != FeatureCachePolicy.FORCE_RECOMPUTE:
            cached = self._store.get(
                symbol,
                feature_id,
                params,
                self._config.data_version,
                start=start,
                end=end,
            )
            if not isinstance(cached, FeatureCacheMiss):
                log.info("feature.cache_hit", symbol=symbol, feature_id=feature_id, params=params)
                return cached.data

        if policy == FeatureCachePolicy.CACHE_ONLY:
            reason = cached.reason if isinstance(cached, FeatureCacheMiss) else "cache_only_miss"
            msg = f"Feature cache miss under cache_only policy: {symbol}/{feature_id} ({reason})"
            raise ValueError(msg)

        log.info("feature.cache_miss", symbol=symbol, feature_id=feature_id, params=params)
        ohlcv = self._ohlcv.read(symbol, start=start, end=end)
        if ohlcv.empty:
            msg = f"No OHLCV data for {symbol}"
            raise ValueError(msg)

        if self._registry is None:
            msg = "PluginRegistry is required for indicator resolution"
            raise ValueError(msg)

        compute_fn = resolve_indicator(self._registry, feature_id)
        self._compute_count += 1
        values = compute_fn(ohlcv, params)
        out = self._frame_output(feature_id, ohlcv, values, params)

        self._store.put(symbol, feature_id, params, self._config.data_version, out)
        result = self._store.get(
            symbol,
            feature_id,
            params,
            self._config.data_version,
            start=start,
            end=end,
        )
        assert not isinstance(result, FeatureCacheMiss)
        return result.data

    @staticmethod
    def _frame_output(
        feature_id: str,
        ohlcv: pd.DataFrame,
        values: pd.Series | pd.DataFrame,
        params: dict[str, Any],
    ) -> pd.DataFrame:
        if isinstance(values, pd.Series):
            col = f"{feature_id}_{params['period']}" if "period" in params else feature_id
            return pd.DataFrame({"date": ohlcv["date"].values, col: values.values})
        if feature_id == "pattern":
            return values
        return pd.concat(
            [ohlcv[["date"]].reset_index(drop=True), values.reset_index(drop=True)],
            axis=1,
        )
