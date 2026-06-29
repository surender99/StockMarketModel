"""Indicator execution engine — REQ-IND-ENGINE-001, ATH-REL-004 §02."""

from __future__ import annotations

from typing import Any

import pandas as pd

from athena_core.domain.features.indicator_plugins import IndicatorFn, resolve_indicator
from athena_core.domain.indicators.validation import validate_indicator_output
from athena_core.domain.plugins import PluginRegistry


class IndicatorEngine:
    """Execute indicators via PluginRegistry with output validation."""

    def __init__(self, registry: PluginRegistry) -> None:
        self._registry = registry

    def compute(
        self,
        indicator_id: str,
        ohlcv: pd.DataFrame,
        params: dict[str, Any] | None = None,
    ) -> pd.Series | pd.DataFrame:
        """Resolve and run an indicator, validating output alignment."""
        fn = resolve_indicator(self._registry, indicator_id)
        result = fn(ohlcv, params or {})
        validate_indicator_output(ohlcv, result, indicator_id=indicator_id)
        return result

    def compute_many(
        self,
        requests: list[tuple[str, dict[str, Any]]],
        ohlcv: pd.DataFrame,
    ) -> dict[str, pd.Series | pd.DataFrame]:
        """Run multiple indicators — REQ-IND-COMPOSITION-001."""
        outputs: dict[str, pd.Series | pd.DataFrame] = {}
        for indicator_id, params in requests:
            outputs[indicator_id] = self.compute(indicator_id, ohlcv, params)
        return outputs
