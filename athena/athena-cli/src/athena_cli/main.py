"""Polished Athena CLI entrypoint — REQ-CLI-001."""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

from athena_core.infrastructure.logging import configure_logging, get_logger
from athena_sdk import AthenaClient
from athena_sdk.client import StrategyLoadError

from athena_cli import __version__
from athena_cli.formatting import emit_output, render_payload


def _parse_date(value: str) -> date:
    return date.fromisoformat(value)


def _client(args: argparse.Namespace) -> AthenaClient:
    return AthenaClient(config_path=args.config, profile=args.profile)


def _cmd_health(_: argparse.Namespace) -> int:
    log = get_logger("athena.cli.health")
    log.info("athena.health_ok", version=__version__)
    print(f"athena {__version__} (core + sdk ready)")
    return 0


def _cmd_profiles(args: argparse.Namespace) -> int:
    client = _client(args)
    names = client.list_profiles()
    payload = {"config": str(args.config) if args.config else None, "profiles": names}
    emit_output(
        render_payload(payload, output_format=args.output_format),
        output_path=getattr(args, "output", None),
    )
    return 0


def _cmd_ingest(args: argparse.Namespace) -> int:
    log = get_logger("athena.cli.ingest")
    client = _client(args)
    symbols: list[str] = []
    if args.symbol:
        symbols.append(args.symbol)
    if args.symbols_file:
        symbols.extend(client._runtime.load_symbols(Path(args.symbols_file)))
    if not symbols:
        log.error("ingest.no_symbols")
        return 1
    batch = client.ingest(symbols, _parse_date(args.start), _parse_date(args.end))
    payload = {
        "ingested": [
            {"symbol": result.symbol, "rows": result.row_count, "source": result.source}
            for result in batch.results
        ],
        "failures": [{"symbol": symbol, "error": error} for symbol, error in batch.failures],
    }
    log.info("ingest.complete", ok=len(batch.results), failed=len(batch.failures))
    emit_output(
        render_payload(payload, output_format=args.output_format),
        output_path=getattr(args, "output", None),
    )
    return 1 if batch.failures else 0


def _cmd_backtest(args: argparse.Namespace) -> int:
    log = get_logger("athena.cli.backtest")
    client = _client(args)
    try:
        run = client.backtest(
            args.strategy,
            _parse_date(args.start),
            _parse_date(args.end),
            symbol=args.symbol,
            symbols_file=args.symbols_file,
            track_experiment=args.track_experiment,
            output_dir=args.output,
        )
    except StrategyLoadError as exc:
        log.error("backtest.strategy_load_failed", error=str(exc))
        return 1
    payload = {
        "metrics": run.result.metrics,
        "trade_count": len(run.result.trades),
        "experiment_id": run.experiment_id,
    }
    log.info("backtest.complete", metrics=run.result.metrics, trades=len(run.result.trades))
    if args.output and args.track_experiment:
        payload["artifacts_dir"] = str(args.output)
    emit_output(render_payload(payload, output_format=args.output_format), output_path=args.metrics_output)
    return 0


def _cmd_scan(args: argparse.Namespace) -> int:
    log = get_logger("athena.cli.scan")
    client = _client(args)
    try:
        payload = client.scan_dict(
            args.strategy,
            _parse_date(args.as_of),
            symbol=args.symbol,
            symbols_file=args.symbols_file,
        )
    except StrategyLoadError as exc:
        log.error("scan.strategy_load_failed", error=str(exc))
        return 1
    log.info("scan.complete", candidates=len(payload.get("candidates", [])))
    emit_output(
        render_payload(payload, output_format=args.output_format),
        output_path=getattr(args, "output", None),
    )
    return 0


def _cmd_walk_forward(args: argparse.Namespace) -> int:
    log = get_logger("athena.cli.walk_forward")
    client = _client(args)
    try:
        payload = client.walk_forward_dict(
            args.strategy,
            _parse_date(args.start),
            _parse_date(args.end),
            symbol=args.symbol,
            symbols_file=args.symbols_file,
        )
    except StrategyLoadError as exc:
        log.error("walk_forward.strategy_load_failed", error=str(exc))
        return 1
    log.info("walk_forward.complete", folds=payload.get("fold_count", 0))
    emit_output(
        render_payload(payload, output_format=args.output_format),
        output_path=getattr(args, "output", None),
    )
    return 0


