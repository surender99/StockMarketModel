"""OHLCV bar entity — REQ-DATA-INGEST-001."""

from dataclasses import dataclass
from datetime import date


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
        if self.high < max(self.open, self.close):
            msg = f"high {self.high} must be >= max(open, close) for {self.symbol}"
            raise ValueError(msg)
        if self.low > min(self.open, self.close):
            msg = f"low {self.low} must be <= min(open, close) for {self.symbol}"
            raise ValueError(msg)
        if self.volume < 0:
            msg = f"volume must be non-negative for {self.symbol}"
            raise ValueError(msg)
