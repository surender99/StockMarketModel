"""FeatureService adapter for backtest engine — REQ-BT-ENGINE-001."""

from __future__ import annotations

from datetime import date
from typing import Any

import pandas as pd

from athena_core.application.backtest_engine import FeatureProviderPort
from athena_core.application.feature_service import FeatureService


class FeatureServiceProvider(FeatureProviderPort):
    """Bridge FeatureService to BacktestEngine."""

    def __init__(self, feature_service: FeatureService) -> None:
        self._service = feature_service

    def get_indicator_frame(
        self,
        symbol: str,
        indicator_type: str,
        params: dict[str, Any],
        start: date | None,
        end: date | None,
    ) -> pd.DataFrame:
        return self._service.get_feature(symbol, indicator_type, params, start=start, end=end)
