"""Remove stale Hatch editable shadow packages from the active venv."""

from __future__ import annotations

import shutil
from pathlib import Path

NAMES = (
    "athena_core",
    "athena_os",
    "athena_common",
    "athena_domain",
    "athena_data",
    "athena_indicators",
    "athena_patterns",
    "athena_strategies",
    "athena_risk",
    "athena_portfolio",
    "athena_execution",
    "athena_math",
    "athena_research",
    "athena_platform",
    "athena_sdk",
    "athena_ai",
    "athena_cli",
    "athena_dashboard",
    "athena_testing",
)


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    site_packages = repo / "athena-core" / ".venv" / "Lib" / "site-packages"
    if not site_packages.is_dir():
        return 0

    removed: list[str] = []
    for name in NAMES:
        shadow = site_packages / name
        pth = site_packages / f"_editable_impl_{name}.pth"
        if shadow.is_dir() and pth.is_file():
            shutil.rmtree(shadow, ignore_errors=True)
            removed.append(name)

    if removed:
        print("Removed stale editable shadows:", ", ".join(removed))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
