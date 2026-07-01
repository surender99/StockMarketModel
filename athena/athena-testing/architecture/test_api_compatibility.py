"""Public API surface stability — __all__ and Protocol exports."""

from __future__ import annotations

import importlib
from importlib.util import find_spec
from typing import Any

import pytest

FACADE_PACKAGES = [
    "athena_indicators",
    "athena_patterns",
    "athena_strategies",
    "athena_risk",
    "athena_portfolio",
    "athena_execution",
    "athena_data",
    "athena_research",
    "athena_math",
]

MINIMUM_EXPORTS: dict[str, set[str]] = {
    "athena_indicators": {"IndicatorEngine", "IndicatorEngineFacade"},
    "athena_patterns": {"PatternEngineFacade"},
    "athena_strategies": {"StrategyEngineFacade"},
    "athena_risk": set(),
    "athena_portfolio": set(),
    "athena_execution": set(),
    "athena_data": set(),
    "athena_research": {"ResearchWorkspace"},
    "athena_math": set(),
}


def _import_facade(pkg_name: str) -> Any:
    if find_spec(pkg_name) is None:
        pytest.skip(f"{pkg_name} not installed")
    return importlib.import_module(pkg_name)


def test_facade_packages_declare_all() -> None:
    for pkg_name in FACADE_PACKAGES:
        mod = _import_facade(pkg_name)
        assert hasattr(mod, "__all__"), f"{pkg_name} must define __all__"
        assert isinstance(mod.__all__, list)
        assert len(mod.__all__) >= 1, f"{pkg_name}.__all__ must not be empty"


def test_facade_minimum_exports_stable() -> None:
    for pkg_name, required in MINIMUM_EXPORTS.items():
        if not required:
            continue
        mod = _import_facade(pkg_name)
        exports = set(mod.__all__)
        missing = required - exports
        assert not missing, f"{pkg_name} missing stable exports: {missing}"


def test_domain_protocols_importable() -> None:
    protocols = importlib.import_module("athena_domain.contracts.protocols")
    for name in ("IIndicatorEngine", "IStrategyEngine", "IExecutionEngine"):
        assert hasattr(protocols, name), f"Protocol {name} must remain public"


def _protocol_names(mod: Any) -> set[str]:
    return {n for n in dir(mod) if n.endswith("Engine") or n.endswith("Provider")}


def test_protocol_catalog_non_empty() -> None:
    protocols = importlib.import_module("athena_domain.contracts.protocols")
    assert len(_protocol_names(protocols)) >= 3
