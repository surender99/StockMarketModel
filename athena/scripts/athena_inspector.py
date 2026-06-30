#!/usr/bin/env python3
"""Read module.yaml manifests and print dependencies, events, and APIs."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml

ATHENA_ROOT = Path(__file__).resolve().parents[1]


def find_manifests(root: Path) -> list[Path]:
    return sorted(root.glob("athena-*/module.yaml"))


def load_manifest(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def format_manifest(data: dict[str, Any], path: Path) -> str:
    lines = [
        f"## {data.get('name', path.parent.name)} (v{data.get('version', '?')})",
        f"Layer: {data.get('layer', 'unknown')}",
        f"Description: {data.get('description', '')}",
        "",
        "**Dependencies:** " + ", ".join(data.get("dependencies", []) or ["none"]),
        "**Publishes:** " + ", ".join(data.get("publishes_events", []) or ["none"]),
        "**Consumes:** " + ", ".join(data.get("consumes_events", []) or ["none"]),
        "**APIs:** " + ", ".join(data.get("public_apis", []) or ["none"]),
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect Athena module manifests")
    parser.add_argument("--root", type=Path, default=ATHENA_ROOT)
    parser.add_argument("--json", action="store_true", help="Emit YAML list")
    args = parser.parse_args()

    manifests = [load_manifest(p) for p in find_manifests(args.root)]
    if args.json:
        print(yaml.safe_dump(manifests, sort_keys=False))
        return 0

    for path, data in zip(find_manifests(args.root), manifests, strict=True):
        print(format_manifest(data, path))
        print()
    print(f"Total modules: {len(manifests)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
