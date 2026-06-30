"""Indicator APS catalog — REQ-APS-IND-REGISTRY-001, ATH-REL-004."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

IndicatorStatus = Literal["MVP", "Partial", "Deferred"]


@dataclass(frozen=True, slots=True)
class IndicatorCatalogEntry:
    """Metadata for a built-in indicator wired to an APS spec."""

    plugin_id: str
    aps_id: str
    name: str
    category: str
    status: IndicatorStatus


INDICATOR_CATALOG: tuple[IndicatorCatalogEntry, ...] = (
    IndicatorCatalogEntry("sma", "APS-IND-SMA-001", "Simple Moving Average", "Moving-Averages", "MVP"),
    IndicatorCatalogEntry("ema", "APS-IND-EMA-001", "Exponential Moving Average", "Moving-Averages", "MVP"),
    IndicatorCatalogEntry("wma", "APS-IND-WMA-001", "Weighted Moving Average", "Moving-Averages", "MVP"),
    IndicatorCatalogEntry("adx", "APS-IND-ADX-001", "Average Directional Index", "Trend-Indicators", "MVP"),
    IndicatorCatalogEntry("macd", "APS-IND-MACD-001", "MACD", "Trend-Indicators", "MVP"),
    IndicatorCatalogEntry("rsi", "APS-IND-RSI-001", "Relative Strength Index", "Momentum-Indicators", "MVP"),
    IndicatorCatalogEntry("roc", "APS-IND-ROC-001", "Rate of Change", "Momentum-Indicators", "MVP"),
    IndicatorCatalogEntry("stoch", "APS-IND-STOCH-001", "Stochastic Oscillator", "Momentum-Indicators", "MVP"),
    IndicatorCatalogEntry("obv", "APS-IND-OBV-001", "On-Balance Volume", "Volume-Indicators", "MVP"),
    IndicatorCatalogEntry("cmf", "APS-IND-CMF-001", "Chaikin Money Flow", "Volume-Indicators", "MVP"),
    IndicatorCatalogEntry("mfi", "APS-IND-MFI-001", "Money Flow Index", "Volume-Indicators", "MVP"),
    IndicatorCatalogEntry("atr", "APS-IND-ATR-001", "Average True Range", "Volatility-Indicators", "MVP"),
    IndicatorCatalogEntry("bollinger", "APS-IND-BBANDS-001", "Bollinger Bands", "Volatility-Indicators", "MVP"),
    IndicatorCatalogEntry("cci", "APS-IND-CCI-001", "Commodity Channel Index", "Oscillators", "MVP"),
    IndicatorCatalogEntry("willr", "APS-IND-WILLR-001", "Williams Percent R", "Oscillators", "MVP"),
)


def list_mvp_indicators() -> list[IndicatorCatalogEntry]:
    """Return catalog entries with MVP status."""
    return [e for e in INDICATOR_CATALOG if e.status == "MVP"]


def lookup_indicator_aps(plugin_id: str) -> IndicatorCatalogEntry | None:
    """Resolve APS metadata for a plugin id."""
    for entry in INDICATOR_CATALOG:
        if entry.plugin_id == plugin_id:
            return entry
    return None
