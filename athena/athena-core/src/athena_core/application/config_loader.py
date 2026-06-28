"""Configuration loading with optional named profiles — REQ-CLI-001."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field

from athena_core.application.config import AthenaConfig


class ConfigProfileBundle(BaseModel):
    """Named profile overrides stored alongside base Athena YAML."""

    profiles: dict[str, dict[str, Any]] = Field(default_factory=dict)
    default_profile: str | None = None


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    for key, value in override.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def load_config_bundle(path: Path | None) -> tuple[dict[str, Any], ConfigProfileBundle]:
    """Load raw YAML config and profile metadata."""
    if path is None or not path.is_file():
        return {}, ConfigProfileBundle()
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        return {}, ConfigProfileBundle()
    profiles_raw = raw.pop("profiles", {})
    default_profile = raw.pop("default_profile", None)
    profiles: dict[str, dict[str, Any]] = {}
    if isinstance(profiles_raw, dict):
        profiles = {
            str(name): dict(value)
            for name, value in profiles_raw.items()
            if isinstance(value, dict)
        }
    bundle = ConfigProfileBundle(
        profiles=profiles,
        default_profile=str(default_profile) if default_profile else None,
    )
    return raw, bundle


def resolve_profile_name(
    bundle: ConfigProfileBundle,
    profile: str | None,
) -> str | None:
    """Resolve explicit profile, default profile, or None."""
    if profile:
        return profile
    return bundle.default_profile


def load_athena_config(
    path: Path | None = None,
    *,
    profile: str | None = None,
) -> AthenaConfig:
    """Load AthenaConfig from YAML with optional profile overlay."""
    raw, bundle = load_config_bundle(path)
    selected = resolve_profile_name(bundle, profile)
    if selected:
        if selected not in bundle.profiles:
            known = ", ".join(sorted(bundle.profiles)) or "(none)"
            msg = f"unknown config profile '{selected}'; available: {known}"
            raise ValueError(msg)
        raw = _deep_merge(raw, bundle.profiles[selected])
    return AthenaConfig.model_validate(raw)


def list_profile_names(path: Path | None) -> list[str]:
    """Return profile names declared in a config file."""
    _, bundle = load_config_bundle(path)
    return sorted(bundle.profiles)
