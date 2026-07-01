#!/usr/bin/env python3
"""Read rich module.yaml manifests and print dependencies, events, APIs, and graph snippet."""

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


def _packages(data: dict[str, Any]) -> list[str]:
    deps = data.get("dependencies", {})
    if isinstance(deps, dict):
        return list(deps.get("packages", []) or [])
    if isinstance(deps, list):
        return list(deps)
    return []


def _events(data: dict[str, Any], key: str) -> list[str]:
    events = data.get("events", {})
    if isinstance(events, dict):
        return list(events.get(key, []) or [])
    legacy = "publishes_events" if key == "publishes" else "consumes_events"
    return list(data.get(legacy, []) or [])


def _api_modules(data: dict[str, Any]) -> list[str]:
    api = data.get("api", {})
    if isinstance(api, dict):
        return list(api.get("modules", []) or [])
    return list(data.get("public_apis", []) or [])


def format_manifest(data: dict[str, Any], path: Path) -> str:
    name = data.get("name", path.parent.name)
    lines = [
        f"## {name} (v{data.get('version', '?')})",
        f"Owner: {data.get('owner', 'unknown')}",
        f"Bounded context: {data.get('bounded_context', data.get('layer', 'unknown'))}",
        f"Description: {data.get('description', '')}",
        "",
        "**Dependencies:** " + ", ".join(_packages(data) or ["none"]),
        "**Publishes:** " + ", ".join(_events(data, "publishes") or ["none"]),
        "**Consumes:** " + ", ".join(_events(data, "consumes") or ["none"]),
        "**Interfaces:** " + ", ".join(data.get("interfaces", []) or ["none"]),
        "**APIs:** " + ", ".join(_api_modules(data) or ["none"]),
    ]
    quality = data.get("quality", {})
    if isinstance(quality, dict) and quality.get("fitness_tests"):
        lines.append("**Fitness tests:** enabled")
    return "\n".join(lines)


def dependency_graph_snippet(manifests: list[tuple[Path, dict[str, Any]]]) -> str:
    lines = ["```mermaid", "flowchart BT"]
    for path, data in manifests:
        pkg = str(data.get("name", path.parent.name))
        for dep in _packages(data):
            lines.append(f"    {dep.replace('-', '_')} --> {pkg.replace('-', '_')}")
    lines.append("```")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect Athena module manifests")
    parser.add_argument("--root", type=Path, default=ATHENA_ROOT)
    parser.add_argument("--json", action="store_true", help="Emit YAML list")
    parser.add_argument("--graph", action="store_true", help="Emit Mermaid dependency snippet")
    args = parser.parse_args()

    paths = find_manifests(args.root)
    manifests = [(p, load_manifest(p)) for p in paths]

    if args.json:
        print(yaml.safe_dump([m for _, m in manifests], sort_keys=False))
        return 0

    if args.graph:
        print(dependency_graph_snippet(manifests))
        return 0

    for path, data in manifests:
        print(format_manifest(data, path))
        print()
    print(f"Total modules: {len(manifests)}")
    print()
    print("## Dependency graph snippet")
    print()
    print(dependency_graph_snippet(manifests))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
