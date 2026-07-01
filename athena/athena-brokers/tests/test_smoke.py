from athena_brokers.alpaca import AlpacaBroker
from athena_brokers.registry import BrokerRegistry
from athena_brokers.zerodha import ZerodhaBroker


def test_broker_registry_smoke() -> None:
    reg = BrokerRegistry()
    reg.register(ZerodhaBroker())
    reg.register(AlpacaBroker())
    assert reg.list_ids() == ["alpaca", "zerodha"]
