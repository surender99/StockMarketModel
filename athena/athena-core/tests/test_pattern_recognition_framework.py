"""Pattern recognition framework tests — ATH-REL-005."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from athena_core.application.config import FeatureStoreConfig
from athena_core.application.feature_pipeline import FeaturePipeline, FeatureRequest
from athena_core.application.feature_service import FeatureService
from athena_core.domain.features.indicator_plugins import register_builtin_indicators
from athena_core.domain.patterns import PatternDetector, register_builtin_patterns
from athena_core.domain.patterns.pattern_plugins import pattern_to_feature_frame, resolve_pattern
from athena_core.domain.plugins import PluginRegistry, PluginType
from athena_core.infrastructure.parquet_feature_store import ParquetFeatureStore
from athena_core.infrastructure.parquet_ohlcv_store import ParquetOHLCVStore


def _ohlcv(rows: list[dict[str, float]]) -> pd.DataFrame:
    dates = pd.date_range("2024-01-02", periods=len(rows), freq="B").date
    return pd.DataFrame(
        {
            "date": dates,
            "open": [r["open"] for r in rows],
            "high": [r["high"] for r in rows],
            "low": [r["low"] for r in rows],
            "close": [r["close"] for r in rows],
            "volume": [r.get("volume", 1000) for r in rows],
        }
    )


def _full_registry() -> PluginRegistry:
    registry = PluginRegistry()
    register_builtin_indicators(registry)
    register_builtin_patterns(registry)
    return registry


def test_req_pat_registry_001_builtin_patterns_registered() -> None:
    """REQ-PAT-REGISTRY-001 — built-in patterns resolve via PluginRegistry."""
    registry = PluginRegistry()
    register_builtin_patterns(registry)
    patterns = registry.list(plugin_type=PluginType.PATTERN, active_only=True)
    ids = {p.id for p in patterns}
    assert {"bullish_engulfing", "bearish_engulfing", "bull_flag", "bear_flag", "double_top"} <= ids


def test_bearish_engulfing_detection() -> None:
    df = _ohlcv(
        [
            {"open": 100, "high": 115, "low": 99, "close": 110},
            {"open": 116, "high": 117, "low": 95, "close": 96},
        ]
    )
    events = PatternDetector().detect(df, "bearish_engulfing")
    assert len(events) == 1
    assert events[0].pattern_id == "bearish_engulfing"


def test_shooting_star_detection() -> None:
    df = _ohlcv([{"open": 100, "high": 120, "low": 100, "close": 100.2}])
    events = PatternDetector().detect(df, "shooting_star")
    assert len(events) == 1


def test_evening_star_detection() -> None:
    df = _ohlcv(
        [
            {"open": 100, "high": 115, "low": 99, "close": 114},
            {"open": 115, "high": 116, "low": 114, "close": 115},
            {"open": 114, "high": 115, "low": 90, "close": 95},
        ]
    )
    events = PatternDetector().detect(df, "evening_star")
    assert len(events) == 1


def test_bear_flag_detection() -> None:
    rows: list[dict[str, float]] = []
    price = 120.0
    for _ in range(5):
        rows.append({"open": price, "high": price + 1, "low": price - 3, "close": price - 2})
        price -= 2
    for i in range(4):
        rows.append(
            {
                "open": price,
                "high": price + 0.5,
                "low": price - 0.5,
                "close": price - 0.1 * (i % 2),
            }
        )
    events = PatternDetector().detect(_ohlcv(rows), "bear_flag")
    assert len(events) >= 1


def test_pattern_plugin_resolve_and_detect() -> None:
    """REQ-PAT-REGISTRY-001 — resolve_pattern returns working detector."""
    registry = PluginRegistry()
    register_builtin_patterns(registry)
    df = _ohlcv([{"open": 100, "high": 101, "low": 99, "close": 100.05}])
    detect_fn = resolve_pattern(registry, "doji")
    assert len(detect_fn(df)) == 1


def test_pattern_feature_pipeline_integration(tmp_path: Path) -> None:
    """ATH-REL-005 — pattern features via feature pipeline."""
    dates = pd.date_range("2024-01-02", periods=10, freq="B")
    close = pd.Series(range(100, 110), index=dates)
    ohlcv = pd.DataFrame(
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
    ohlcv_store = ParquetOHLCVStore(tmp_path / "ohlcv")
    feature_store = ParquetFeatureStore(tmp_path / "features")
    ohlcv_store.write("TEST.NS", ohlcv)
    service = FeatureService(
        feature_store,
        ohlcv_store,
        FeatureStoreConfig(data_version="v1"),
        plugin_registry=_full_registry(),
    )
    pipeline = FeaturePipeline(
        service,
        [FeatureRequest("pattern", {"pattern_id": "doji"}, alias="doji_signal")],
    )
    result = pipeline.run("TEST.NS")
    assert "doji_signal" in result.frames
    assert "signal" in result.frames["doji_signal"].columns


def test_pattern_to_feature_frame_via_registry() -> None:
    df = _ohlcv([{"open": 100, "high": 101, "low": 99, "close": 100.05}])
    registry = PluginRegistry()
    register_builtin_patterns(registry)
    frame = pattern_to_feature_frame(df, "doji", registry=registry)
    assert "signal" in frame.columns
