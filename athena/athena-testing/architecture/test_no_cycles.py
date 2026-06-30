"""Detect circular package dependencies via pyproject.toml."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ATHENA_ROOT = Path(__file__).resolve().parents[2]
CHECK_SCRIPT = ATHENA_ROOT / "scripts" / "check_dependencies.py"

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


def build_graph(root: Path) -> dict[str, list[str]]:
    graph: dict[str, list[str]] = {}
    for pkg_dir in sorted(root.glob("athena-*")):
        py = pkg_dir / "pyproject.toml"
        if py.exists():
            graph[pkg_dir.name] = parse_deps(py)
    return graph


def find_cycles(graph: dict[str, list[str]]) -> list[list[str]]:
    cycles: list[list[str]] = []
    visited: set[str] = set()
    stack: list[str] = []

    def dfs(node: str) -> None:
        if node in stack:
            idx = stack.index(node)
            cycles.append(stack[idx:] + [node])
            return
        if node in visited:
            return
        visited.add(node)
        stack.append(node)
        for dep in graph.get(node, []):
            dep_key = dep  # already package dir names
            # map athena_core style to dir? deps use athena-core with hyphen
            dep_dir = dep.replace("_", "-")
            if dep_dir in graph or dep in graph:
                dfs(dep_dir if dep_dir in graph else dep)
        stack.pop()

    for node in graph:
        dfs(node)
    return cycles


def test_no_dependency_cycles() -> None:
    graph = build_graph(ATHENA_ROOT)
    cycles = find_cycles(graph)
    assert not cycles, f"dependency cycles detected: {cycles}"


def test_check_dependencies_script_passes() -> None:
    if not CHECK_SCRIPT.exists():
        return
    result = subprocess.run(
        [sys.executable, str(CHECK_SCRIPT)],
        cwd=ATHENA_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
