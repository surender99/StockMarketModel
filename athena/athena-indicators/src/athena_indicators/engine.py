"""Indicator engine adapter implementing IIndicatorEngine."""
from __future__ import annotations

from typing import Any

import pandas as pd

from athena_core.domain.indicators.engine import IndicatorEngine
from athena_core.domain.plugins import PluginRegistry


class IndicatorEngineFacade:
    """Delegates to athena-core IndicatorEngine — extraction path: ADR-0006."""

    def __init__(self, registry: PluginRegistry) -> None:
        self._engine = IndicatorEngine(registry)

    def compute(
        self,
        indicator_id: str,
        ohlcv: pd.DataFrame,
        params: dict[str, Any] | None = None,
    ) -> pd.Series | pd.DataFrame:
        return self._engine.compute(indicator_id, ohlcv, params)
