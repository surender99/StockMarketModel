"""Ensure milestone tests resolve athena-core from source tree."""

from __future__ import annotations

import sys
from pathlib import Path

_CORE_SRC = Path(__file__).resolve().parents[2] / "athena-core" / "src"
if _CORE_SRC.is_dir():
    path = str(_CORE_SRC)
    if path not in sys.path:
        sys.path.insert(0, path)
