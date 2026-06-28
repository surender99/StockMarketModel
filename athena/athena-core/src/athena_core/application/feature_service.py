"""Feature orchestration — REQ-FEAT-STORE-001."""

from __future__ import annotations

from collections.abc import Callable
from datetime import date
from typing import Any

import pandas as pd
import structlog

from athena_core.application.config import FeatureStoreConfig
from athena_core.domain.indicators.ema import compute_ema_from_ohlcv
from athena_core.domain.indicators.macd import compute_macd_from_ohlcv
from athena_core.domain.indicators.rsi import compute_rsi_from_ohlcv
from athena_core.domain.indicators.sma import compute_sma_from_ohlcv
from athena_core.domain.indicators.stoch import compute_stoch_from_ohlcv
from athena_core.domain.patterns.series import compute_pattern_series
from athena_core.domain.ports.feature_store import FeatureCacheMiss, FeatureStorePort
from athena_core.domain.ports.ohlcv_repository import OHLCVRepositoryPort

log = structlog.get_logger(__name__)

IndicatorFn = Callable[[pd.DataFrame, dict[str, Any]], pd.Series | pd.DataFrame]

_INDICATOR_REGISTRY: dict[str, IndicatorFn] = {
    "ema": lambda df, params: compute_ema_from_ohlcv(
        df, int(params["period"]), price_column=params.get("price_column", "close")
    ),
    "sma": lambda df, params: compute_sma_from_ohlcv(
        df, int(params["period"]), price_column=params.get("price_column", "close")
    ),
    "macd": lambda df, params: compute_macd_from_ohlcv(
        df,
        fast=int(params.get("fast", 12)),
        slow=int(params.get("slow", 26)),
        signal=int(params.get("signal", 9)),
        price_column=params.get("price_column", "close"),
    ),
    "rsi": lambda df, params: compute_rsi_from_ohlcv(
        df, int(params.get("period", 14)), price_column=params.get("price_column", "close")
    ),
    "stoch": lambda df, params: compute_stoch_from_ohlcv(
        df,
        k_period=int(params.get("k_period", 14)),
        d_period=int(params.get("d_period", 3)),
    ),
    "pattern": lambda df, params: compute_pattern_series(df, str(params["pattern_id"])),
}


class FeatureService:
    """Compute-on-miss / read-on-hit feature access — REQ-FEAT-STORE-001."""

    def __init__(
        self,
        feature_store: FeatureStorePort,
        ohlcv_repo: OHLCVRepositoryPort,
        config: FeatureStoreConfig,
    ) -> None:
        self._store = feature_store
        self._ohlcv = ohlcv_repo
        self._config = config
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

        log.info("feature.cache_miss", symbol=symbol, feature_id=feature_id, params=params)
        ohlcv = self._ohlcv.read(symbol, start=start, end=end)
        if ohlcv.empty:
            msg = f"No OHLCV data for {symbol}"
            raise ValueError(msg)

        compute_fn = _INDICATOR_REGISTRY.get(feature_id)
        if compute_fn is None:
            msg = f"Unknown feature_id: {feature_id}"
            raise ValueError(msg)

        self._compute_count += 1
        values = compute_fn(ohlcv, params)
        if isinstance(values, pd.Series):
            col = f"{feature_id}_{params['period']}" if "period" in params else feature_id
            out = pd.DataFrame({"date": ohlcv["date"].values, col: values.values})
        elif feature_id == "pattern":
            out = values
        else:
            out = pd.concat(
                [ohlcv[["date"]].reset_index(drop=True), values.reset_index(drop=True)],
                axis=1,
            )

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
