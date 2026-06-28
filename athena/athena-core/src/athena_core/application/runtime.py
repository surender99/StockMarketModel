"""Shared orchestration for CLI and SDK — REQ-CLI-001, REQ-SDK-001."""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

from athena_core.application.backtest_config import BacktestConfig
from athena_core.application.backtest_engine import BacktestEngine, BacktestResult
from athena_core.application.backtest_features import FeatureServiceProvider
from athena_core.application.config import AthenaConfig
from athena_core.application.config_loader import load_athena_config
from athena_core.application.errors import IngestError
from athena_core.application.experiment_tracker import ExperimentTracker
from athena_core.application.explainability import ShapExplainer
from athena_core.application.feature_service import FeatureService
from athena_core.application.ingest_ohlcv import IngestOHLCVUseCase, IngestResult
from athena_core.application.ml_scorer import MLSignalScorer
from athena_core.application.optimizer import OptimizerResult, StrategyOptimizer
from athena_core.application.regime_engine import RegimeEngine
from athena_core.application.scanner import DailyScanner, ScanResult, scan_result_to_dict
from athena_core.application.walk_forward import WalkForwardSummary, WalkForwardValidator
from athena_core.domain.strategy.config import StrategyConfig
from athena_core.infrastructure.nse_calendar import NSETradingCalendar
from athena_core.infrastructure.parquet_feature_store import ParquetFeatureStore
from athena_core.infrastructure.parquet_ohlcv_store import ParquetOHLCVStore
from athena_core.infrastructure.strategy_yaml_loader import StrategyLoadError, load_strategy_yaml


@dataclass(frozen=True)
class IngestBatchResult:
    """Batch ingest summary."""

    results: list[IngestResult]
    failures: list[tuple[str, str]]


@dataclass(frozen=True)
class BacktestRunResult:
    """Backtest output bundle."""

    result: BacktestResult
    experiment_id: str | None = None


