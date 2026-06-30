#!/usr/bin/env python3
"""CLI wrapper — delegates to athena.codegen.generate_events."""

from __future__ import annotations

import runpy
import sys
from pathlib import Path

if __name__ == "__main__":
    script = Path(__file__).resolve().parents[1] / "codegen" / "generate_events.py"
    sys.argv[0] = str(script)
    runpy.run_path(str(script), run_name="__main__")
