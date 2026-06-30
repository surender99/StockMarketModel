"""Import smoke tests — facade re-exports from athena-core."""
import importlib


def test_package_imports() -> None:
    mod = importlib.import_module("athena_patterns")
    assert mod is not None