class AthenaRuntime:
    """Programmatic access to Athena use cases — REQ-SDK-001."""

    def __init__(
        self,
        config: AthenaConfig | None = None,
        *,
        config_path: Path | None = None,
        profile: str | None = None,
    ) -> None:
        if config is None:
            self.config = load_athena_config(config_path, profile=profile)
        else:
            self.config = config
        self._calendar: NSETradingCalendar | None = None
        self._ohlcv_store: ParquetOHLCVStore | None = None
        self._feature_service: FeatureService | None = None
        self._regime_engine: RegimeEngine | None = None

    @staticmethod
    def load_symbols(path: Path) -> list[str]:
        with path.open(encoding="utf-8", newline="") as fh:
            reader = csv.DictReader(fh)
            if reader.fieldnames and "symbol" in reader.fieldnames:
                return [row["symbol"].strip() for row in reader if row.get("symbol")]
            fh.seek(0)
            return [line.strip() for line in fh if line.strip() and not line.startswith("symbol")]

    @staticmethod
    def resolve_symbols(
        strategy: StrategyConfig,
        *,
        symbol: str | None = None,
        symbols_file: Path | None = None,
    ) -> list[str]:
        symbols: list[str] = list(strategy.universe.symbols)
        if symbols_file is not None:
            symbols.extend(AthenaRuntime.load_symbols(symbols_file))
        if symbol:
            symbols.append(symbol)
        return list(dict.fromkeys(symbols))

    def _services(
        self,
    ) -> tuple[NSETradingCalendar, ParquetOHLCVStore, FeatureService, RegimeEngine]:
        if self._calendar is None:
            self._calendar = NSETradingCalendar(holidays_file=self.config.calendar.holidays_file)
            self._ohlcv_store = ParquetOHLCVStore(self.config.data_ingest.base_path)
            feature_store = ParquetFeatureStore(
                self.config.feature_store.base_path,
                self.config.feature_store.compression,
            )
            self._feature_service = FeatureService(
                feature_store,
                self._ohlcv_store,
                self.config.feature_store,
            )
            self._regime_engine = RegimeEngine(self._ohlcv_store, self.config.regime)
        assert self._calendar is not None
        assert self._ohlcv_store is not None
        assert self._feature_service is not None
        assert self._regime_engine is not None
        return self._calendar, self._ohlcv_store, self._feature_service, self._regime_engine

    def _backtest_engine(self) -> tuple[NSETradingCalendar, BacktestEngine]:
        calendar, ohlcv_store, feature_service, regime_engine = self._services()
        engine = BacktestEngine(
            calendar,
            ohlcv_store,
            FeatureServiceProvider(feature_service),
            regime_engine=regime_engine,
        )
        return calendar, engine

    def load_strategy(self, strategy_path: Path) -> StrategyConfig:
        return load_strategy_yaml(strategy_path)

    def ingest(
        self,
        symbols: list[str],
        start: date,
        end: date,
    ) -> IngestBatchResult:
        _, ohlcv_store, _, _ = self._services()
        use_case = IngestOHLCVUseCase(ohlcv_store, self.config.data_ingest)
        results: list[IngestResult] = []
        failures: list[tuple[str, str]] = []
        for sym in symbols:
            try:
                results.append(use_case.run(sym, start, end))
            except IngestError as exc:
                failures.append((exc.symbol, str(exc)))
        return IngestBatchResult(results=results, failures=failures)

    def backtest(
        self,
        strategy: StrategyConfig,
        start: date,
        end: date,
        *,
        symbols: list[str],
        track_experiment: bool = False,
        output_dir: Path | None = None,
    ) -> BacktestRunResult:
        bt_config = BacktestConfig(**self.config.backtest.model_dump(), start=start, end=end)
        _, engine = self._backtest_engine()
        result = engine.run(
            strategy,
            bt_config,
            symbols=symbols,
            dataset_version=self.config.feature_store.data_version,
        )
        experiment_id: str | None = None
        if output_dir is not None:
            output_dir.mkdir(parents=True, exist_ok=True)
            result.equity_curve.to_parquet(output_dir / "equity_curve.parquet", index=False)
            trades_payload = [
                {
                    "symbol": t.symbol,
                    "entry_date": t.entry_date.isoformat(),
                    "exit_date": t.exit_date.isoformat(),
                    "entry_price": t.entry_price,
                    "exit_price": t.exit_price,
                    "quantity": t.quantity,
                    "net_pnl": t.net_pnl,
                    "exit_reason": t.exit_reason,
                }
                for t in result.trades
            ]
            (output_dir / "trades.json").write_text(
                json.dumps(trades_payload, indent=2), encoding="utf-8"
            )
            if result.statistics_report is not None:
                (output_dir / "statistics.json").write_text(
                    json.dumps(result.statistics_report, indent=2),
                    encoding="utf-8",
                )

        if track_experiment:
            tracker = ExperimentTracker(self.config.experiment_tracking)
            artifacts: dict[str, str] = {}
            if output_dir is not None:
                artifacts = {
                    "equity_curve": str(output_dir / "equity_curve.parquet"),
                    "trades": str(output_dir / "trades.json"),
                }
            record = tracker.create_record(
                strategy,
                bt_config,
                result,
                dataset_version=self.config.feature_store.data_version,
                artifacts=artifacts,
            )
            tracker.save(record)
            experiment_id = record.experiment_id
        return BacktestRunResult(result=result, experiment_id=experiment_id)

    def scan(
        self,
        strategy: StrategyConfig,
        symbols: list[str],
        as_of: date,
    ) -> ScanResult:
        _, ohlcv_store, feature_service, regime_engine = self._services()
        ml_scorer: MLSignalScorer | None = None
        explainer: ShapExplainer | None = None
        if self.config.scanner.use_ml_scorer or self.config.ml_scorer.enabled:
            ml_scorer = MLSignalScorer(self.config.ml_scorer)
            explainer = ShapExplainer(self.config.explainability)
        scanner = DailyScanner(
            ohlcv_store,
            FeatureServiceProvider(feature_service),
            config=self.config.scanner,
            regime_engine=regime_engine,
            ml_scorer=ml_scorer,
            explainer=explainer,
        )
        return scanner.scan(strategy, symbols, as_of)

    def walk_forward(
        self,
        strategy: StrategyConfig,
        start: date,
        end: date,
        *,
        symbols: list[str],
    ) -> WalkForwardSummary:
        bt_config = BacktestConfig(**self.config.backtest.model_dump(), start=start, end=end)
        calendar, engine = self._backtest_engine()
        validator = WalkForwardValidator(calendar, engine, self.config.walk_forward)
        return validator.run(
            strategy,
            bt_config,
            symbols=symbols,
            dataset_version=self.config.feature_store.data_version,
            start=start,
            end=end,
        )

    def optimize(
        self,
        strategy: StrategyConfig,
        start: date,
        end: date,
        *,
        symbols: list[str],
    ) -> OptimizerResult:
        bt_config = BacktestConfig(**self.config.backtest.model_dump(), start=start, end=end)
        calendar, engine = self._backtest_engine()
        validator = WalkForwardValidator(calendar, engine, self.config.walk_forward)
        optimizer = StrategyOptimizer(validator, self.config.optimizer)
        return optimizer.run(
            strategy,
            bt_config,
            symbols=symbols,
            dataset_version=self.config.feature_store.data_version,
            start=start,
            end=end,
        )

    def compare_experiments(
        self,
        experiment_ids: list[str] | None = None,
        *,
        latest: int | None = None,
    ) -> dict[str, Any]:
        tracker = ExperimentTracker(self.config.experiment_tracking)
        if latest is not None:
            return tracker.compare_experiments(latest=latest)
        if experiment_ids is None:
            msg = "experiment_ids or latest is required"
            raise ValueError(msg)
        return tracker.compare_experiments(experiment_ids)


