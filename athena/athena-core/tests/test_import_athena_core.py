"""Smoke tests for athena-core package."""

from datetime import date

import athena_core
from athena_core.domain.entities import OHLCVBar, Symbol
from athena_core.infrastructure.logging import configure_logging, get_logger


def test_import_athena_core() -> None:
    assert athena_core.__version__ == "0.1.0"


def test_symbol_yfinance_ticker() -> None:
    sym = Symbol(code="RELIANCE")
    assert sym.yfinance_ticker == "RELIANCE.NS"
    assert str(sym) == "RELIANCE.NSE"


def test_ohlcv_bar_valid() -> None:
    bar = OHLCVBar(
        symbol="RELIANCE.NS",
        bar_date=date(2024, 1, 2),
        open=100.0,
        high=105.0,
        low=99.0,
        close=104.0,
        volume=1_000_000.0,
    )
    assert bar.close == 104.0


def test_structured_logging_configures() -> None:
    configure_logging()
    log = get_logger("test")
    log.info("smoke_test", status="ok")
