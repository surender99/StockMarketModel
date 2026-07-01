#!/usr/bin/env python3
"""Generate DTO dataclasses from athena-spec/schemas/dtos/*.dto.yaml."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

import yaml

ATHENA_ROOT = Path(__file__).resolve().parents[1]
SPEC_DIR = ATHENA_ROOT / "athena-spec" / "schemas" / "dtos"
DEFAULT_OUTPUT = ATHENA_ROOT / "athena-common" / "src" / "athena_common" / "dtos_generated.py"

PY_TYPE_MAP = {
    "string": "str",
    "integer": "int",
    "float": "float",
    "boolean": "bool",
}


def _field_type(spec: str) -> str:
    return PY_TYPE_MAP.get(spec.strip().lower(), "Any")


def _load_dtos(spec_dir: Path) -> list[dict[str, Any]]:
    dtos: list[dict[str, Any]] = []
    for path in sorted(spec_dir.glob("*.dto.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            data["_source"] = path.name
            dtos.append(data)
    return dtos


def _render_dto(dto: dict[str, Any]) -> str:
    name = str(dto["name"])
    version = int(dto.get("version", 1))
    fields = dto.get("fields", {})
    description = str(dto.get("description", ""))

    field_lines = [f"    {fname}: {_field_type(str(ftype))}" for fname, ftype in fields.items()]
    doc = description.replace('"', "'")
    lines = [
        "@dataclass(frozen=True, slots=True)",
        f"class {name}:",
        f'    """{doc} — v{version}."""',
        "",
        f"    VERSION: ClassVar[int] = {version}",
    ]
    if field_lines:
        lines.append("")
        lines.extend(field_lines)
    else:
        lines.append("    pass")
    return "\n".join(lines)


def generate(spec_dir: Path, output: Path) -> str:
    dtos = _load_dtos(spec_dir)
    if not dtos:
        msg = f"no DTO specs found in {spec_dir}"
        raise FileNotFoundError(msg)

    header = '''# GENERATED — DO NOT EDIT
# Source: athena-spec/schemas/dtos/*.dto.yaml
# Regenerate: make codegen

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, ClassVar

'''
    blocks = [_render_dto(d) for d in dtos]
    registry = {str(d["name"]): str(d["name"]) for d in dtos}
    registry_lines = ["DTO_REGISTRY: dict[str, type] = {"]
    for name, cls in registry.items():
        registry_lines.append(f"    {name!r}: {cls},")
    registry_lines.append("}")
    registry_lines.append("")
    registry_lines.append("__all__ = [")
    for cls in registry.values():
        registry_lines.append(f'    "{cls}",')
    registry_lines.append('    "DTO_REGISTRY",')
    registry_lines.append("]")

    return header + "\n\n".join(blocks) + "\n\n\n" + "\n".join(registry_lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate DTO classes from YAML specs")
    parser.add_argument("--spec-dir", type=Path, default=SPEC_DIR)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    code = generate(args.spec_dir, args.output)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(code, encoding="utf-8")
    print(f"Wrote {args.output} ({len(re.findall(r'^class ', code, re.M))} DTOs)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
