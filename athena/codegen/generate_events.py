#!/usr/bin/env python3
"""Generate Python event dataclasses from athena-spec/events/registry/*.event.yaml."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

import yaml

ATHENA_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_DIR = ATHENA_ROOT / "athena-spec" / "events" / "registry"
DEFAULT_OUTPUT = ATHENA_ROOT / "athena-common" / "src" / "athena_common" / "events_generated.py"

PY_TYPE_MAP = {
    "string": "str",
    "integer": "int",
    "float": "float",
    "boolean": "bool",
}


def _field_type(spec: str) -> str:
    return PY_TYPE_MAP.get(spec.strip().lower(), "Any")


def _load_events(registry_dir: Path) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for path in sorted(registry_dir.glob("*.event.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            data["_source"] = path.name
            events.append(data)
    return events


def _payload_schema(payload: dict[str, Any]) -> dict[str, Any]:
    properties = {k: {"type": _json_type(str(v))} for k, v in payload.items()}
    return {
        "type": "object",
        "required": list(payload.keys()),
        "properties": properties,
    }


def _json_type(spec: str) -> str:
    mapping = {"string": "string", "integer": "integer", "float": "number", "boolean": "boolean"}
    return mapping.get(spec.strip().lower(), "string")


def _render_event(event: dict[str, Any]) -> str:
    name = str(event["name"])
    version = int(event.get("version", 1))
    publisher = str(event.get("publisher", ""))
    consumers = event.get("consumers", [])
    payload = event.get("payload", {})
    description = str(event.get("description", ""))
    schema = event.get("schema") or _payload_schema(payload)

    fields: list[str] = []
    for field_name, type_spec in payload.items():
        py_type = _field_type(str(type_spec))
        fields.append(f"    {field_name}: {py_type}")

    consumer_repr = ", ".join(repr(c) for c in consumers)
    schema_repr = repr(schema)
    doc = description.replace('"', "'")
    lines = [
        "@dataclass(frozen=True, slots=True)",
        f"class {name}Event:",
        f'    """{doc} — v{version}, publisher={publisher}."""',
        "",
        f"    EVENT_NAME: ClassVar[str] = {name!r}",
        f"    VERSION: ClassVar[int] = {version}",
        f"    PUBLISHER: ClassVar[str] = {publisher!r}",
        f"    CONSUMERS: ClassVar[tuple[str, ...]] = ({consumer_repr})",
        f"    SCHEMA: ClassVar[dict[str, Any]] = {schema_repr}",
    ]
    if fields:
        lines.append("")
        lines.extend(fields)
    else:
        lines.append("    pass")
    return "\n".join(lines)


def generate(registry_dir: Path, output: Path) -> str:
    events = _load_events(registry_dir)
    if not events:
        msg = f"no events found in {registry_dir}"
        raise FileNotFoundError(msg)

    event_blocks = [_render_event(e) for e in events]
    registry_map = {str(e["name"]): f"{e['name']}Event" for e in events}

    header = '''# GENERATED — DO NOT EDIT
# Source: athena-spec/events/registry/*.event.yaml
# Regenerate: make codegen  OR  python athena/scripts/generate_events.py

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, ClassVar

'''
    registry_lines = ["EVENT_REGISTRY: dict[str, type] = {"]
    for name, cls in registry_map.items():
        registry_lines.append(f"    {name!r}: {cls},")
    registry_lines.append("}")
    registry_lines.append("")
    registry_lines.append("__all__ = [")
    for cls in registry_map.values():
        registry_lines.append(f'    "{cls}",')
    registry_lines.append('    "EVENT_REGISTRY",')
    registry_lines.append("]")

    body = "\n\n".join(event_blocks)
    return header + body + "\n\n\n" + "\n".join(registry_lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate event classes from YAML registry")
    parser.add_argument("--registry", type=Path, default=REGISTRY_DIR)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    code = generate(args.registry, args.output)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(code, encoding="utf-8")
    print(f"Wrote {args.output} ({len(re.findall(r'^class ', code, re.M))} events)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
