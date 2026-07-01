import importlib


def test_runtime_facade_imports() -> None:
    mod = importlib.import_module("athena_core_runtime")
    assert hasattr(mod, "bootstrap_athena_core")
    assert hasattr(mod, "CoreContext")
