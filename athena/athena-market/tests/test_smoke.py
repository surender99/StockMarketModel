from athena_market import DEFAULT_EXCHANGE, SUPPORTED_EXCHANGES


def test_market_smoke() -> None:
    assert DEFAULT_EXCHANGE in SUPPORTED_EXCHANGES
