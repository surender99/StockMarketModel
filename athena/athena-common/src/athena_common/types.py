"""Pure domain value types — no infrastructure dependencies."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from typing import Self


@dataclass(frozen=True, slots=True)
class Precision:
    """Decimal precision for monetary calculations."""

    places: int = 2

    def __post_init__(self) -> None:
        if self.places < 0:
            msg = "precision places must be non-negative"
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class Currency:
    """ISO 4217 currency code."""

    code: str

    def __post_init__(self) -> None:
        if len(self.code) != 3 or not self.code.isalpha():
            msg = f"invalid currency code: {self.code!r}"
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class Money:
    """Monetary amount with currency."""

    amount: Decimal
    currency: Currency

    @classmethod
    def of(cls, amount: float | Decimal | str, currency: str | Currency) -> Self:
        cur = currency if isinstance(currency, Currency) else Currency(currency.upper())
        dec = amount if isinstance(amount, Decimal) else Decimal(str(amount))
        return cls(amount=dec, currency=cur)


@dataclass(frozen=True, slots=True)
class Percentage:
    """Percentage value stored as a fraction (0.05 = 5%)."""

    value: float

    def __post_init__(self) -> None:
        if not -1.0 <= self.value <= 1.0:
            msg = f"percentage fraction must be in [-1, 1], got {self.value}"
            raise ValueError(msg)

    @classmethod
    def from_percent(cls, percent: float) -> Self:
        return cls(value=percent / 100.0)

    def as_percent(self) -> float:
        return self.value * 100.0


@dataclass(frozen=True, slots=True)
class OHLC:
    """Open-high-low-close price bar without volume or symbol."""

    open: float
    high: float
    low: float
    close: float

    def __post_init__(self) -> None:
        if self.high < max(self.open, self.close):
            msg = f"high {self.high} must be >= max(open, close)"
            raise ValueError(msg)
        if self.low > min(self.open, self.close):
            msg = f"low {self.low} must be <= min(open, close)"
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class Candle(OHLC):
    """OHLC bar with symbol, timestamp, and volume."""

    symbol: str
    timestamp: date | datetime
    volume: float = 0.0

    def __post_init__(self) -> None:
        if self.volume < 0:
            msg = f"volume must be non-negative for {self.symbol}"
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class Pair:
    """Trading pair (base / quote)."""

    base: str
    quote: str

    def __str__(self) -> str:
        return f"{self.base}/{self.quote}"
