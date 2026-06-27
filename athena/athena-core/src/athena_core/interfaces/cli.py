"""CLI stub — full CLI ships in athena-cli (future)."""

from __future__ import annotations

import argparse
import sys

from athena_core import __version__
from athena_core.infrastructure.logging import configure_logging, get_logger


def main(argv: list[str] | None = None) -> int:
    """Entry point stub for Athena core CLI."""
    parser = argparse.ArgumentParser(prog="athena-core", description="Athena core utilities")
    parser.add_argument("--version", action="version", version=f"athena-core {__version__}")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable debug logging")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("health", help="Verify installation")

    args = parser.parse_args(argv)
    configure_logging(level=10 if args.verbose else 20)
    log = get_logger("athena_core.cli")

    if args.command == "health":
        log.info("athena_core.health_ok", version=__version__)
        return 0

    parser.print_help()
    return 0 if args.command is None else 1


if __name__ == "__main__":
    sys.exit(main())
