"""Feature engineering framework tests — ATH-REL-003."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pandas as pd
import pytest

from athena_core.application.config import FeatureStoreConfig
from athena_core.application.feature_pipeline import FeaturePipeline, FeatureRequest
from athena_core.application.feature_service import FeatureService
from athena_core.domain.features.caching import FeatureCachePolicy
from athena_core.domain.features.indicator_plugins import register_builtin_indicators
from athena_core.domain.plugins import PluginRegistry, PluginType
from athena_core.infrastructure.parquet_feature_store import ParquetFeatureStore
from athena_core.infrastructure.parquet_ohlcv_store import ParquetOHLCVStore


def _registry() -> PluginRegistry:
    registry = PluginRegistry()
    register_builtin_indicators(registry)
    return registry


def _service(tmp_path: Path, ohlcv: pd.DataFrame, *, cache_policy: FeatureCachePolicy | None = None) -> FeatureService:
    ohlcv_store = ParquetOHLCVStore(tmp_path / "ohlcv")
    feature_store = ParquetFeatureStore(tmp_path / "features")
    ohlcv_store.write("TEST.NS", ohlcv)
    config = FeatureStoreConfig(data_version="v1")
    if cache_policy is not None:
        config = FeatureStoreConfig(data_version="v1", cache_policy=cache_policy)
    return FeatureService(feature_store, ohlcv_store, config, plugin_registry=_registry())


@pytest.fixture
def ohlcv_sample() -> pd.DataFrame:
    dates = pd.date_range("2024-01-02", periods=30, freq="B")
    close = pd.Series(range(100, 130), index=dates)
    return pd.DataFrame(
        {
            "date": [d.date() for d in dates],
            "open": close.values,
            "high": close.values + 1,
            "low": close.values - 1,
            "close": close.values,
            "volume": 1000,
            "symbol": "TEST.NS",
        }
    )


def test_req_feat_registry_001_builtin_indicators_registered() -> None:
    """REQ-FEAT-REGISTRY-001 — built-in indicators resolve via PluginRegistry."""
    registry = _registry()
    indicators = registry.list(plugin_type=PluginType.INDICATOR, active_only=True)
    ids = {plugin.id for plugin in indicators}
    assert {"ema", "sma", "macd", "rsi", "stoch", "atr", "adx", "bollinger", "pattern"} <= ids


def test_req_feat_pipeline_001_multi_feature_run(tmp_path: Path, ohlcv_sample: pd.DataFrame) -> None:
    """REQ-FEAT-PIPELINE-001 — pipeline orchestrates multiple features."""
    service = _service(tmp_path, ohlcv_sample)
    pipeline = FeaturePipeline(
        service,
        [
            FeatureRequest("ema", {"period": 9}, alias="fast_ema"),
            FeatureRequest("atr", {"period": 14}, alias="atr_14"),
        ],
    )
    result = pipeline.run("TEST.NS")
    assert "fast_ema" in result.frames
    assert "atr_14" in result.frames
    assert "ema_9" in result.frames["fast_ema"].columns
    assert "atr_14" in result.frames["atr_14"].columns


def test_req_feat_cache_001_force_recompute(tmp_path: Path, ohlcv_sample: pd.DataFrame) -> None:
    """REQ-FEAT-CACHE-001 — force_recompute bypasses cache hits."""
    service = _service(tmp_path, ohlcv_sample, cache_policy=FeatureCachePolicy.COMPUTE_ON_MISS)
    service.get_feature("TEST.NS", "ema", {"period": 9})
    assert service.compute_count == 1
    service.get_feature("TEST.NS", "ema", {"period": 9})
    assert service.compute_count == 1

    service._config.cache_policy = FeatureCachePolicy.FORCE_RECOMPUTE  # noqa: SLF001
    service.get_feature("TEST.NS", "ema", {"period": 9})
    assert service.compute_count == 2


def test_req_feat_cache_001_cache_only_raises_on_miss(tmp_path: Path, ohlcv_sample: pd.DataFrame) -> None:
    """REQ-FEAT-CACHE-001 — cache_only raises on miss."""
    service = _service(tmp_path, ohlcv_sample, cache_policy=FeatureCachePolicy.CACHE_ONLY)
    with pytest.raises(ValueError, match="cache_only"):
        service.get_feature("TEST.NS", "ema", {"period": 9})


def test_req_ind_atr_001_feature_service_integration(tmp_path: Path, ohlcv_sample: pd.DataFrame) -> None:
    """REQ-IND-ATR-001 — ATR available through FeatureService."""
    service = _service(tmp_path, ohlcv_sample)
    frame = service.get_feature("TEST.NS", "atr", {"period": 14})
    assert "atr_14" in frame.columns
    assert len(frame) == len(ohlcv_sample)


def test_req_ind_adx_001_feature_service_integration(tmp_path: Path, ohlcv_sample: pd.DataFrame) -> None:
    """REQ-IND-ADX-001 — ADX available through FeatureService."""
    service = _service(tmp_path, ohlcv_sample)
    frame = service.get_feature("TEST.NS", "adx", {"period": 14})
    assert "adx_14" in frame.columns


def test_req_ind_bollinger_001_feature_service_integration(tmp_path: Path, ohlcv_sample: pd.DataFrame) -> None:
    """REQ-IND-BOLLINGER-001 — Bollinger available through FeatureService."""
    service = _service(tmp_path, ohlcv_sample)
    frame = service.get_feature("TEST.NS", "bollinger", {"period": 20, "std_dev": 2.0})
    assert {"bb_upper", "bb_middle", "bb_lower"} <= set(frame.columns)
