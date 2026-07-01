"""Enforce ADR-0006 bounded-context manifest and layering rules."""

from __future__ import annotations

from pathlib import Path

import yaml

ATHENA_ROOT = Path(__file__).resolve().parents[2]

VALID_CONTEXTS = {
    "foundation",
    "contracts",
    "data",
    "indicators",
    "patterns",
    "strategies",
    "risk",
    "portfolio",
    "execution",
    "analytics",
    "research",
    "platform",
    "specification",
    "runtime",
    "events",
    "engine",
    "metadata",
    "observability",
    "market",
    "brokers",
}

# bounded_context -> allowed dependency package prefixes (manifest names)
CONTEXT_ALLOWED_DEPS: dict[str, set[str]] = {
    "foundation": set(),
    "contracts": {"athena-common", "athena-os"},
    "data": {"athena-os", "athena-common", "athena-core"},
    "indicators": {"athena-os", "athena-common", "athena-core"},
    "patterns": {"athena-os", "athena-common", "athena-core"},
    "strategies": {"athena-os", "athena-common", "athena-core"},
    "risk": {"athena-os", "athena-common", "athena-core"},
    "portfolio": {"athena-os", "athena-common", "athena-core"},
    "execution": {"athena-os", "athena-common", "athena-core"},
    "analytics": {"athena-os", "athena-common", "athena-core"},
    "research": {"athena-os", "athena-common", "athena-core"},
    "runtime": {"athena-os", "athena-common", "athena-core"},
    "events": {"athena-os", "athena-common", "athena-core"},
    "engine": {"athena-os", "athena-common", "athena-core"},
    "metadata": {"athena-os", "athena-common", "athena-core"},
    "observability": {"athena-os", "athena-common", "athena-core"},
    "market": {"athena-os", "athena-common", "athena-core"},
    "brokers": {"athena-os", "athena-common", "athena-core"},
}


def _load_manifest(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def _packages(data: dict) -> list[str]:
    deps = data.get("dependencies", {})
    if isinstance(deps, dict):
        return list(deps.get("packages", []) or [])
    return list(deps or [])


def test_manifests_use_valid_bounded_contexts() -> None:
    errors: list[str] = []
    for path in sorted(ATHENA_ROOT.glob("athena-*/module.yaml")):
        data = _load_manifest(path)
        ctx = data.get("bounded_context", data.get("layer"))
        if ctx not in VALID_CONTEXTS:
            errors.append(f"{path.name}: invalid bounded_context '{ctx}'")
        if not data.get("owner"):
            errors.append(f"{path.name}: missing owner")
    assert not errors, "\n".join(errors)


def test_bounded_context_dependency_allowlist() -> None:
    errors: list[str] = []
    for path in sorted(ATHENA_ROOT.glob("athena-*/module.yaml")):
        data = _load_manifest(path)
        ctx = data.get("bounded_context", data.get("layer", ""))
        allowed = CONTEXT_ALLOWED_DEPS.get(ctx)
        if allowed is None:
            continue
        for dep in _packages(data):
            if dep not in allowed and ctx != "platform" and ctx != "specification":
                errors.append(f"{data.get('name')}: {ctx} may not depend on {dep}")
    assert not errors, "\n".join(errors)


def test_core_facades_do_not_depend_on_bounded_contexts() -> None:
    """athena-core must not import facade bounded contexts (ADR-0006)."""
    core_manifest = ATHENA_ROOT / "athena-core" / "module.yaml"
    if not core_manifest.exists():
        return
    data = _load_manifest(core_manifest)
    bounded = {
        "athena-data",
        "athena-indicators",
        "athena-patterns",
        "athena-strategies",
        "athena-risk",
        "athena-portfolio",
        "athena-execution",
    }
    for dep in _packages(data):
        assert dep not in bounded, f"athena-core must not depend on {dep}"
