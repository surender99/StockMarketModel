"""Production startup and CLI entry point."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from athena_platform.features import PlatformFeatures
from athena_platform.runtime import assemble_runtime


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Athena platform runtime")
    parser.add_argument("--config", type=Path, help="Path to YAML configuration file")
    parser.add_argument("--json-logs", action="store_true", help="Emit structured JSON logs")
    parser.add_argument(
        "--list-features",
        action="store_true",
        help="Print enabled feature modules and exit",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Bootstrap production runtime (default: print status and exit 0)."""
    args = build_parser().parse_args(argv)
    features = PlatformFeatures()
    if args.list_features:
        for name in features.enabled_modules():
            print(name)
        return 0
    runtime = assemble_runtime(
        config_path=args.config,
        json_logs=args.json_logs,
        features=features,
    )
    enabled = ", ".join(runtime.features.enabled_modules())
    print(f"Athena platform ready — modules: {enabled}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
