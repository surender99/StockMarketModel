"""Athena core CLI — REQ-DATA-INGEST-001, REQ-BT-ENGINE-001, REQ-EXP-TRACK-001, REQ-SCANNER-001, REQ-WALK-FORWARD-001, REQ-EXP-COMPARE-001, REQ-OPT-001, REQ-ML-SCORER-001, REQ-EXPLAIN-001, REQ-CLI-001."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

from athena_core import __version__
from athena_core.application.runtime import (
    AthenaRuntime,
    StrategyLoadError,
    format_comparison_table,
    optimizer_to_dict,
    scan_result_to_dict,
    walk_forward_to_dict,
)
from athena_core.infrastructure.logging import configure_logging, get_logger


def _parse_date(value: str) -> date:
    return date.fromisoformat(value)


def _runtime(args: argparse.Namespace) -> AthenaRuntime:
    return AthenaRuntime(config_path=args.config, profile=getattr(args, "profile", None))


def _cmd_ingest(args: argparse.Namespace) -> int:
    log = get_logger("athena_core.cli.ingest")
    runtime = _runtime(args)
    symbols: list[str] = []
    if args.symbol:
        symbols.append(args.symbol)
    if args.symbols_file:
        symbols.extend(AthenaRuntime.load_symbols(Path(args.symbols_file)))
    if not symbols:
        log.error("ingest.no_symbols")
        return 1
    batch = runtime.ingest(symbols, _parse_date(args.start), _parse_date(args.end))
    for result in batch.results:
        log.info("ingest.symbol_ok", symbol=result.symbol, rows=result.row_count, source=result.source)
    for symbol, error in batch.failures:
        log.error("ingest.failed", symbol=symbol, error=error)
    return 1 if batch.failures else 0


def _cmd_backtest(args: argparse.Namespace) -> int:
    log = get_logger("athena_core.cli.backtest")
    runtime = _runtime(args)
    try:
        strategy = runtime.load_strategy(args.strategy)
    except StrategyLoadError as exc:
        log.error("backtest.strategy_load_failed", error=str(exc))
        return 1
    symbols = runtime.resolve_symbols(
        strategy,
        symbol=args.symbol,
        symbols_file=Path(args.symbols_file) if args.symbols_file else None,
    )
    if not symbols:
        log.error("backtest.no_symbols")
        return 1
    run = runtime.backtest(
        strategy,
        _parse_date(args.start),
        _parse_date(args.end),
        symbols=symbols,
        track_experiment=args.track_experiment,
        output_dir=args.output,
    )
    log.info("backtest.complete", metrics=run.result.metrics, trades=len(run.result.trades))
    if run.experiment_id:
        log.info("backtest.experiment_saved", experiment_id=run.experiment_id)
    return 0


def _cmd_scan(args: argparse.Namespace) -> int:
    log = get_logger("athena_core.cli.scan")
    runtime = _runtime(args)
    try:
        strategy = runtime.load_strategy(args.strategy)
    except StrategyLoadError as exc:
        log.error("scan.strategy_load_failed", error=str(exc))
        return 1
    symbols = runtime.resolve_symbols(
        strategy,
        symbol=args.symbol,
        symbols_file=Path(args.symbols_file) if args.symbols_file else None,
    )
    if not symbols:
        log.error("scan.no_symbols")
        return 1
    result = runtime.scan(strategy, symbols, _parse_date(args.as_of))
    payload = scan_result_to_dict(result)
    log.info("scan.complete", candidates=len(result.candidates), scanned=result.scanned_count)
    text = json.dumps(payload, indent=2)
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    else:
        print(text)
    return 0


def _cmd_walk_forward(args: argparse.Namespace) -> int:
    log = get_logger("athena_core.cli.walk_forward")
    runtime = _runtime(args)
    try:
        strategy = runtime.load_strategy(args.strategy)
    except StrategyLoadError as exc:
        log.error("walk_forward.strategy_load_failed", error=str(exc))
        return 1
    symbols = runtime.resolve_symbols(
        strategy,
        symbol=args.symbol,
        symbols_file=Path(args.symbols_file) if args.symbols_file else None,
    )
    if not symbols:
        log.error("walk_forward.no_symbols")
        return 1
    summary = runtime.walk_forward(
        strategy,
        _parse_date(args.start),
        _parse_date(args.end),
        symbols=symbols,
    )
    output = walk_forward_to_dict(summary)
    log.info("walk_forward.complete", folds=output["fold_count"])
    text = json.dumps(output, indent=2)
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    else:
        print(text)
    return 0


def _cmd_optimize(args: argparse.Namespace) -> int:
    log = get_logger("athena_core.cli.optimize")
    runtime = _runtime(args)
    try:
        strategy = runtime.load_strategy(args.strategy)
    except StrategyLoadError as exc:
        log.error("optimize.strategy_load_failed", error=str(exc))
        return 1
    symbols = runtime.resolve_symbols(
        strategy,
        symbol=args.symbol,
        symbols_file=Path(args.symbols_file) if args.symbols_file else None,
    )
    if not symbols:
        log.error("optimize.no_symbols")
        return 1
    result = runtime.optimize(
        strategy,
        _parse_date(args.start),
        _parse_date(args.end),
        symbols=symbols,
    )
    output = optimizer_to_dict(result)
    log.info("optimize.complete", trials=output["trial_count"], best=output["best_trial"])
    text = json.dumps(output, indent=2)
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    else:
        print(text)
    return 0


def _cmd_compare_experiments(args: argparse.Namespace) -> int:
    log = get_logger("athena_core.cli.compare")
    runtime = _runtime(args)
    try:
        if args.latest:
            comparison = runtime.compare_experiments(latest=args.latest)
        else:
            comparison = runtime.compare_experiments(list(args.experiment_id))
    except (FileNotFoundError, ValueError) as exc:
        log.error("compare.failed", error=str(exc))
        return 1
    text = json.dumps(comparison, indent=2) if args.format == "json" else format_comparison_table(comparison)
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    else:
        print(text)
    log.info("compare.complete", count=len(comparison["experiments"]))
    return 0


def _add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--config", type=Path, help="YAML config path")
    parser.add_argument("--profile", help="Named config profile from YAML")


def _add_symbol_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--symbol", help="Single symbol override")
    parser.add_argument("--symbols-file", help="CSV with symbol column")


def _add_output_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--output", type=Path, help="Output file or directory path")


def build_parser() -> argparse.ArgumentParser:
    """Build argparse parser for athena-core CLI."""
    parser = argparse.ArgumentParser(prog="athena-core", description="Athena core utilities")
    parser.add_argument("--version", action="version", version=f"athena-core {__version__}")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable debug logging")
    _add_common_args(parser)
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("health", help="Verify installation")

    ingest_parser = subparsers.add_parser("ingest", help="Ingest OHLCV via yfinance → Parquet")
    ingest_parser.add_argument("--symbol", help="Single symbol (e.g. RELIANCE or RELIANCE.NS)")
    ingest_parser.add_argument("--symbols-file", help="CSV with symbol column")
    ingest_parser.add_argument("--start", required=True, help="Start date ISO (YYYY-MM-DD)")
    ingest_parser.add_argument("--end", required=True, help="End date ISO (YYYY-MM-DD)")

    backtest_parser = subparsers.add_parser("backtest", help="Run configuration-driven backtest")
    backtest_parser.add_argument("--strategy", type=Path, required=True, help="Strategy YAML path")
    backtest_parser.add_argument("--start", required=True, help="Start date ISO (YYYY-MM-DD)")
    backtest_parser.add_argument("--end", required=True, help="End date ISO (YYYY-MM-DD)")
    _add_symbol_args(backtest_parser)
    _add_output_args(backtest_parser)
    backtest_parser.add_argument(
        "--track-experiment",
        action="store_true",
        help="Persist experiment metadata JSON",
    )

    scan_parser = subparsers.add_parser("scan", help="Daily universe scanner — REQ-SCANNER-001")
    scan_parser.add_argument("--strategy", type=Path, required=True, help="Strategy YAML path")
    scan_parser.add_argument("--as-of", required=True, help="Scan date ISO (YYYY-MM-DD)")
    _add_symbol_args(scan_parser)
    _add_output_args(scan_parser)

    wf_parser = subparsers.add_parser("walk-forward", help="Walk-forward validation — REQ-WALK-FORWARD-001")
    wf_parser.add_argument("--strategy", type=Path, required=True, help="Strategy YAML path")
    wf_parser.add_argument("--start", required=True, help="Start date ISO (YYYY-MM-DD)")
    wf_parser.add_argument("--end", required=True, help="End date ISO (YYYY-MM-DD)")
    _add_symbol_args(wf_parser)
    _add_output_args(wf_parser)

    opt_parser = subparsers.add_parser("optimize", help="Parameter search — REQ-OPT-001")
    opt_parser.add_argument("--strategy", type=Path, required=True, help="Strategy YAML path")
    opt_parser.add_argument("--start", required=True, help="Start date ISO (YYYY-MM-DD)")
    opt_parser.add_argument("--end", required=True, help="End date ISO (YYYY-MM-DD)")
    _add_symbol_args(opt_parser)
    _add_output_args(opt_parser)

    compare_parser = subparsers.add_parser(
        "compare-experiments",
        help="Side-by-side experiment metrics — REQ-EXP-COMPARE-001",
    )
    compare_parser.add_argument("experiment_id", nargs="*", help="Experiment IDs to compare")
    compare_parser.add_argument("--latest", type=int, help="Compare N most recent experiments")
    compare_parser.add_argument("--format", choices=["table", "json"], default="table")
    _add_output_args(compare_parser)
    return parser


def main(argv: list[str] | None = None) -> int:
    """Entry point for Athena core CLI."""
    parser = build_parser()
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
    if args.command == "optimize":
        return _cmd_optimize(args)
    if args.command == "compare-experiments":
        return _cmd_compare_experiments(args)

    parser.print_help()
    return 0 if args.command is None else 1


if __name__ == "__main__":
    sys.exit(main())
