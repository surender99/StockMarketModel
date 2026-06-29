"""Statistics analysis context — ATH-REL-009 §5.1."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import pandas as pd

from athena_core.domain.backtest import TradeRecord


@dataclass
class StatisticsContext:
    """Input bundle for statistics and analytics runs — FR-012."""

    equity_curve: pd.DataFrame
    trades: list[TradeRecord] = field(default_factory=list)
    initial_capital: float = 100_000.0
    trading_days_per_year: int = 252
    benchmark_returns: pd.Series | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def daily_returns(self) -> pd.Series:
        if self.equity_curve.empty or "equity" not in self.equity_curve.columns:
            return pd.Series(dtype=float)
        return self.equity_curve["equity"].astype(float).pct_change().dropna()
