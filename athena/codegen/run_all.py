#!/usr/bin/env python3
"""Run all Athena code generators."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

CODEGEN_DIR = Path(__file__).resolve().parent
PY = sys.executable

GENERATORS = [
    "generate_events.py",
    "generate_dtos.py",
    "generate_openapi.py",
    "generate_proto.py",
    "generate_clients.py",
    "generate_docs.py",
    "generate_manifests.py",
]


def main() -> int:
    rc = 0
    for name in GENERATORS:
        script = CODEGEN_DIR / name
        print(f"==> {name}")
        result = subprocess.run([PY, str(script)], check=False)
        if result.returncode != 0:
            rc = result.returncode
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
