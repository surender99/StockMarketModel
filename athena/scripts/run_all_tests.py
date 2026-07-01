#!/usr/bin/env python3
"""Run pytest across Athena packages and report total passed count."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
_VENV_BIN = REPO / "athena-core" / ".venv" / ("Scripts" if sys.platform == "win32" else "bin")
PY = _VENV_BIN / ("python.exe" if sys.platform == "win32" else "python")

PACKAGES = [
    "athena-os",
    "athena-common",
    "athena-domain",
    "athena-data",
    "athena-indicators",
    "athena-patterns",
    "athena-strategies",
    "athena-risk",
    "athena-portfolio",
    "athena-execution",
    "athena-math",
    "athena-research",
    "athena-core-runtime",
    "athena-core-events",
    "athena-core-engine",
    "athena-core-metadata",
    "athena-metadata",
    "athena-observability",
    "athena-market",
    "athena-brokers",
    "athena-platform",
    "athena-sdk",
    "athena-ai",
    "athena-cli",
    "athena-dashboard",
    "athena-core",
    "athena-testing",
]


def main() -> int:
    subprocess.run([str(PY), str(REPO / "scripts" / "fix_editable_shadows.py")], check=False, cwd=REPO)
    total = 0
    failed = 0
    for pkg in PACKAGES:
        py = PY
        result = subprocess.run(
            [str(py), "-m", "pytest", "-q"],
            cwd=REPO / pkg,
            capture_output=True,
            text=True,
            check=False,
        )
        out = result.stdout + result.stderr
        m = re.search(r"(\d+) passed", out)
        if m:
            total += int(m.group(1))
        if result.returncode != 0:
            failed += 1
            print(f"FAIL {pkg}: {out[-500:]}")
        else:
            print(f"OK   {pkg}: {m.group(0) if m else '0 passed'}")
    print(f"TOTAL_PASSED={total} FAILED_PACKAGES={failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
