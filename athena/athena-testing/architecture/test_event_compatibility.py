"""Event registry YAML must match generated Python contracts."""

from __future__ import annotations

from pathlib import Path

import yaml
from athena_common.events_generated import EVENT_REGISTRY

ATHENA_ROOT = Path(__file__).resolve().parents[2]
REGISTRY_DIR = ATHENA_ROOT / "athena-spec" / "events" / "registry"


def _yaml_events() -> dict[str, int]:
    events: dict[str, int] = {}
    for path in sorted(REGISTRY_DIR.glob("*.event.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if isinstance(data, dict) and "name" in data:
            events[str(data["name"])] = int(data.get("version", 1))
    return events


def test_event_registry_matches_yaml_catalog() -> None:
    yaml_events = _yaml_events()
    assert yaml_events, "event registry directory must not be empty"
    yaml_names = set(yaml_events)
    gen_names = set(EVENT_REGISTRY)
    assert yaml_names == gen_names, f"drift: yaml-only={yaml_names - gen_names} gen-only={gen_names - yaml_names}"


def test_event_versions_match_generated() -> None:
    mismatches: list[str] = []
    for path in sorted(REGISTRY_DIR.glob("*.event.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            continue
        name = str(data["name"])
        expected = int(data.get("version", 1))
        cls = EVENT_REGISTRY.get(name)
        assert cls is not None
        actual = getattr(cls, "VERSION", None)
        if actual != expected:
            mismatches.append(f"{name}: yaml v{expected} != generated v{actual}")
    assert not mismatches, "\n".join(mismatches)


def test_event_payload_fields_present() -> None:
    cls = EVENT_REGISTRY["IndicatorCalculated"]
    fields = cls.__dataclass_fields__
    assert "symbol" in fields
    assert "indicator_id" in fields


def test_event_yaml_has_schema_block() -> None:
    missing: list[str] = []
    for path in sorted(REGISTRY_DIR.glob("*.event.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            continue
        if "schema" not in data:
            missing.append(path.name)
    assert not missing, f"events missing schema block: {missing}"
