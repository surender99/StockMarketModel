"""Athena core CLI — REQ-DATA-INGEST-001."""

from __future__ import annotations

import argparse
import csv
import sys
from datetime import date
from pathlib import Path

import yaml

from athena_core import __version__
from athena_core.application.config import AthenaConfig, CalendarConfig, DataIngestConfig, FeatureStoreConfig
from athena_core.application.errors import IngestError
from athena_core.application.ingest_ohlcv import IngestOHLCVUseCase
from athena_core.infrastructure.logging import configure_logging, get_logger
from athena_core.infrastructure.parquet_ohlcv_store import ParquetOHLCVStore


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

    args = parser.parse_args(argv)
    configure_logging(level=10 if args.verbose else 20)
    log = get_logger("athena_core.cli")

    if args.command == "health":
        log.info("athena_core.health_ok", version=__version__)
        return 0
    if args.command == "ingest":
        return _cmd_ingest(args)

    parser.print_help()
    return 0 if args.command is None else 1


if __name__ == "__main__":
    sys.exit(main())
