#!/usr/bin/env python3
"""Fix hatchling src-layout package discovery in all athena pyproject.toml files."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

for path in ROOT.glob("athena-*/pyproject.toml"):
    text = path.read_text(encoding="utf-8")
    match = re.search(r'packages = \["src/(athena_\w+)"\]', text)
    if not match or "[tool.hatch.build.targets.wheel.sources]" in text:
        continue
    pkg = match.group(1)
    old = f'packages = ["src/{pkg}"]'
    new = (
        f'packages = ["{pkg}"]\n\n'
        f'[tool.hatch.build.targets.wheel.sources]\n'
        f'"src" = ""'
    )
    path.write_text(text.replace(old, new), encoding="utf-8")
    print(f"fixed {path.name} in {path.parent.name}")
