"""Indicator plugin registry — REQ-FEAT-REGISTRY-001, ATH-REL-003/004."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import pandas as pd

from athena_core.domain.indicators.adx import compute_adx_from_ohlcv
from athena_core.domain.indicators.atr import compute_atr_from_ohlcv
from athena_core.domain.indicators.bollinger import compute_bollinger_from_ohlcv
from athena_core.domain.indicators.cci import compute_cci_from_ohlcv
from athena_core.domain.indicators.cmf import compute_cmf_from_ohlcv
from athena_core.domain.indicators.ema import compute_ema_from_ohlcv
from athena_core.domain.indicators.macd import compute_macd_from_ohlcv
from athena_core.domain.indicators.mfi import compute_mfi_from_ohlcv
from athena_core.domain.indicators.obv import compute_obv_from_ohlcv
from athena_core.domain.indicators.roc import compute_roc_from_ohlcv
from athena_core.domain.indicators.rsi import compute_rsi_from_ohlcv
from athena_core.domain.indicators.sma import compute_sma_from_ohlcv
from athena_core.domain.indicators.stoch import compute_stoch_from_ohlcv
from athena_core.domain.indicators.willr import compute_willr_from_ohlcv
from athena_core.domain.indicators.wma import compute_wma_from_ohlcv
from athena_core.domain.patterns.series import compute_pattern_series
from athena_core.domain.plugins import Plugin, PluginMetadata, PluginRegistry, PluginType

IndicatorFn = Callable[[pd.DataFrame, dict[str, Any]], pd.Series | pd.DataFrame]


def build_indicator_plugin(
    indicator_id: str,
    *,
    version: str,
    name: str,
    description: str,
    configuration_schema: dict[str, Any],
    compute_fn: IndicatorFn,
) -> Plugin:
    """Wrap a vectorized indicator function as an AES-0202 plugin."""
    return Plugin(
        id=indicator_id,
        version=version,
        plugin_type=PluginType.INDICATOR,
        metadata=PluginMetadata(name=name, description=description),
        configuration_schema=configuration_schema,
        execute=compute_fn,
    )


def _builtin_indicator_specs() -> list[tuple[str, str, str, dict[str, Any], IndicatorFn]]:
    return [
        (
            "ema",
            "0.1.0",
            "Exponential Moving Average",
            {"period": {"type": "integer", "minimum": 1}, "price_column": {"type": "string"}},
            lambda df, params: compute_ema_from_ohlcv(
                df, int(params["period"]), price_column=params.get("price_column", "close")
            ),
        ),
        (
            "sma",
            "0.1.0",
            "Simple Moving Average",
            {"period": {"type": "integer", "minimum": 1}, "price_column": {"type": "string"}},
            lambda df, params: compute_sma_from_ohlcv(
                df, int(params["period"]), price_column=params.get("price_column", "close")
            ),
        ),
        (
            "macd",
            "0.1.0",
            "MACD",
            {
                "fast": {"type": "integer", "default": 12},
                "slow": {"type": "integer", "default": 26},
                "signal": {"type": "integer", "default": 9},
            },
            lambda df, params: compute_macd_from_ohlcv(
                df,
                fast=int(params.get("fast", 12)),
                slow=int(params.get("slow", 26)),
                signal=int(params.get("signal", 9)),
                price_column=params.get("price_column", "close"),
            ),
        ),
        (
            "rsi",
            "0.1.0",
            "Relative Strength Index",
            {"period": {"type": "integer", "default": 14}, "price_column": {"type": "string"}},
            lambda df, params: compute_rsi_from_ohlcv(
                df, int(params.get("period", 14)), price_column=params.get("price_column", "close")
            ),
        ),
        (
            "stoch",
            "0.1.0",
            "Stochastic Oscillator",
            {"k_period": {"type": "integer", "default": 14}, "d_period": {"type": "integer", "default": 3}},
            lambda df, params: compute_stoch_from_ohlcv(
                df,
                k_period=int(params.get("k_period", 14)),
                d_period=int(params.get("d_period", 3)),
            ),
        ),
        (
            "atr",
            "0.1.0",
            "Average True Range",
            {"period": {"type": "integer", "default": 14}},
            lambda df, params: compute_atr_from_ohlcv(df, int(params.get("period", 14))),
        ),
        (
            "adx",
            "0.1.0",
            "Average Directional Index",
            {"period": {"type": "integer", "default": 14}},
            lambda df, params: compute_adx_from_ohlcv(df, int(params.get("period", 14))),
        ),
        (
            "bollinger",
            "0.1.0",
            "Bollinger Bands",
            {
                "period": {"type": "integer", "default": 20},
                "std_dev": {"type": "number", "default": 2.0},
                "price_column": {"type": "string"},
            },
            lambda df, params: compute_bollinger_from_ohlcv(
                df,
                period=int(params.get("period", 20)),
                std_dev=float(params.get("std_dev", 2.0)),
                price_column=params.get("price_column", "close"),
            ),
        ),
        (
            "wma",
            "0.1.0",
            "Weighted Moving Average",
            {"period": {"type": "integer", "minimum": 1}, "price_column": {"type": "string"}},
            lambda df, params: compute_wma_from_ohlcv(
                df, int(params["period"]), price_column=params.get("price_column", "close")
            ),
        ),
        (
            "roc",
            "0.1.0",
            "Rate of Change",
            {"period": {"type": "integer", "default": 12}, "price_column": {"type": "string"}},
            lambda df, params: compute_roc_from_ohlcv(
                df, int(params.get("period", 12)), price_column=params.get("price_column", "close")
            ),
        ),
        (
            "obv",
            "0.1.0",
            "On-Balance Volume",
            {},
            lambda df, params: compute_obv_from_ohlcv(df),
        ),
        (
            "cmf",
            "0.1.0",
            "Chaikin Money Flow",
            {"period": {"type": "integer", "default": 20}},
            lambda df, params: compute_cmf_from_ohlcv(df, int(params.get("period", 20))),
        ),
        (
            "mfi",
            "0.1.0",
            "Money Flow Index",
            {"period": {"type": "integer", "default": 14}},
            lambda df, params: compute_mfi_from_ohlcv(df, int(params.get("period", 14))),
        ),
        (
            "cci",
            "0.1.0",
            "Commodity Channel Index",
            {"period": {"type": "integer", "default": 20}},
            lambda df, params: compute_cci_from_ohlcv(df, int(params.get("period", 20))),
        ),
        (
            "willr",
            "0.1.0",
            "Williams %R",
            {"period": {"type": "integer", "default": 14}},
            lambda df, params: compute_willr_from_ohlcv(df, int(params.get("period", 14))),
        ),
        (
            "pattern",
            "0.1.0",
            "Pattern Recognition Series",
            {"pattern_id": {"type": "string"}},
            lambda df, params: compute_pattern_series(df, str(params["pattern_id"])),
        ),
    ]


def register_builtin_indicators(registry: PluginRegistry) -> int:
    """Register all built-in indicators; returns count added — REQ-FEAT-REGISTRY-001."""
    plugins = [
        build_indicator_plugin(
            indicator_id,
            version=version,
            name=name,
            description=name,
            configuration_schema=schema,
            compute_fn=compute_fn,
        )
        for indicator_id, version, name, schema, compute_fn in _builtin_indicator_specs()
    ]
    return registry.discover(plugins)


def resolve_indicator(registry: PluginRegistry, feature_id: str) -> IndicatorFn:
    """Resolve an active indicator plugin execute callable."""
    plugin = registry.get(feature_id)
    if plugin.plugin_type != PluginType.INDICATOR:
        msg = f"plugin is not an indicator: {feature_id}"
        raise ValueError(msg)
    if plugin.execute is None:
        msg = f"indicator plugin has no execute callable: {feature_id}"
        raise ValueError(msg)
    return plugin.execute  # type: ignore[return-value]