def walk_forward_to_dict(summary: WalkForwardSummary) -> dict[str, Any]:
    return {
        "fold_count": summary.aggregate_metrics.get("fold_count", 0),
        "aggregate_metrics": summary.aggregate_metrics,
        "folds": [
            {
                "fold": fold.window.fold,
                "train_start": fold.window.train_start.isoformat(),
                "train_end": fold.window.train_end.isoformat(),
                "test_start": fold.window.test_start.isoformat(),
                "test_end": fold.window.test_end.isoformat(),
                "metrics": fold.result.metrics,
            }
            for fold in summary.folds
        ],
    }


def optimizer_to_dict(result: OptimizerResult) -> dict[str, Any]:
    return {
        "method": result.method,
        "trial_count": len(result.trials),
        "best_trial": None
        if result.best_trial is None
        else {
            "trial_id": result.best_trial.trial_id,
            "parameters": result.best_trial.parameters,
            "composite_score": result.best_trial.composite_score,
            "aggregate_metrics": result.best_trial.aggregate_metrics,
        },
        "trials": [
            {
                "trial_id": trial.trial_id,
                "parameters": trial.parameters,
                "composite_score": trial.composite_score,
                "aggregate_metrics": trial.aggregate_metrics,
            }
            for trial in result.trials
        ],
    }


def format_comparison_table(comparison: dict[str, Any]) -> str:
    keys = comparison["metric_keys"]
    header = ["experiment_id", "strategy_id", "train_start", "train_end", *keys]
    rows = [header]
    for row in comparison["experiments"]:
        rows.append([str(row.get(col, "")) for col in header])
    col_widths = [max(len(row[i]) for row in rows) for i in range(len(header))]
    lines: list[str] = []
    for i, row in enumerate(rows):
        line = "  ".join(val.ljust(col_widths[j]) for j, val in enumerate(row))
        lines.append(line)
        if i == 0:
            lines.append("  ".join("-" * width for width in col_widths))
    return "\n".join(lines)


__all__ = [
    "AthenaRuntime",
    "BacktestRunResult",
    "IngestBatchResult",
    "StrategyLoadError",
    "format_comparison_table",
    "optimizer_to_dict",
    "scan_result_to_dict",
    "walk_forward_to_dict",
]
