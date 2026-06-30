#!/usr/bin/env python3
"""Stub: generate DTO dataclasses from interface specs."""

from __future__ import annotations

import argparse


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate DTOs (stub)")
    parser.add_argument("--spec-dir", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    print(f"DTO codegen stub — spec={args.spec_dir} output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
