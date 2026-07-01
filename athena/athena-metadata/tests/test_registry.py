from athena_metadata import load_registry


def test_load_registry() -> None:
    reg = load_registry()
    assert len(reg.indicators) > 0
    assert len(reg.strategies) > 0
