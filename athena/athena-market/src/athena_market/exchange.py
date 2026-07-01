"""Exchange metadata stub."""

DEFAULT_EXCHANGE = "NSE"

SUPPORTED_EXCHANGES: tuple[str, ...] = ("NSE", "BSE", "NYSE", "NASDAQ")

__all__ = ["DEFAULT_EXCHANGE", "SUPPORTED_EXCHANGES"]
