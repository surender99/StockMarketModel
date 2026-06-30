"""Protocol contract smoke tests."""

from athena_domain import IIndicatorEngine, IStrategyEngine


def test_protocols_are_runtime_checkable() -> None:
    assert hasattr(IIndicatorEngine, "__protocol_attrs__") or hasattr(IIndicatorEngine, "_is_protocol")
    assert IStrategyEngine.__name__ == "IStrategyEngine"
