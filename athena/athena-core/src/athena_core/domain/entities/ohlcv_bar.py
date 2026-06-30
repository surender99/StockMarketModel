"""OHLCV bar entity — REQ-DATA-INGEST-001."""

from dataclasses import dataclass
from datetime import date

from athena_common.types import OHLC


@dataclass(frozen=True, slots=True)
class OHLCVBar:
    """Single daily OHLCV bar for one symbol."""

    symbol: str
    bar_date: date
    open: float
    high: float
    low: float
    close: float
    volume: float

    def __post_init__(self) -> None:
        OHLC(open=self.open, high=self.high, low=self.low, close=self.close)
        if self.volume < 0:
            msg = f"volume must be non-negative for {self.symbol}"
            raise ValueError(msg)
