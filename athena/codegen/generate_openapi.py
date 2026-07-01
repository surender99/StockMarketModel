#!/usr/bin/env python3
"""Stub: generate OpenAPI spec from module api definitions."""

from __future__ import annotations

import argparse
from pathlib import Path

ATHENA_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ATHENA_ROOT / "athena-spec" / "metadata" / "generated" / "openapi-stub.yaml"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate OpenAPI (stub)")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    stub = (
        "# GENERATED — DO NOT EDIT\n"
        "openapi: 3.1.0\n"
        "info:\n"
        "  title: Athena API (stub)\n"
        "  version: 0.1.0\n"
        "paths: {}\n"
    )
    args.output.write_text(stub, encoding="utf-8")
    print(f"Wrote OpenAPI stub to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
