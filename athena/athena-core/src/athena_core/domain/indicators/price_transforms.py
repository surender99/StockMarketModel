"""Price transformation formulas — APS-PRICE-*-001, PHASE 3 Architecture."""

from __future__ import annotations

import pandas as pd


def compute_hlc3(ohlcv: pd.DataFrame) -> pd.Series:
    """(high + low + close) / 3 — APS-PRICE-HLC3-001."""
    return (ohlcv["high"] + ohlcv["low"] + ohlcv["close"]) / 3.0


def compute_hl2(ohlcv: pd.DataFrame) -> pd.Series:
    """(high + low) / 2 — APS-PRICE-HL2-001."""
    return (ohlcv["high"] + ohlcv["low"]) / 2.0


def compute_ohlc4(ohlcv: pd.DataFrame) -> pd.Series:
    """(open + high + low + close) / 4 — APS-PRICE-OHLC4-001."""
    return (ohlcv["open"] + ohlcv["high"] + ohlcv["low"] + ohlcv["close"]) / 4.0


def compute_median_price(ohlcv: pd.DataFrame) -> pd.Series:
    """(high + low) / 2 median price alias — APS-PRICE-MEDIANPRICE-001."""
    return compute_hl2(ohlcv)


PRICE_TRANSFORMS: dict[str, object] = {
    "hlc3": compute_hlc3,
    "hl2": compute_hl2,
    "ohlc4": compute_ohlc4,
    "median_price": compute_median_price,
}
