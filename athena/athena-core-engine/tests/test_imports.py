import importlib


def test_engine_facade_imports() -> None:
    mod = importlib.import_module("athena_core_engine")
    for name in ("IndicatorEngine", "PatternPipeline", "StrategyEngine"):
        assert hasattr(mod, name)
