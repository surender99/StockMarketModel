import importlib


def test_metadata_facade_imports() -> None:
    mod = importlib.import_module("athena_core_metadata")
    assert len(mod.INDICATOR_CATALOG) > 0
