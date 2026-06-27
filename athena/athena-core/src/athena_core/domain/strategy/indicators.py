"""Indicator type registry — REQ-STRAT-CONFIG-001."""

from __future__ import annotations

from typing import Any

from athena_core.domain.strategy.config import IndicatorSpec

INDICATOR_TYPES: frozenset[str] = frozenset({"ema", "sma"})

_REQUIRED_PARAMS: dict[str, tuple[str, ...]] = {
    "ema": ("period",),
    "sma": ("period",),
}


def validate_indicator_specs(specs: list[IndicatorSpec]) -> None:
    """Ensure indicator types and params are registered and valid."""
    for spec in specs:
        if spec.type not in INDICATOR_TYPES:
            msg = f"unknown indicator type '{spec.type}' for id '{spec.id}'"
            raise ValueError(msg)
        required = _REQUIRED_PARAMS[spec.type]
        for key in required:
            if key not in spec.params:
                msg = f"indicator '{spec.id}' missing required param '{key}'"
                raise ValueError(msg)
        period = int(spec.params["period"])
        if period < 1:
            msg = f"indicator '{spec.id}' period must be >= 1"
            raise ValueError(msg)


def indicator_feature_id(indicator_type: str) -> str:
    """Map strategy indicator type to feature store feature_id."""
    if indicator_type not in INDICATOR_TYPES:
        msg = f"unsupported indicator type: {indicator_type}"
        raise ValueError(msg)
    return indicator_type


def indicator_column_name(spec: IndicatorSpec) -> str:
    """Column name for indicator values in feature frames."""
    period = spec.params["period"]
    return f"{spec.type}_{period}"