def _cmd_optimize(args: argparse.Namespace) -> int:
    log = get_logger("athena.cli.optimize")
    client = _client(args)
    try:
        payload = client.optimize_dict(
            args.strategy,
            _parse_date(args.start),
            _parse_date(args.end),
            symbol=args.symbol,
            symbols_file=args.symbols_file,
        )
    except StrategyLoadError as exc:
        log.error("optimize.strategy_load_failed", error=str(exc))
        return 1
    log.info("optimize.complete", trials=payload.get("trial_count", 0))
    emit_output(
        render_payload(payload, output_format=args.output_format),
        output_path=getattr(args, "output", None),
    )
    return 0


def _cmd_compare_experiments(args: argparse.Namespace) -> int:
    log = get_logger("athena.cli.compare")
    client = _client(args)
    try:
        if args.latest:
            comparison = client.compare_experiments(latest=args.latest)
        else:
            comparison = client.compare_experiments(list(args.experiment_id))
    except (FileNotFoundError, ValueError) as exc:
        log.error("compare.failed", error=str(exc))
        return 1
    text = render_payload(comparison, output_format=args.output_format)
    emit_output(text, output_path=getattr(args, "output", None))
    log.info("compare.complete", count=len(comparison["experiments"]))
    return 0


def _add_global_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--config", type=Path, help="YAML config path")
    parser.add_argument("--profile", help="Named config profile from YAML")
    parser.add_argument(
        "--output-format",
        choices=["json", "table"],
        default="json",
        help="Structured command output format (default: json)",
    )


def _add_symbol_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--symbol", help="Single symbol override")
    parser.add_argument("--symbols-file", type=Path, help="CSV with symbol column")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="athena",
        description="Athena quantitative research CLI",
        epilog="Use --profile to apply named overlays from config YAML (see `athena profiles`).",
    )
    parser.add_argument("--version", action="version", version=f"athena {__version__}")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable debug logging")
    _add_global_args(parser)
    subparsers = parser.add_subparsers(dest="command", required=False)

    subparsers.add_parser("health", help="Verify installation")
    subparsers.add_parser("profiles", help="List config profiles in YAML")

    ingest = subparsers.add_parser("ingest", help="Ingest OHLCV via yfinance → Parquet")
    ingest.add_argument("--symbol", help="Single symbol")
    ingest.add_argument("--symbols-file", type=Path, help="CSV with symbol column")
    ingest.add_argument("--start", required=True)
    ingest.add_argument("--end", required=True)
    ingest.add_argument("--output", help="Write JSON summary to path")

    backtest = subparsers.add_parser("backtest", help="Run configuration-driven backtest")
    backtest.add_argument("--strategy", type=Path, required=True)
    backtest.add_argument("--start", required=True)
    backtest.add_argument("--end", required=True)
    _add_symbol_args(backtest)
    backtest.add_argument("--output", type=Path, help="Directory for equity curve and trades")
    backtest.add_argument("--metrics-output", help="Optional JSON metrics summary path")
    backtest.add_argument("--track-experiment", action="store_true")

    scan = subparsers.add_parser("scan", help="Daily universe scanner")
    scan.add_argument("--strategy", type=Path, required=True)
    scan.add_argument("--as-of", required=True)
    _add_symbol_args(scan)
    scan.add_argument("--output", help="JSON output path")

    wf = subparsers.add_parser("walk-forward", help="Walk-forward validation")
    wf.add_argument("--strategy", type=Path, required=True)
    wf.add_argument("--start", required=True)
    wf.add_argument("--end", required=True)
    _add_symbol_args(wf)
    wf.add_argument("--output", help="JSON output path")

    opt = subparsers.add_parser("optimize", help="Parameter search on walk-forward folds")
    opt.add_argument("--strategy", type=Path, required=True)
    opt.add_argument("--start", required=True)
    opt.add_argument("--end", required=True)
    _add_symbol_args(opt)
    opt.add_argument("--output", help="JSON output path")

    compare = subparsers.add_parser("compare-experiments", help="Compare persisted experiments")
    compare.add_argument("experiment_id", nargs="*", help="Experiment IDs")
    compare.add_argument("--latest", type=int, help="Compare N most recent experiments")
    compare.add_argument("--output", help="Output path")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    configure_logging(level=10 if args.verbose else 20)

    handlers = {
        "health": _cmd_health,
        "profiles": _cmd_profiles,
        "ingest": _cmd_ingest,
        "backtest": _cmd_backtest,
        "scan": _cmd_scan,
        "walk-forward": _cmd_walk_forward,
        "optimize": _cmd_optimize,
        "compare-experiments": _cmd_compare_experiments,
    }
    handler = handlers.get(args.command)
    if handler is None:
        parser.print_help()
        return 0 if args.command is None else 1
    return handler(args)


if __name__ == "__main__":
    sys.exit(main())
