import importlib


def test_events_facade_imports() -> None:
    mod = importlib.import_module("athena_core_events")
    assert "EVENT_REGISTRY" in mod.__all__
    assert "IndicatorCalculated" in mod.EVENT_REGISTRY
