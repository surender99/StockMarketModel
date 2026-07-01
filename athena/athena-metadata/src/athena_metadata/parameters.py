"""Default parameter metadata."""

DEFAULT_PARAMETERS: dict[str, dict[str, int | float | str]] = {
    "ema": {"period": 20},
    "sma": {"period": 20},
    "rsi": {"period": 14},
    "macd": {"fast": 12, "slow": 26, "signal": 9},
}

__all__ = ["DEFAULT_PARAMETERS"]
