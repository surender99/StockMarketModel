"""Indicator APS catalog — REQ-APS-IND-REGISTRY-001, PHASE 3 Architecture."""

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


def _e(
    plugin_id: str,
    aps_id: str,
    name: str,
    category: str,
    status: IndicatorStatus = "Deferred",
) -> IndicatorCatalogEntry:
    return IndicatorCatalogEntry(plugin_id, aps_id, name, category, status)


INDICATOR_CATALOG: tuple[IndicatorCatalogEntry, ...] = (
    # Price transformations (MVP)
    _e("hlc3", "APS-PRICE-HLC3-001", "HLC3 Price", "Price-Transformations", "MVP"),
    _e("hl2", "APS-PRICE-HL2-001", "HL2 Price", "Price-Transformations", "MVP"),
    _e("ohlc4", "APS-PRICE-OHLC4-001", "OHLC4 Price", "Price-Transformations", "MVP"),
    _e("median_price", "APS-PRICE-MEDIANPRICE-001", "Median Price", "Price-Transformations", "MVP"),
    _e("heikin_ashi", "APS-PRICE-HEIKINASHI-001", "Heikin Ashi", "Price-Transformations"),
    _e("renko", "APS-PRICE-RENKO-001", "Renko", "Price-Transformations"),
    _e("kagi", "APS-PRICE-KAGI-001", "Kagi", "Price-Transformations"),
    _e("line_break", "APS-PRICE-LINEBREAK-001", "Line Break", "Price-Transformations"),
    _e("point_figure", "APS-PRICE-POINTFIGURE-001", "Point and Figure", "Price-Transformations"),
    _e("pivot_points", "APS-PRICE-PIVOT-001", "Pivot Points", "Price-Transformations", "MVP"),
    # Moving averages
    _e("sma", "APS-IND-SMA-001", "Simple Moving Average", "Moving-Averages", "MVP"),
    _e("ema", "APS-IND-EMA-001", "Exponential Moving Average", "Moving-Averages", "MVP"),
    _e("wma", "APS-IND-WMA-001", "Weighted Moving Average", "Moving-Averages", "MVP"),
    _e("hma", "APS-IND-HMA-001", "Hull Moving Average", "Moving-Averages"),
    _e("vwma", "APS-IND-VWMA-001", "Volume Weighted Moving Average", "Moving-Averages"),
    _e("kama", "APS-IND-KAMA-001", "Kaufman Adaptive Moving Average", "Moving-Averages"),
    _e("dema", "APS-IND-DEMA-001", "Double Exponential Moving Average", "Moving-Averages"),
    _e("tema", "APS-IND-TEMA-001", "Triple Exponential Moving Average", "Moving-Averages"),
    _e("zlema", "APS-IND-ZLEMA-001", "Zero Lag Exponential Moving Average", "Moving-Averages"),
    _e("alma", "APS-IND-ALMA-001", "Arnaud Legoux Moving Average", "Moving-Averages"),
    _e("lsma", "APS-IND-LSMA-001", "Least Squares Moving Average", "Moving-Averages"),
    _e("t3", "APS-IND-T3-001", "T3 Moving Average", "Moving-Averages"),
    # Trend
    _e("adx", "APS-IND-ADX-001", "Average Directional Index", "Trend-Indicators", "MVP"),
    _e("macd", "APS-IND-MACD-001", "MACD", "Trend-Indicators", "MVP"),
    _e("supertrend", "APS-IND-SUPERTREND-001", "SuperTrend", "Trend-Indicators"),
    _e("dmi", "APS-IND-DMI-001", "Directional Movement Index", "Trend-Indicators"),
    _e("aroon", "APS-IND-AROON-001", "Aroon", "Trend-Indicators"),
    _e("psar", "APS-IND-PSAR-001", "Parabolic SAR", "Trend-Indicators"),
    _e("vortex", "APS-IND-VORTEX-001", "Vortex Indicator", "Trend-Indicators"),
    _e("ichimoku", "APS-IND-ICHIMOKU-001", "Ichimoku Cloud", "Trend-Indicators", "MVP"),
    _e("donchian", "APS-IND-DONCHIAN-001", "Donchian Channels", "Trend-Indicators"),
    _e("ma_ribbon", "APS-IND-MARIBBON-001", "Moving Average Ribbon", "Trend-Indicators"),
    # Momentum
    _e("rsi", "APS-IND-RSI-001", "Relative Strength Index", "Momentum-Indicators", "MVP"),
    _e("roc", "APS-IND-ROC-001", "Rate of Change", "Momentum-Indicators", "MVP"),
    _e("stoch", "APS-IND-STOCH-001", "Stochastic Oscillator", "Momentum-Indicators", "MVP"),
    _e("mom", "APS-IND-MOM-001", "Momentum", "Momentum-Indicators"),
    _e("ppo", "APS-IND-PPO-001", "Percentage Price Oscillator", "Momentum-Indicators"),
    _e("trix", "APS-IND-TRIX-001", "TRIX", "Momentum-Indicators"),
    _e("ao", "APS-IND-AO-001", "Awesome Oscillator", "Momentum-Indicators"),
    _e("tsi", "APS-IND-TSI-001", "True Strength Index", "Momentum-Indicators"),
    # Oscillators
    _e("cci", "APS-IND-CCI-001", "Commodity Channel Index", "Oscillators", "MVP"),
    _e("willr", "APS-IND-WILLR-001", "Williams Percent R", "Oscillators", "MVP"),
    _e("uo", "APS-IND-UO-001", "Ultimate Oscillator", "Oscillators"),
    _e("kst", "APS-IND-KST-001", "Know Sure Thing", "Oscillators"),
    _e("fisher", "APS-IND-FISHER-001", "Fisher Transform", "Oscillators"),
    _e("dpo", "APS-IND-DPO-001", "Detrended Price Oscillator", "Oscillators"),
    # Volatility
    _e("atr", "APS-IND-ATR-001", "Average True Range", "Volatility-Indicators", "MVP"),
    _e("bollinger", "APS-IND-BBANDS-001", "Bollinger Bands", "Volatility-Indicators", "MVP"),
    _e("keltner", "APS-IND-KELTNER-001", "Keltner Channels", "Volatility-Indicators"),
    _e("chv", "APS-IND-CHV-001", "Chaikin Volatility", "Volatility-Indicators"),
    _e("stddev", "APS-IND-STDDEV-001", "Standard Deviation", "Volatility-Indicators"),
    _e("hvol", "APS-IND-HVOL-001", "Historical Volatility", "Volatility-Indicators"),
    _e("vstop", "APS-IND-VSTOP-001", "Volatility Stop", "Volatility-Indicators"),
    _e("atr_bands", "APS-IND-ATRBANDS-001", "ATR Bands", "Volatility-Indicators", "MVP"),
    # Volume
    _e("obv", "APS-IND-OBV-001", "On-Balance Volume", "Volume-Indicators", "MVP"),
    _e("cmf", "APS-IND-CMF-001", "Chaikin Money Flow", "Volume-Indicators", "MVP"),
    _e("mfi", "APS-IND-MFI-001", "Money Flow Index", "Volume-Indicators", "MVP"),
    _e("vwap", "APS-IND-VWAP-001", "Volume Weighted Average Price", "Volume-Indicators", "MVP"),
    _e("adl", "APS-IND-ADL-001", "Accumulation Distribution Line", "Volume-Indicators"),
    _e("eom", "APS-IND-EOM-001", "Ease of Movement", "Volume-Indicators"),
    _e("fi", "APS-IND-FI-001", "Force Index", "Volume-Indicators"),
    _e("nvi", "APS-IND-NVI-001", "Negative Volume Index", "Volume-Indicators"),
    _e("pvi", "APS-IND-PVI-001", "Positive Volume Index", "Volume-Indicators"),
    # Breadth
    _e("breadth", "APS-IND-BREADTH-001", "Market Breadth Engine", "Market-Breadth", "Partial"),
    _e("ad_line", "APS-IND-ADLINE-001", "Advance Decline Line", "Market-Breadth"),
    _e("adr", "APS-IND-ADR-001", "Advance Decline Ratio", "Market-Breadth"),
    _e("mcclellan", "APS-IND-MCCLELLAN-001", "McClellan Oscillator", "Market-Breadth"),
    _e("trin", "APS-IND-TRIN-001", "TRIN Arms Index", "Market-Breadth"),
    _e("arms", "APS-IND-ARMS-001", "Arms Index", "Market-Breadth"),
    _e("hl_index", "APS-IND-HLINDEX-001", "High Low Index", "Market-Breadth"),
    # Cycle
    _e("hilbert", "APS-IND-HILBERT-001", "Hilbert Transform", "Cycle-Indicators"),
    _e("domcycle", "APS-IND-DOMCYCLE-001", "Dominant Cycle", "Cycle-Indicators"),
    _e("ehlers", "APS-IND-EHLERS-001", "Ehlers Filters", "Cycle-Indicators"),
    _e("sinewave", "APS-IND-SINEWAVE-001", "Sine Wave Indicator", "Cycle-Indicators"),
    # Composite
    _e("macd_hist", "APS-IND-MACDHIST-001", "MACD Histogram", "Composite-Indicators"),
    _e("stoch_rsi", "APS-IND-STOCHRSI-001", "Stochastic RSI", "Composite-Indicators"),
    _e("crsi", "APS-IND-CRSI-001", "Connors RSI", "Composite-Indicators"),
    _e("elder_ray", "APS-IND-ELDERRAY-001", "Elder Ray", "Composite-Indicators"),
    _e("ttm_squeeze", "APS-IND-TTMSQUEEZE-001", "TTM Squeeze", "Composite-Indicators"),
    _e("comp_mom", "APS-IND-COMPMOM-001", "Composite Momentum", "Composite-Indicators"),
    _e("comp_trend", "APS-IND-COMPTREND-001", "Composite Trend Score", "Composite-Indicators"),
)


def list_mvp_indicators() -> list[IndicatorCatalogEntry]:
    """Return catalog entries with MVP status."""
    return [e for e in INDICATOR_CATALOG if e.status == "MVP"]


def list_by_status(status: IndicatorStatus) -> list[IndicatorCatalogEntry]:
    """Return catalog entries filtered by implementation status."""
    return [e for e in INDICATOR_CATALOG if e.status == status]


def lookup_indicator_aps(plugin_id: str) -> IndicatorCatalogEntry | None:
    """Resolve APS metadata for a plugin id."""
    for entry in INDICATOR_CATALOG:
        if entry.plugin_id == plugin_id:
            return entry
    return None


def lookup_by_aps_id(aps_id: str) -> IndicatorCatalogEntry | None:
    """Resolve catalog entry by APS id."""
    for entry in INDICATOR_CATALOG:
        if entry.aps_id == aps_id:
            return entry
    return None
