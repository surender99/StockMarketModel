"""Domain engine interface contracts — ADR-0006 bounded contexts."""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

import pandas as pd


@runtime_checkable
class IIndicatorEngine(Protocol):
    """Compute technical indicators from OHLCV frames."""

    def compute(
        self,
        indicator_id: str,
        ohlcv: pd.DataFrame,
        params: dict[str, Any] | None = None,
    ) -> pd.Series | pd.DataFrame: ...


@runtime_checkable
class IPatternEngine(Protocol):
    """Detect chart and candlestick patterns."""

    def detect(self, ohlcv: pd.DataFrame) -> list[Any]: ...


@runtime_checkable
class IStrategyEngine(Protocol):
    """Evaluate trading strategies and generate signals."""

    def validate(self, strategy: Any) -> None: ...

    def evaluate_entry(self, strategy: Any, frame: pd.DataFrame, index: int) -> Any | None: ...


@runtime_checkable
class IRiskEngine(Protocol):
    """Analyze portfolio and equity-curve risk."""

    def analyze(self, equity_curve: pd.DataFrame, **kwargs: Any) -> Any: ...


@runtime_checkable
class IPortfolioEngine(Protocol):
    """Manage positions and portfolio state."""

    @property
    def positions(self) -> tuple[Any, ...]: ...


@runtime_checkable
class IExecutionEngine(Protocol):
    """Run backtests and simulation execution."""

    @property
    def backtest_manager(self) -> Any: ...
