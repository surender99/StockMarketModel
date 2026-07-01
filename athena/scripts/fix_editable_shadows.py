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
    "athena_core_runtime",
    "athena_core_events",
    "athena_core_engine",
    "athena_core_metadata",
    "athena_metadata",
    "athena_observability",
    "athena_market",
    "athena_brokers",
)


def _package_src(repo: Path, name: str) -> Path | None:
    folder = "athena-" + name.removeprefix("athena_").replace("_", "-")
    if name == "athena_core":
        folder = "athena-core"
    src = repo / folder / "src"
    return src if src.is_dir() else None


def _is_corrupted_shadow(shadow: Path) -> bool:
    if not shadow.is_dir():
        return False
    for child in shadow.rglob("*"):
        if child.is_dir() and child.name.startswith("~"):
            return True
    return False


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    site_packages = repo / "athena-core" / ".venv" / "Lib" / "site-packages"
    if not site_packages.is_dir():
        return 0

    removed: list[str] = []
    for name in NAMES:
        shadow = site_packages / name
        pth = site_packages / f"_editable_impl_{name}.pth"
        src = _package_src(repo, name)
        if not shadow.is_dir():
            continue
        stale = pth.is_file() or _is_corrupted_shadow(shadow) or src is not None
        if not stale:
            continue
        shutil.rmtree(shadow, ignore_errors=True)
        removed.append(name)
        if src is not None and not pth.is_file():
            pth.write_text(str(src.resolve()) + "\n", encoding="utf-8")

    if removed:
        print("Removed stale editable shadows:", ", ".join(removed))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
