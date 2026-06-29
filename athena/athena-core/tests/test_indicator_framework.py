"""Indicator framework tests — ATH-REL-004."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from athena_core.application.config import FeatureStoreConfig
from athena_core.application.feature_service import FeatureService
from athena_core.domain.features.indicator_plugins import register_builtin_indicators
from athena_core.domain.indicators.engine import IndicatorEngine
from athena_core.domain.indicators.validation import validate_indicator_output
from athena_core.domain.plugins import PluginRegistry, PluginType
from athena_core.infrastructure.parquet_feature_store import ParquetFeatureStore
from athena_core.infrastructure.parquet_ohlcv_store import ParquetOHLCVStore


def _registry() -> PluginRegistry:
    registry = PluginRegistry()
    register_builtin_indicators(registry)
    return registry


@pytest.fixture
def ohlcv_df() -> pd.DataFrame:
    dates = pd.date_range("2020-01-01", periods=60, freq="B")
    close = pd.Series(100 + np.arange(60) * 0.5, index=dates)
    return pd.DataFrame(
        {
            "date": dates.date,
            "open": close.values,
            "high": close.values + 2,
            "low": close.values - 2,
            "close": close.values,
            "volume": 1000 + np.arange(60) * 10,
        }
    )


def test_req_ind_engine_001_indicator_engine_compute(ohlcv_df: pd.DataFrame) -> None:
    """REQ-IND-ENGINE-001 — IndicatorEngine resolves and runs indicators."""
    engine = IndicatorEngine(_registry())
    result = engine.compute("roc", ohlcv_df, {"period": 12})
    assert len(result) == len(ohlcv_df)


def test_req_ind_engine_001_compute_many(ohlcv_df: pd.DataFrame) -> None:
    """REQ-IND-COMPOSITION-001 — compute_many runs multiple indicators."""
    engine = IndicatorEngine(_registry())
    outputs = engine.compute_many(
        [("obv", {}), ("cmf", {"period": 20})],
        ohlcv_df,
    )
    assert set(outputs.keys()) == {"obv", "cmf"}
    assert len(outputs["obv"]) == len(ohlcv_df)


def test_req_ind_validation_001_length_mismatch_raises(ohlcv_df: pd.DataFrame) -> None:
    """REQ-IND-VALIDATION-001 — output length must match OHLCV."""
    bad = pd.Series([1.0, 2.0])
    with pytest.raises(ValueError, match="output length"):
        validate_indicator_output(ohlcv_df, bad, indicator_id="test")


def test_req_ind_registry_004_new_indicators_registered() -> None:
    """ATH-REL-004 — expanded indicator catalog in registry."""
    registry = _registry()
    ids = {p.id for p in registry.list(plugin_type=PluginType.INDICATOR, active_only=True)}
    assert {"wma", "roc", "obv", "cmf", "mfi", "cci", "willr"} <= ids


def test_req_ind_obv_001_positive_cumulative(ohlcv_df: pd.DataFrame) -> None:
    """REQ-IND-OBV-001 — OBV via IndicatorEngine."""
    engine = IndicatorEngine(_registry())
    result = engine.compute("obv", ohlcv_df)
    assert result.notna().all()


def test_req_ind_mfi_001_bounded_range(ohlcv_df: pd.DataFrame) -> None:
    """REQ-IND-MFI-001 — MFI bounded 0-100 after warmup."""
    engine = IndicatorEngine(_registry())
    result = engine.compute("mfi", ohlcv_df, {"period": 14})
    valid = result.dropna()
    assert (valid >= 0).all() and (valid <= 100).all()


def test_req_ind_willr_001_feature_service(tmp_path: Path, ohlcv_df: pd.DataFrame) -> None:
    """REQ-IND-WILLR-001 — Williams %R via FeatureService."""
    ohlcv_store = ParquetOHLCVStore(tmp_path / "ohlcv")
    feature_store = ParquetFeatureStore(tmp_path / "features")
    ohlcv_store.write("TEST.NS", ohlcv_df.assign(symbol="TEST.NS"))
    service = FeatureService(
        feature_store,
        ohlcv_store,
        FeatureStoreConfig(data_version="v1"),
        plugin_registry=_registry(),
    )
    frame = service.get_feature("TEST.NS", "willr", {"period": 14})
    assert len(frame) == len(ohlcv_df)
