#!/usr/bin/env python3
"""Generate BUILD-GRAPH.md and optional Mermaid from package dependencies."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

ATHENA_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_MD = ATHENA_ROOT / "athena-spec" / "ATHENA" / "Dependency-Graph" / "BUILD-GRAPH.md"
OUTPUT_DOT = ATHENA_ROOT / "athena-spec" / "ATHENA" / "Dependency-Graph" / "BUILD-GRAPH.dot"

DEP_PATTERN = re.compile(r"^[\s\"]*([a-zA-Z0-9_-]+)")
ATHENA_PKG = re.compile(r"^athena[-_]")


def parse_deps(pyproject: Path) -> list[str]:
    text = pyproject.read_text(encoding="utf-8")
    deps: list[str] = []
    in_deps = False
    for line in text.splitlines():
        if line.strip().startswith("dependencies = ["):
            in_deps = True
            continue
        if in_deps:
            if line.strip() == "]":
                break
            m = DEP_PATTERN.match(line.strip().strip(",").strip('"'))
            if m:
                name = m.group(1).split("@")[0].strip()
                if ATHENA_PKG.match(name):
                    deps.append(name)
    return deps


def collect_graph(root: Path) -> dict[str, list[str]]:
    graph: dict[str, list[str]] = {}
    for pkg_dir in sorted(root.glob("athena-*")):
        pyproject = pkg_dir / "pyproject.toml"
        if pyproject.exists():
            graph[pkg_dir.name] = parse_deps(pyproject)
    return graph


def render_mermaid(graph: dict[str, list[str]]) -> str:
    lines = ["```mermaid", "flowchart BT"]
    for pkg, deps in sorted(graph.items()):
        for dep in deps:
            lines.append(f"    {dep.replace('-', '_')} --> {pkg.replace('-', '_')}")
    lines.append("```")
    return "\n".join(lines)


def render_dot(graph: dict[str, list[str]]) -> str:
    lines = ["digraph athena {", '  rankdir=BT;']
    for pkg, deps in sorted(graph.items()):
        for dep in deps:
            lines.append(f'  "{dep}" -> "{pkg}";')
    lines.append("}")
    return "\n".join(lines)


def render_md(graph: dict[str, list[str]]) -> str:
    lines = [
        "# Athena Build Dependency Graph",
        "",
        "> AUTO-GENERATED — run `make graph` or `python athena/scripts/generate_dependency_graph.py`",
        "",
        "## Package Dependencies",
        "",
        "| Package | Depends on |",
        "|---------|------------|",
    ]
    for pkg, deps in sorted(graph.items()):
        lines.append(f"| `{pkg}` | {', '.join(f'`{d}`' for d in deps) or '—'} |")
    lines.extend(["", "## Mermaid", "", render_mermaid(graph), ""])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ATHENA_ROOT)
    parser.add_argument("--dot", action="store_true")
    args = parser.parse_args()

    graph = collect_graph(args.root)
    OUTPUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_MD.write_text(render_md(graph), encoding="utf-8")
    if args.dot:
        OUTPUT_DOT.write_text(render_dot(graph), encoding="utf-8")
    print(f"Wrote {OUTPUT_MD} ({len(graph)} packages)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
