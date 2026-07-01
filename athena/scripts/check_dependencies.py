#!/usr/bin/env python3
"""Enforce Athena package dependency rules — see ATHENA/DEPENDENCY-RULES.md."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ATHENA_ROOT = Path(__file__).resolve().parents[1]

_BOUNDED = {
    "athena-data",
    "athena-indicators",
    "athena-patterns",
    "athena-strategies",
    "athena-risk",
    "athena-portfolio",
    "athena-execution",
}

_FOUNDATION = {
    "athena-common": set(),
    "athena-os": set(),
    "athena-domain": {"athena-common", "athena-os"},
    "athena-core": {"athena-os", "athena-common"},
}

_BOUNDED_ALLOWED = {"athena-os", "athena-common", "athena-core"}

_CORE_FACADE = {
    "athena-core-runtime",
    "athena-core-events",
    "athena-core-engine",
    "athena-core-metadata",
}

_EXTENSION = {
    "athena-metadata",
    "athena-observability",
    "athena-market",
    "athena-brokers",
}

# package_name -> allowed athena-* dependency package names
ALLOWED: dict[str, set[str]] = {
    **_FOUNDATION,
    **{pkg: _BOUNDED_ALLOWED for pkg in _BOUNDED},
    **{pkg: _BOUNDED_ALLOWED for pkg in _CORE_FACADE},
    **{pkg: _BOUNDED_ALLOWED for pkg in _EXTENSION},
    "athena-math": {"athena-os", "athena-common", "athena-core"},
    "athena-research": {"athena-os", "athena-common", "athena-core"},
    "athena-platform": {
        "athena-os",
        "athena-common",
        "athena-core",
        "athena-domain",
        *_BOUNDED,
    },
    "athena-sdk": {"athena-os", "athena-core"},
    "athena-cli": {"athena-os", "athena-core", "athena-sdk", "athena-ai"},
    "athena-ai": {"athena-os", "athena-core", "athena-sdk"},
    "athena-dashboard": {"athena-os", "athena-core", "athena-sdk"},
    "athena-testing": {"athena-os", "athena-core", "athena-common"},
}

ATHENA_PKG_PATTERN = re.compile(r"^athena[-_]")
DEP_PATTERN = re.compile(r"^[\s\"]*([a-zA-Z0-9_-]+)")


def parse_dependencies(pyproject: Path) -> list[str]:
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
            match = DEP_PATTERN.match(line.strip().strip(",").strip('"'))
            if match:
                raw = match.group(1)
                name = raw.split("@")[0].strip()
                deps.append(name)
    return deps


def athena_packages(deps: list[str]) -> list[str]:
    return [dep for dep in deps if ATHENA_PKG_PATTERN.match(dep)]


def check_package(package_dir: Path) -> list[str]:
    errors: list[str] = []
    pyproject = package_dir / "pyproject.toml"
    if not pyproject.exists():
        return errors
    pkg_name = package_dir.name
    allowed = ALLOWED.get(pkg_name)
    if allowed is None:
        return errors
    for dep in athena_packages(parse_dependencies(pyproject)):
        if dep not in allowed:
            errors.append(
                f"{pkg_name}: disallowed athena dependency '{dep}' "
                f"(allowed: {sorted(allowed) or ['none']})"
            )
    return errors


def main() -> int:
    all_errors: list[str] = []
    for pkg_dir in sorted(ATHENA_ROOT.glob("athena-*")):
        if pkg_dir.is_dir():
            all_errors.extend(check_package(pkg_dir))
    if all_errors:
        print("Dependency rule violations:")
        for err in all_errors:
            print(f"  - {err}")
        return 1
    print("All dependency rules satisfied.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
