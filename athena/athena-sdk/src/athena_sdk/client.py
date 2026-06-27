"""AthenaClient — REQ-SDK-001.

Public facade over Athena core use cases. Internal imports from ``athena_core``
are implementation details; external callers should use only ``AthenaClient``.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

from athena_core.application.config import AthenaConfig
from athena_core.application.config_loader import list_profile_names, load_athena_config
from athena_core.application.optimizer import OptimizerResult
from athena_core.application.runtime import (
    AthenaRuntime,
    BacktestRunResult,
    IngestBatchResult,
    StrategyLoadError,
    format_comparison_table,
    optimizer_to_dict,
    scan_result_to_dict,
    walk_forward_to_dict,
)
from athena_core.application.scanner import ScanResult
from athena_core.application.walk_forward import WalkForwardSummary
from athena_core.domain.strategy.config import StrategyConfig


class AthenaClient:
    """Programmatic facade over Athena core use cases — REQ-SDK-001."""

    def __init__(
        self,
        config_path: Path | str | None = None,
        *,
        profile: str | None = None,
        config: AthenaConfig | None = None,
    ) -> None:
        path = Path(config_path) if config_path is not None else None
        self._runtime = AthenaRuntime(config=config, config_path=path, profile=profile)
        self.config_path = path
        self.profile = profile

    @property
    def config(self) -> AthenaConfig:
        return self._runtime.config

    def list_profiles(self) -> list[str]:
        return list_profile_names(self.config_path)

    @staticmethod
    def load_config(
        config_path: Path | str | None = None,
        *,
        profile: str | None = None,
    ) -> AthenaConfig:
        path = Path(config_path) if config_path is not None else None
        return load_athena_config(path, profile=profile)

    def load_strategy(self, strategy_path: Path | str) -> StrategyConfig:
        return self._runtime.load_strategy(Path(strategy_path))

    def ingest(
        self,
        symbols: list[str],
        start: date,
        end: date,
    ) -> IngestBatchResult:
        return self._runtime.ingest(symbols, start, end)

    def backtest(
        self,
        strategy: StrategyConfig | Path | str,
        start: date,
        end: date,
        *,
        symbols: list[str] | None = None,
        symbol: str | None = None,
        symbols_file: Path | str | None = None,
        track_experiment: bool = False,
        output_dir: Path | str | None = None,
    ) -> BacktestRunResult:
        strategy_cfg = self._coerce_strategy(strategy)
        resolved = symbols or self._runtime.resolve_symbols(
            strategy_cfg,
            symbol=symbol,
            symbols_file=Path(symbols_file) if symbols_file else None,
        )
        out = Path(output_dir) if output_dir is not None else None
        return self._runtime.backtest(
            strategy_cfg,
            start,
            end,
            symbols=resolved,
            track_experiment=track_experiment,
            output_dir=out,
        )

    def scan(
        self,
        strategy: StrategyConfig | Path | str,
        as_of: date,
        *,
        symbols: list[str] | None = None,
        symbol: str | None = None,
        symbols_file: Path | str | None = None,
    ) -> ScanResult:
        strategy_cfg = self._coerce_strategy(strategy)
        resolved = symbols or self._runtime.resolve_symbols(
            strategy_cfg,
            symbol=symbol,
            symbols_file=Path(symbols_file) if symbols_file else None,
        )
        return self._runtime.scan(strategy_cfg, resolved, as_of)

    def scan_dict(
        self,
        strategy: StrategyConfig | Path | str,
        as_of: date,
        *,
        symbols: list[str] | None = None,
        symbol: str | None = None,
        symbols_file: Path | str | None = None,
    ) -> dict[str, Any]:
        return scan_result_to_dict(
            self.scan(
                strategy,
                as_of,
                symbols=symbols,
                symbol=symbol,
                symbols_file=symbols_file,
            )
        )

    def walk_forward(
        self,
        strategy: StrategyConfig | Path | str,
        start: date,
        end: date,
        *,
        symbols: list[str] | None = None,
        symbol: str | None = None,
        symbols_file: Path | str | None = None,
    ) -> WalkForwardSummary:
        strategy_cfg = self._coerce_strategy(strategy)
        resolved = symbols or self._runtime.resolve_symbols(
            strategy_cfg,
            symbol=symbol,
            symbols_file=Path(symbols_file) if symbols_file else None,
        )
        return self._runtime.walk_forward(strategy_cfg, start, end, symbols=resolved)

    def walk_forward_dict(
        self,
        strategy: StrategyConfig | Path | str,
        start: date,
        end: date,
        **kwargs: Any,
    ) -> dict[str, Any]:
        return walk_forward_to_dict(self.walk_forward(strategy, start, end, **kwargs))

    def optimize(
        self,
        strategy: StrategyConfig | Path | str,
        start: date,
        end: date,
        *,
        symbols: list[str] | None = None,
        symbol: str | None = None,
        symbols_file: Path | str | None = None,
    ) -> OptimizerResult:
        strategy_cfg = self._coerce_strategy(strategy)
        resolved = symbols or self._runtime.resolve_symbols(
            strategy_cfg,
            symbol=symbol,
            symbols_file=Path(symbols_file) if symbols_file else None,
        )
        return self._runtime.optimize(strategy_cfg, start, end, symbols=resolved)

    def optimize_dict(
        self,
        strategy: StrategyConfig | Path | str,
        start: date,
        end: date,
        **kwargs: Any,
    ) -> dict[str, Any]:
        return optimizer_to_dict(self.optimize(strategy, start, end, **kwargs))

    def compare_experiments(
        self,
        experiment_ids: list[str] | None = None,
        *,
        latest: int | None = None,
        as_table: bool = False,
    ) -> dict[str, Any] | str:
        comparison = self._runtime.compare_experiments(experiment_ids, latest=latest)
        if as_table:
            return format_comparison_table(comparison)
        return comparison

    def _coerce_strategy(self, strategy: StrategyConfig | Path | str) -> StrategyConfig:
        if isinstance(strategy, StrategyConfig):
            return strategy
        return self.load_strategy(strategy)


__all__ = ["AthenaClient", "StrategyLoadError"]
