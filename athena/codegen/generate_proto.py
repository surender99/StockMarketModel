#!/usr/bin/env python3
"""Stub: generate protobuf definitions from interface catalog."""

from __future__ import annotations

import argparse
from pathlib import Path

ATHENA_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ATHENA_ROOT / "athena-spec" / "metadata" / "generated" / "athena.proto"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate protobuf (stub)")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    stub = (
        "// GENERATED — DO NOT EDIT\n"
        "syntax = \"proto3\";\n"
        "package athena.v1;\n"
        "// Stub — wire from interface catalog in future phase\n"
    )
    args.output.write_text(stub, encoding="utf-8")
    print(f"Wrote proto stub to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
