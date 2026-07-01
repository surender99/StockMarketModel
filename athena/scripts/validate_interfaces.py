#!/usr/bin/env python3
"""Interface catalog validator — ensures catalog docs exist (M1 ATH-016)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

SPEC = Path(__file__).resolve().parents[1] / "athena-spec"
CATALOG = SPEC / "interfaces" / "INTERFACE-CATALOG.md"
TABLE_ROW = re.compile(r"^\|\s*\d+\s*\|", re.MULTILINE)
HEADING = re.compile(r"^###\s+`([^`]+)`", re.MULTILINE)


def main() -> int:
    if not CATALOG.is_file():
        print(f"ERROR: missing {CATALOG}")
        return 1
    text = CATALOG.read_text(encoding="utf-8")
    entries = TABLE_ROW.findall(text) or HEADING.findall(text)
    if len(entries) < 5:
        print(f"FAIL: expected >=5 interface entries, found {len(entries)}")
        return 1
    print(f"Interfaces OK — {len(entries)} catalog entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
