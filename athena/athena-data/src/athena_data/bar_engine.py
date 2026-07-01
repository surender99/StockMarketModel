"""Tick-to-bar aggregation — ATH-IP-000012 Bar-Engine MVP."""

from __future__ import annotations

from collections import defaultdict
from decimal import Decimal

from athena_common.types import OHLC
from athena_data.tick_repository import Tick


class BarEngine:
    """Build OHLC bars from ordered ticks (single timeframe bucket per call)."""

    def aggregate(self, ticks: list[Tick]) -> dict[str, OHLC]:
        buckets: dict[str, list[Tick]] = defaultdict(list)
        for tick in ticks:
            buckets[tick.symbol].append(tick)

        bars: dict[str, OHLC] = {}
        for symbol, series in buckets.items():
            if not series:
                continue
            prices = [float(t.price) for t in series]
            bars[symbol] = OHLC(
                open=prices[0],
                high=max(prices),
                low=min(prices),
                close=prices[-1],
            )
        return bars
