"""Tests for athena_common types."""

from datetime import date
from decimal import Decimal

import pytest

from athena_common import Candle, Money, OHLC, Percentage, TimeFrame
from athena_common.types import Currency


def test_money_creation() -> None:
    m = Money.of(100.5, "USD")
    assert m.amount == Decimal("100.5")
    assert m.currency.code == "USD"


def test_ohlc_validation() -> None:
    OHLC(open=10.0, high=12.0, low=9.0, close=11.0)
    with pytest.raises(ValueError):
        OHLC(open=10.0, high=9.0, low=8.0, close=11.0)


def test_candle() -> None:
    c = Candle(
        open=1.0,
        high=2.0,
        low=0.5,
        close=1.5,
        symbol="AAPL",
        timestamp=date(2024, 1, 1),
        volume=1000.0,
    )
    assert c.symbol == "AAPL"


def test_percentage() -> None:
    p = Percentage.from_percent(5.0)
    assert p.as_percent() == pytest.approx(5.0)


def test_timeframe_intraday() -> None:
    assert TimeFrame.M5.is_intraday
    assert not TimeFrame.D1.is_intraday
