"""Tests for feature store — REQ-FEAT-STORE-001."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import pandas as pd
import pytest

from athena_core.application.config import FeatureStoreConfig
from athena_core.application.feature_service import FeatureService
from athena_core.domain.ports.feature_store import FeatureCacheMiss
from athena_core.infrastructure.parquet_feature_store import ParquetFeatureStore, params_hash
from athena_core.infrastructure.parquet_ohlcv_store import ParquetOHLCVStore


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


def test_params_hash_isolation() -> None:
    h1 = params_hash({"period": 21})
    h2 = params_hash({"period": 50})
    assert h1 != h2


def test_put_get_round_trip(tmp_path: Path) -> None:
    store = ParquetFeatureStore(tmp_path)
    df = pd.DataFrame({"date": [date(2024, 1, 2)], "ema_21": [100.5]})
    path = store.put("RELIANCE.NS", "ema", {"period": 21}, "v1", df)
    from athena_core.domain.ports.feature_store import FeatureCacheHit

    hit = store.get("RELIANCE.NS", "ema", {"period": 21}, "v1")
    assert isinstance(hit, FeatureCacheHit)
    assert hit.data["ema_21"].iloc[0] == pytest.approx(100.5)
    assert Path(path).is_dir()


def test_date_range_slice(tmp_path: Path) -> None:
    store = ParquetFeatureStore(tmp_path)
    df = pd.DataFrame(
        {
            "date": [date(2024, 1, 2), date(2024, 1, 3), date(2024, 1, 4)],
            "ema_21": [1.0, 2.0, 3.0],
        }
    )
    store.put("X.NS", "ema", {"period": 21}, "v1", df)
    from athena_core.domain.ports.feature_store import FeatureCacheHit

    hit = store.get(
        "X.NS", "ema", {"period": 21}, "v1", start=date(2024, 1, 3), end=date(2024, 1, 3)
    )
    assert isinstance(hit, FeatureCacheHit)
    assert len(hit.data) == 1
    assert hit.data["date"].iloc[0] == date(2024, 1, 3)


def test_missing_cache_returns_miss(tmp_path: Path) -> None:
    store = ParquetFeatureStore(tmp_path)
    result = store.get("MISSING.NS", "ema", {"period": 21}, "v1")
    assert isinstance(result, FeatureCacheMiss)


def test_version_mismatch_triggers_miss(tmp_path: Path) -> None:
    store = ParquetFeatureStore(tmp_path)
    df = pd.DataFrame({"date": [date(2024, 1, 2)], "ema_21": [1.0]})
    store.put("X.NS", "ema", {"period": 21}, "v1", df)
    result = store.get("X.NS", "ema", {"period": 21}, "v2")
    assert isinstance(result, FeatureCacheMiss)
    assert result.reason == "data_version_mismatch"


def test_metadata_sidecar(tmp_path: Path) -> None:
    store = ParquetFeatureStore(tmp_path)
    df = pd.DataFrame({"date": [date(2024, 1, 2)], "ema_21": [1.0]})
    store.put("X.NS", "ema", {"period": 21}, "v1", df)
    phash = params_hash({"period": 21})
    meta_path = tmp_path / "X.NS" / "ema" / phash / "metadata.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    assert meta["feature_id"] == "ema"
    assert meta["params"] == {"period": 21}
    assert meta["data_version"] == "v1"
    assert "created_at" in meta


def test_feature_service_cache_hit_skips_recompute(tmp_path: Path, ohlcv_sample: pd.DataFrame) -> None:
    ohlcv_store = ParquetOHLCVStore(tmp_path / "ohlcv")
    feature_store = ParquetFeatureStore(tmp_path / "features")
    ohlcv_store.write("TEST.NS", ohlcv_sample)
    service = FeatureService(feature_store, ohlcv_store, FeatureStoreConfig(data_version="v1"))

    first = service.get_feature("TEST.NS", "ema", {"period": 9})
    assert service.compute_count == 1
    second = service.get_feature("TEST.NS", "ema", {"period": 9})
    assert service.compute_count == 1
    pd.testing.assert_frame_equal(first, second)


def test_different_params_separate_paths(tmp_path: Path, ohlcv_sample: pd.DataFrame) -> None:
    ohlcv_store = ParquetOHLCVStore(tmp_path / "ohlcv")
    feature_store = ParquetFeatureStore(tmp_path / "features")
    ohlcv_store.write("TEST.NS", ohlcv_sample)
    service = FeatureService(feature_store, ohlcv_store, FeatureStoreConfig())

    service.get_feature("TEST.NS", "ema", {"period": 9})
    service.get_feature("TEST.NS", "ema", {"period": 21})
    assert service.compute_count == 2
    h9 = params_hash({"period": 9})
    h21 = params_hash({"period": 21})
    assert (tmp_path / "features" / "TEST.NS" / "ema" / h9).exists()
    assert (tmp_path / "features" / "TEST.NS" / "ema" / h21).exists()
