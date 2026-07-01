"""Enforce forbidden cross-bounded-context imports — build breaker."""

from __future__ import annotations

import ast
from pathlib import Path

ATHENA_ROOT = Path(__file__).resolve().parents[2]

# module prefix -> forbidden import prefixes
FORBIDDEN_IMPORTS: dict[str, set[str]] = {
    "athena_indicators": {"athena_portfolio", "athena_execution", "athena_strategies"},
    "athena_patterns": {"athena_portfolio", "athena_execution"},
    "athena_data": {"athena_strategies", "athena_portfolio"},
    "athena_research": {
        "athena_execution",
        "athena_platform",
    },
}

PACKAGE_SRC = {
    "athena-indicators": "athena_indicators",
    "athena-patterns": "athena_patterns",
    "athena-data": "athena_data",
    "athena-strategies": "athena_strategies",
    "athena-risk": "athena_risk",
    "athena-portfolio": "athena_portfolio",
    "athena-execution": "athena_execution",
    "athena-research": "athena_research",
}


def _imports_in_file(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    found: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                found.add(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            found.add(node.module)
    return found


def _violates(forbidden: str, imp: str) -> bool:
    return imp == forbidden or imp.startswith(forbidden + ".")


def test_forbidden_bounded_context_imports() -> None:
    violations: list[str] = []
    for pkg_dir, module_prefix in PACKAGE_SRC.items():
        forbidden = FORBIDDEN_IMPORTS.get(module_prefix, set())
        if not forbidden:
            continue
        src = ATHENA_ROOT / pkg_dir / "src" / module_prefix
        if not src.exists():
            continue
        for py_file in src.rglob("*.py"):
            imports = _imports_in_file(py_file)
            for imp in imports:
                for bad in forbidden:
                    if _violates(bad, imp):
                        violations.append(
                            f"{py_file.relative_to(ATHENA_ROOT)} imports forbidden {bad} via {imp}"
                        )
    assert not violations, "\n".join(violations)
