#!/usr/bin/env python3
"""Generate markdown documentation from component metadata YAML (stub + examples)."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml

ATHENA_ROOT = Path(__file__).resolve().parents[1]
METADATA_DIR = ATHENA_ROOT / "athena-spec" / "metadata" / "components"
OUTPUT_DIR = ATHENA_ROOT / "athena-spec" / "metadata" / "generated"


def render_component(data: dict[str, Any]) -> str:
    lines = [
        f"# {data.get('name', 'Component')}",
        "",
        f"**Capability:** {data.get('capability', 'N/A')}",
        f"**Owner:** {data.get('owner', 'N/A')}",
        f"**Status:** {data.get('status', 'draft')}",
        "",
        data.get("description", ""),
        "",
    ]
    apis = data.get("apis", [])
    if apis:
        lines.append("## APIs")
        for api in apis:
            lines.append(f"- `{api}`")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--metadata-dir", type=Path, default=METADATA_DIR)
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    for path in sorted(args.metadata_dir.glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            continue
        out = args.output_dir / f"{path.stem}.md"
        out.write_text(render_component(data), encoding="utf-8")
        count += 1
    print(f"Generated {count} component docs in {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
