"""Athena core CLI — REQ-DATA-INGEST-001, REQ-BT-ENGINE-001, REQ-EXP-TRACK-001, REQ-SCANNER-001, REQ-WALK-FORWARD-001, REQ-EXP-COMPARE-001."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import date
from pathlib import Path

import yaml

from athena_core import __version__
from athena_core.application.backtest_config import BacktestConfig, ExperimentTrackingConfig
from athena_core.application.backtest_engine import BacktestEngine
from athena_core.application.backtest_features import FeatureServiceProvider
from athena_core.application.config import (
    AthenaConfig,
    BacktestSettings,
    CalendarConfig,
    DataIngestConfig,
    FeatureStoreConfig,
)
from athena_core.application.errors import IngestError
from athena_core.application.experiment_tracker import ExperimentTracker
from athena_core.application.feature_service import FeatureService
from athena_core.application.ingest_ohlcv import IngestOHLCVUseCase
from athena_core.application.regime_config import RegimeConfig
from athena_core.application.regime_engine import RegimeEngine
from athena_core.application.scanner import DailyScanner
from athena_core.application.scanner_config import ScannerConfig
from athena_core.application.walk_forward import WalkForwardValidator
from athena_core.application.walk_forward_config import WalkForwardConfig
from athena_core.infrastructure.logging import configure_logging, get_logger
from athena_core.infrastructure.nse_calendar import NSETradingCalendar
from athena_core.infrastructure.parquet_feature_store import ParquetFeatureStore
from athena_core.infrastructure.parquet_ohlcv_store import ParquetOHLCVStore
from athena_core.infrastructure.strategy_yaml_loader import StrategyLoadError, load_strategy_yaml


def _load_config(path: Path | None) -> AthenaConfig:
    if path is None or not path.is_file():
        return AthenaConfig()
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        return AthenaConfig()
    return AthenaConfig(
        calendar=CalendarConfig.model_validate(raw.get("calendar", {})),
        data_ingest=DataIngestConfig.model_validate(raw.get("data_ingest", {})),
        feature_store=FeatureStoreConfig.model_validate(raw.get("feature_store", {})),
        backtest=BacktestSettings.model_validate(raw.get("backtest", {})),
        experiment_tracking=ExperimentTrackingConfig.model_validate(raw.get("experiment_tracking", {})),
        regime=RegimeConfig.model_validate(raw.get("regime", {})),
        scanner=ScannerConfig.model_validate(raw.get("scanner", {})),
        walk_forward=WalkForwardConfig.model_validate(raw.get("walk_forward", {})),
    )


def _parse_date(value: str) -> date:
    return date.fromisoformat(value)


def _load_symbols(path: Path) -> list[str]:
    with path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames and "symbol" in reader.fieldnames:
            return [row["symbol"].strip() for row in reader if row.get("symbol")]
        fh.seek(0)
        return [line.strip() for line in fh if line.strip() and not line.startswith("symbol")]


def _build_services(config: AthenaConfig) -> tuple[NSETradingCalendar, ParquetOHLCVStore, FeatureService, RegimeEngine]:
    calendar = NSETradingCalendar(holidays_file=config.calendar.holidays_file)
    ohlcv_store = ParquetOHLCVStore(config.data_ingest.base_path)
    feature_store = ParquetFeatureStore(config.feature_store.base_path, config.feature_store.compression)
    feature_service = FeatureService(feature_store, ohlcv_store, config.feature_store)
    regime_engine = RegimeEngine(ohlcv_store, config.regime)
    return calendar, ohlcv_store, feature_service, regime_engine


def _cmd_ingest(args: argparse.Namespace) -> int:
    log = get_logger("athena_core.cli.ingest")
    config = _load_config(args.config)
    store = ParquetOHLCVStore(config.data_ingest.base_path)
    use_case = IngestOHLCVUseCase(store, config.data_ingest)

    symbols: list[str] = []
    if args.symbol:
        symbols.append(args.symbol)
    if args.symbols_file:
        symbols.extend(_load_symbols(Path(args.symbols_file)))

    if not symbols:
        log.error("ingest.no_symbols")
        return 1

    start = _parse_date(args.start)
    end = _parse_date(args.end)
    failures = 0
    for sym in symbols:
        try:
            result = use_case.run(sym, start, end)
            log.info(
                "ingest.symbol_ok",
                symbol=result.symbol,
                rows=result.row_count,
                source=result.source,
            )
        except IngestError as exc:
            log.error("ingest.failed", symbol=exc.symbol, error=str(exc))
            failures += 1
    return 1 if failures else 0


def _cmd_backtest(args: argparse.Namespace) -> int:
    log = get_logger("athena_core.cli.backtest")
    config = _load_config(args.config)

    try:
        strategy = load_strategy_yaml(args.strategy)
    except StrategyLoadError as exc:
        log.error("backtest.strategy_load_failed", error=str(exc))
        return 1

    symbols: list[str] = list(strategy.universe.symbols)
    if args.symbols_file:
        symbols.extend(_load_symbols(Path(args.symbols_file)))
    if args.symbol:
        symbols.append(args.symbol)
    symbols = list(dict.fromkeys(symbols))
    if not symbols:
        log.error("backtest.no_symbols")
        return 1

    start = _parse_date(args.start)
    end = _parse_date(args.end)
    bt_config = BacktestConfig(**config.backtest.model_dump(), start=start, end=end)

    calendar, ohlcv_store, feature_service, regime_engine = _build_services(config)
    engine = BacktestEngine(
        calendar,
        ohlcv_store,
        FeatureServiceProvider(feature_service),
        regime_engine=regime_engine,
    )

    result = engine.run(
        strategy,
        bt_config,
        symbols=symbols,
        dataset_version=config.feature_store.data_version,
    )

    log.info("backtest.complete", metrics=result.metrics, trades=len(result.trades))

    if args.output:
        out = Path(args.output)
        out.mkdir(parents=True, exist_ok=True)
        result.equity_curve.to_parquet(out / "equity_curve.parquet", index=False)
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
        (out / "trades.json").write_text(json.dumps(trades_payload, indent=2), encoding="utf-8")

    if args.track_experiment:
        tracker = ExperimentTracker(config.experiment_tracking)
        artifacts = {}
        if args.output:
            artifacts = {
                "equity_curve": str(Path(args.output) / "equity_curve.parquet"),
                "trades": str(Path(args.output) / "trades.json"),
            }
        record = tracker.create_record(
            strategy,
            bt_config,
            result,
            dataset_version=config.feature_store.data_version,
            artifacts=artifacts,
        )
        path = tracker.save(record)
        log.info("backtest.experiment_saved", experiment_id=record.experiment_id, path=str(path))

    return 0


def _cmd_scan(args: argparse.Namespace) -> int:
    log = get_logger("athena_core.cli.scan")
    config = _load_config(args.config)

    try:
        strategy = load_strategy_yaml(args.strategy)
    except StrategyLoadError as exc:
        log.error("scan.strategy_load_failed", error=str(exc))
        return 1

    symbols: list[str] = list(strategy.universe.symbols)
    if args.symbols_file:
        symbols.extend(_load_symbols(Path(args.symbols_file)))
    if args.symbol:
        symbols.append(args.symbol)
    symbols = list(dict.fromkeys(symbols))
    if not symbols:
        log.error("scan.no_symbols")
        return 1

    as_of = _parse_date(args.as_of)
    _, ohlcv_store, feature_service, regime_engine = _build_services(config)
    scanner = DailyScanner(
        ohlcv_store,
        FeatureServiceProvider(feature_service),
        config=config.scanner,
        regime_engine=regime_engine,
    )
    result = scanner.scan(strategy, symbols, as_of)
    payload = scanner.candidates_to_dict(result)
    log.info("scan.complete", candidates=len(result.candidates), scanned=result.scanned_count)

    if args.output:
        Path(args.output).write_text(json.dumps(payload, indent=2), encoding="utf-8")
    else:
        print(json.dumps(payload, indent=2))
    return 0


def _cmd_walk_forward(args: argparse.Namespace) -> int:
    log = get_logger("athena_core.cli.walk_forward")
    config = _load_config(args.config)

    try:
        strategy = load_strategy_yaml(args.strategy)
    except StrategyLoadError as exc:
        log.error("walk_forward.strategy_load_failed", error=str(exc))
        return 1

    symbols: list[str] = list(strategy.universe.symbols)
    if args.symbols_file:
        symbols.extend(_load_symbols(Path(args.symbols_file)))
    if args.symbol:
        symbols.append(args.symbol)
    symbols = list(dict.fromkeys(symbols))
    if not symbols:
        log.error("walk_forward.no_symbols")
        return 1

    start = _parse_date(args.start)
    end = _parse_date(args.end)
    bt_config = BacktestConfig(**config.backtest.model_dump(), start=start, end=end)

    calendar, ohlcv_store, feature_service, regime_engine = _build_services(config)
    engine = BacktestEngine(
        calendar,
        ohlcv_store,
        FeatureServiceProvider(feature_service),
        regime_engine=regime_engine,
    )
    validator = WalkForwardValidator(calendar, engine, config.walk_forward)
    summary = validator.run(
        strategy,
        bt_config,
        symbols=symbols,
        dataset_version=config.feature_store.data_version,
        start=start,
        end=end,
    )

    output = {
        "fold_count": summary.aggregate_metrics.get("fold_count", 0),
        "aggregate_metrics": summary.aggregate_metrics,
        "folds": [
            {
                "fold": f.window.fold,
                "train_start": f.window.train_start.isoformat(),
                "train_end": f.window.train_end.isoformat(),
                "test_start": f.window.test_start.isoformat(),
                "test_end": f.window.test_end.isoformat(),
                "metrics": f.result.metrics,
            }
            for f in summary.folds
        ],
    }
    log.info("walk_forward.complete", folds=output["fold_count"])

    if args.output:
        Path(args.output).write_text(json.dumps(output, indent=2), encoding="utf-8")
    else:
        print(json.dumps(output, indent=2))
    return 0


def _cmd_compare_experiments(args: argparse.Namespace) -> int:
    log = get_logger("athena_core.cli.compare")
    config = _load_config(args.config)
    tracker = ExperimentTracker(config.experiment_tracking)

    try:
        if args.latest:
            comparison = tracker.compare_experiments(latest=args.latest)
        else:
            comparison = tracker.compare_experiments(list(args.experiment_id))
    except (FileNotFoundError, ValueError) as exc:
        log.error("compare.failed", error=str(exc))
        return 1

    if args.format == "json":
        text = json.dumps(comparison, indent=2)
    else:
        keys = comparison["metric_keys"]
        header = ["experiment_id", "strategy_id", "train_start", "train_end", *keys]
        rows = [header]
        for row in comparison["experiments"]:
            rows.append([str(row.get(col, "")) for col in header])
        col_widths = [max(len(r[i]) for r in rows) for i in range(len(header))]
        lines = []
        for i, row in enumerate(rows):
            line = "  ".join(val.ljust(col_widths[j]) for j, val in enumerate(row))
            lines.append(line)
            if i == 0:
                lines.append("  ".join("-" * w for w in col_widths))
        text = "\n".join(lines)

    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    else:
        print(text)
    log.info("compare.complete", count=len(comparison["experiments"]))
    return 0


def main(argv: list[str] | None = None) -> int:
    """Entry point for Athena core CLI."""
    parser = argparse.ArgumentParser(prog="athena-core", description="Athena core utilities")
    parser.add_argument("--version", action="version", version=f"athena-core {__version__}")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable debug logging")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("health", help="Verify installation")

    ingest_parser = subparsers.add_parser("ingest", help="Ingest OHLCV via yfinance → Parquet")
    ingest_parser.add_argument("--symbol", help="Single symbol (e.g. RELIANCE or RELIANCE.NS)")
    ingest_parser.add_argument("--symbols-file", help="CSV with symbol column")
    ingest_parser.add_argument("--start", required=True, help="Start date ISO (YYYY-MM-DD)")
    ingest_parser.add_argument("--end", required=True, help="End date ISO (YYYY-MM-DD)")
    ingest_parser.add_argument("--config", type=Path, help="YAML config path")

    backtest_parser = subparsers.add_parser("backtest", help="Run configuration-driven backtest")
    backtest_parser.add_argument("--strategy", type=Path, required=True, help="Strategy YAML path")
    backtest_parser.add_argument("--start", required=True, help="Start date ISO (YYYY-MM-DD)")
    backtest_parser.add_argument("--end", required=True, help="End date ISO (YYYY-MM-DD)")
    backtest_parser.add_argument("--symbol", help="Single symbol override")
    backtest_parser.add_argument("--symbols-file", help="CSV with symbol column")
    backtest_parser.add_argument("--config", type=Path, help="YAML config path")
    backtest_parser.add_argument("--output", type=Path, help="Directory for equity curve and trades")
    backtest_parser.add_argument(
        "--track-experiment",
        action="store_true",
        help="Persist experiment metadata JSON",
    )

    scan_parser = subparsers.add_parser("scan", help="Daily universe scanner — REQ-SCANNER-001")
    scan_parser.add_argument("--strategy", type=Path, required=True, help="Strategy YAML path")
    scan_parser.add_argument("--as-of", required=True, help="Scan date ISO (YYYY-MM-DD)")
    scan_parser.add_argument("--symbol", help="Single symbol override")
    scan_parser.add_argument("--symbols-file", help="CSV with symbol column")
    scan_parser.add_argument("--config", type=Path, help="YAML config path")
    scan_parser.add_argument("--output", type=Path, help="JSON output path")

    wf_parser = subparsers.add_parser("walk-forward", help="Walk-forward validation — REQ-WALK-FORWARD-001")
    wf_parser.add_argument("--strategy", type=Path, required=True, help="Strategy YAML path")
    wf_parser.add_argument("--start", required=True, help="Start date ISO (YYYY-MM-DD)")
    wf_parser.add_argument("--end", required=True, help="End date ISO (YYYY-MM-DD)")
    wf_parser.add_argument("--symbol", help="Single symbol override")
    wf_parser.add_argument("--symbols-file", help="CSV with symbol column")
    wf_parser.add_argument("--config", type=Path, help="YAML config path")
    wf_parser.add_argument("--output", type=Path, help="JSON output path")

    compare_parser = subparsers.add_parser(
        "compare-experiments",
        help="Side-by-side experiment metrics — REQ-EXP-COMPARE-001",
    )
    compare_parser.add_argument("experiment_id", nargs="*", help="Experiment IDs to compare")
    compare_parser.add_argument("--latest", type=int, help="Compare N most recent experiments")
    compare_parser.add_argument("--config", type=Path, help="YAML config path")
    compare_parser.add_argument("--format", choices=["table", "json"], default="table")
    compare_parser.add_argument("--output", type=Path, help="Output path")

    args = parser.parse_args(argv)
    configure_logging(level=10 if args.verbose else 20)
    log = get_logger("athena_core.cli")

    if args.command == "health":
        log.info("athena_core.health_ok", version=__version__)
        return 0
    if args.command == "ingest":
        return _cmd_ingest(args)
    if args.command == "backtest":
        return _cmd_backtest(args)
    if args.command == "scan":
        return _cmd_scan(args)
    if args.command == "walk-forward":
        return _cmd_walk_forward(args)
    if args.command == "compare-experiments":
        return _cmd_compare_experiments(args)

    parser.print_help()
    return 0 if args.command is None else 1


if __name__ == "__main__":
    sys.exit(main())
