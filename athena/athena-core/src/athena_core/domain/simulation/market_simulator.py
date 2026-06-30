"""Market simulator stub — REQ-APS-MARKET-CORE-001."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from athena_core.domain.simulation.event_bus import SimulationEvent, SimulationEventBus, SimulationEventType


@dataclass(frozen=True, slots=True)
class MarketQuote:
    """Snapshot of simulated market state for one symbol."""

    symbol: str
    last: float
    bid: float
    ask: float
    timestamp: datetime


class MarketSimulator:
    """Stub market state with bid/ask spread — APS-MARKET-CORE-001."""

    def __init__(self, *, bus: SimulationEventBus | None = None, spread_bps: float = 5.0) -> None:
        self._bus = bus
        self._spread_bps = spread_bps
        self._quotes: dict[str, MarketQuote] = {}

    def update(self, symbol: str, last: float, timestamp: datetime) -> MarketQuote:
        half_spread = last * (self._spread_bps / 10_000.0) / 2.0
        quote = MarketQuote(
            symbol=symbol,
            last=last,
            bid=round(last - half_spread, 4),
            ask=round(last + half_spread, 4),
            timestamp=timestamp,
        )
        self._quotes[symbol] = quote
        if self._bus is not None:
            self._bus.publish(
                SimulationEvent(
                    SimulationEventType.MARKET,
                    timestamp,
                    {
                        "symbol": symbol,
                        "last": quote.last,
                        "bid": quote.bid,
                        "ask": quote.ask,
                    },
                )
            )
        return quote

    def quote(self, symbol: str) -> MarketQuote | None:
        return self._quotes.get(symbol)
