#!/usr/bin/env python3
"""Generate module.yaml stubs from component metadata YAML."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml

ATHENA_ROOT = Path(__file__).resolve().parents[1]
COMPONENTS_DIR = ATHENA_ROOT / "athena-spec" / "metadata" / "components"
DEFAULT_OUTPUT_DIR = ATHENA_ROOT / "athena-spec" / "metadata" / "generated" / "manifests"


def _component_to_manifest(data: dict[str, Any]) -> dict[str, Any]:
    slug = str(data.get("name", "component")).lower().replace(" ", "-")
    return {
        "name": f"athena-{slug}",
        "owner": data.get("owner", "platform-team"),
        "bounded_context": data.get("capability", "foundation").lower().replace(" ", "-"),
        "version": "0.1.0",
        "description": data.get("description", ""),
        "dependencies": {"packages": list(data.get("dependencies", []) or [])},
        "events": {"publishes": [], "consumes": []},
        "interfaces": [],
        "api": {"modules": list(data.get("apis", []) or []), "openapi": None},
        "database": {"schemas": []},
        "quality": {"fitness_tests": True, "min_coverage": 0.0},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate module manifests from metadata")
    parser.add_argument("--components-dir", type=Path, default=COMPONENTS_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    for path in sorted(args.components_dir.glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            continue
        manifest = _component_to_manifest(data)
        out = args.output_dir / f"{manifest['name']}.module.yaml"
        out.write_text(
            "# GENERATED — DO NOT EDIT\n" + yaml.safe_dump(manifest, sort_keys=False),
            encoding="utf-8",
        )
        count += 1
    print(f"Generated {count} manifest stubs in {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
