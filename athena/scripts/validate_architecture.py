#!/usr/bin/env python3
"""Architecture validator — dependency rules and module manifests (M1 ATH-013)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ATHENA_ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    check = ATHENA_ROOT / "scripts" / "check_dependencies.py"
    result = subprocess.run([sys.executable, str(check)], cwd=ATHENA_ROOT, check=False)
    if result.returncode != 0:
        return result.returncode

    manifests = list(ATHENA_ROOT.glob("athena-*/module.yaml"))
    if not manifests:
        print("WARN: no module.yaml manifests found")
        return 1
    print(f"Architecture OK — {len(manifests)} module manifests, dependency rules pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
