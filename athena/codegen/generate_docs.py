#!/usr/bin/env python3
"""Generate markdown module index from rich module.yaml manifests."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml

ATHENA_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ATHENA_ROOT / "athena-spec" / "metadata" / "generated" / "MODULE-INDEX.md"


def _packages(data: dict[str, Any]) -> list[str]:
    deps = data.get("dependencies", {})
    if isinstance(deps, dict):
        return list(deps.get("packages", []) or [])
    return list(deps or [])


def render_index(manifests: list[tuple[str, dict[str, Any]]]) -> str:
    lines = [
        "# GENERATED — DO NOT EDIT",
        "",
        "> Regenerate: `make codegen`",
        "",
        "# Athena Module Index",
        "",
        "| Package | Owner | Context | Version | Dependencies |",
        "|---------|-------|---------|---------|--------------|",
    ]
    for name, data in sorted(manifests, key=lambda x: x[0]):
        deps = ", ".join(f"`{d}`" for d in _packages(data)) or "—"
        lines.append(
            f"| `{name}` | {data.get('owner', '?')} | "
            f"{data.get('bounded_context', '?')} | {data.get('version', '?')} | {deps} |"
        )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate module index from manifests")
    parser.add_argument("--root", type=Path, default=ATHENA_ROOT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    manifests: list[tuple[str, dict[str, Any]]] = []
    for path in sorted(args.root.glob("athena-*/module.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            manifests.append((str(data.get("name", path.parent.name)), data))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_index(manifests), encoding="utf-8")
    print(f"Wrote module index ({len(manifests)} packages) to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
