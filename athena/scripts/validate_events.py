#!/usr/bin/env python3
"""Event catalog validator — YAML registry schema checks (M1 ATH-015)."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ATHENA_ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ATHENA_ROOT / "athena-spec" / "events" / "registry"
REQUIRED = {"name", "version", "publisher", "payload"}


def validate_event(path: Path) -> list[str]:
    errors: list[str] = []
    data: Any = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        return [f"{path.name}: root must be a mapping"]
    missing = REQUIRED - set(data.keys())
    if missing:
        errors.append(f"{path.name}: missing fields {sorted(missing)}")
    if "name" in data and not str(data["name"])[0].isupper():
        errors.append(f"{path.name}: name must be PascalCase")
    return errors


def main() -> int:
    if not REGISTRY.is_dir():
        print(f"ERROR: registry not found: {REGISTRY}")
        return 1
    errors: list[str] = []
    events = sorted(REGISTRY.glob("*.event.yaml"))
    if not events:
        print("ERROR: no *.event.yaml files in registry")
        return 1
    for path in events:
        errors.extend(validate_event(path))
    if errors:
        for err in errors:
            print(f"FAIL: {err}")
        return 1
    print(f"Events OK — {len(events)} event definitions validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
