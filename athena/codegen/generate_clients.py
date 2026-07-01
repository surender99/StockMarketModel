#!/usr/bin/env python3
"""Stub: generate SDK client stubs from OpenAPI definitions."""

from __future__ import annotations

import argparse
from pathlib import Path

ATHENA_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ATHENA_ROOT / "athena-sdk" / "src" / "athena_sdk" / "clients_generated.py"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate SDK clients (stub)")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    stub = '''# GENERATED — DO NOT EDIT
"""SDK client stubs — regenerate via make codegen."""

from __future__ import annotations


class GeneratedClientStub:
    """Placeholder until OpenAPI-driven client generation is wired."""

    API_VERSION = "0.1.0"


__all__ = ["GeneratedClientStub"]
'''
    args.output.write_text(stub, encoding="utf-8")
    print(f"Wrote client stub to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
