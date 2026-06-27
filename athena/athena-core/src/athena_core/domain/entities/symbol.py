"""Trading symbol value object."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Symbol:
    """NSE symbol with optional yfinance ticker suffix."""

    code: str
    exchange: str = "NSE"
    yfinance_suffix: str = ".NS"

    @property
    def yfinance_ticker(self) -> str:
        return f"{self.code}{self.yfinance_suffix}"

    def __str__(self) -> str:
        return f"{self.code}.{self.exchange}"
