"""Indicator architecture APS tests — PHASE 3 Architecture expansion."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from athena_core.domain.features.indicator_plugins import register_builtin_indicators
from athena_core.domain.indicators.catalog import (
    INDICATOR_CATALOG,
    list_mvp_indicators,
    lookup_by_aps_id,
)
from athena_core.domain.indicators.engine import IndicatorEngine
from athena_core.domain.indicators.metadata import build_metadata_store, lookup_metadata
from athena_core.domain.indicators.pipeline import IndicatorPipeline, PipelineStage
from athena_core.domain.indicators.price_transforms import (
    PRICE_TRANSFORMS,
    compute_hlc3,
    compute_hl2,
    compute_median_price,
    compute_ohlc4,
)
from athena_core.domain.plugins import PluginRegistry


def _registry() -> PluginRegistry:
    registry = PluginRegistry()
    register_builtin_indicators(registry)
    return registry


def _ohlcv(n: int = 100) -> pd.DataFrame:
    dates = pd.date_range("2020-01-01", periods=n, freq="B")
    close = pd.Series(100 + np.arange(n) * 0.1, index=dates)
    return pd.DataFrame(
        {
            "date": dates.date,
            "open": close.values,
            "high": close.values + 1,
            "low": close.values - 1,
            "close": close.values,
            "volume": 1000 + np.arange(n),
        }
    )


def test_price_transforms_hlc3_hl2_ohlc4() -> None:
    """APS-PRICE-HLC3/HL2/OHLC4-001 — vectorized price transforms."""
    df = _ohlcv()
    hlc3 = compute_hlc3(df)
    hl2 = compute_hl2(df)
    ohlc4 = compute_ohlc4(df)
    assert len(hlc3) == len(df)
    assert hlc3.iloc[-1] == pytest.approx((df["high"].iloc[-1] + df["low"].iloc[-1] + df["close"].iloc[-1]) / 3)
    assert hl2.iloc[-1] == pytest.approx((df["high"].iloc[-1] + df["low"].iloc[-1]) / 2)
    assert ohlc4.iloc[-1] == pytest.approx(
        (df["open"].iloc[-1] + df["high"].iloc[-1] + df["low"].iloc[-1] + df["close"].iloc[-1]) / 4
    )
    assert compute_median_price(df).equals(hl2)


def test_price_transform_registry_covers_mvp() -> None:
    """APS-PRICE-*-001 — transform registry matches core MVP price transforms."""
    mvp_price = [
        e
        for e in INDICATOR_CATALOG
        if e.category == "Price-Transformations" and e.status == "MVP" and e.plugin_id in PRICE_TRANSFORMS
    ]
    assert len(mvp_price) == 4
    assert set(PRICE_TRANSFORMS) == {e.plugin_id for e in mvp_price}


def test_indicator_pipeline_chains_stages() -> None:
    """APS-IND-PIPELINE-001 — pipeline runs EMA then RSI stages."""
    engine = IndicatorEngine(_registry())
    pipeline = IndicatorPipeline(
        engine,
        [
            PipelineStage("ema20", "ema", {"period": 20}),
            PipelineStage("rsi14", "rsi", {"period": 14}),
        ],
    )
    outputs = pipeline.run(_ohlcv(200))
    assert set(outputs) == {"ema20", "rsi14"}
    assert len(outputs["ema20"]) == 200
    assert len(outputs["rsi14"]) == 200


def test_metadata_store_covers_catalog() -> None:
    """APS-IND-METADATA-001 — metadata store has entry per catalog plugin."""
    store = build_metadata_store()
    assert len(store) == len(INDICATOR_CATALOG)
    assert lookup_metadata("ema") is not None
    assert lookup_metadata("ema").entry.aps_id == "APS-IND-EMA-001"


def test_expanded_catalog_has_deferred_entries() -> None:
    """APS-IND-REGISTRY-001 — expanded architecture catalogs deferred indicators."""
    assert len(INDICATOR_CATALOG) >= 70
    deferred = [e for e in INDICATOR_CATALOG if e.status == "Deferred"]
    assert len(deferred) >= 40
    assert lookup_by_aps_id("APS-IND-ICHIMOKU-001") is not None


def test_mvp_indicator_count_includes_price_transforms() -> None:
    """APS-IND-REGISTRY-001 — MVP count includes builtins + price transforms + deferred batch."""
    mvp = list_mvp_indicators()
    assert len(mvp) == 23
