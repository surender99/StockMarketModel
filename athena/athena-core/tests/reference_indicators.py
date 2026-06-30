"""Reference indicators for parity tests — REQ-IND-EMA-001, REQ-IND-SMA-001."""

from __future__ import annotations

import pandas as pd


def reference_ema(series: pd.Series, period: int) -> pd.Series:
    """Independent reference matching pandas-ta ``ema`` (ewm span, adjust=False)."""
    return series.ewm(span=period, adjust=False).mean()


def reference_sma(series: pd.Series, period: int) -> pd.Series:
    """Independent reference matching pandas-ta ``sma`` (rolling window)."""
    return series.rolling(window=period, min_periods=period).mean()


def pandas_ta_ema(series: pd.Series, period: int) -> pd.Series | None:
    """Return pandas-ta EMA when the library is installed."""
    try:
        import pandas_ta as ta
    except ImportError:
        return None
    return ta.ema(series, length=period)


def pandas_ta_sma(series: pd.Series, period: int) -> pd.Series | None:
    """Return pandas-ta SMA when the library is installed."""
    try:
        import pandas_ta as ta
    except ImportError:
        return None
    return ta.sma(series, length=period)


def pandas_ta_rsi(series: pd.Series, period: int) -> pd.Series | None:
    """Return pandas-ta RSI when the library is installed."""
    try:
        import pandas_ta as ta
    except ImportError:
        return None
    return ta.rsi(series, length=period)


def pandas_ta_macd(
    series: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9
) -> pd.DataFrame | None:
    """Return pandas-ta MACD when the library is installed."""
    try:
        import pandas_ta as ta
    except ImportError:
        return None
    result = ta.macd(series, fast=fast, slow=slow, signal=signal)
    if result is None:
        return None
    cols = result.columns.tolist()
    return pd.DataFrame(
        {
            "macd": result[cols[0]],
            "histogram": result[cols[1]],
            "signal": result[cols[2]],
        },
        index=series.index,
    )


def pandas_ta_stoch(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    k_period: int = 14,
    d_period: int = 3,
) -> pd.DataFrame | None:
    """Return pandas-ta stochastic when the library is installed."""
    try:
        import pandas_ta as ta
    except ImportError:
        return None
    result = ta.stoch(high, low, close, k=k_period, d=d_period)
    if result is None:
        return None
    cols = result.columns.tolist()
    return pd.DataFrame(
        {
            "stoch_k": result[cols[0]],
            "stoch_d": result[cols[1]],
        },
        index=close.index,
    )


def reference_ichimoku(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    tenkan_period: int = 9,
    kijun_period: int = 26,
    senkou_period: int = 52,
    displacement: int = 26,
) -> pd.DataFrame:
    """Independent Ichimoku reference (midprice rolling extrema)."""
    tenkan = (high.rolling(tenkan_period, min_periods=tenkan_period).max() + low.rolling(tenkan_period, min_periods=tenkan_period).min()) / 2
    kijun = (high.rolling(kijun_period, min_periods=kijun_period).max() + low.rolling(kijun_period, min_periods=kijun_period).min()) / 2
    senkou_a = ((tenkan + kijun) / 2).shift(displacement)
    senkou_b = ((high.rolling(senkou_period, min_periods=senkou_period).max() + low.rolling(senkou_period, min_periods=senkou_period).min()) / 2).shift(displacement)
    chikou = close.shift(-displacement)
    return pd.DataFrame(
        {"tenkan": tenkan, "kijun": kijun, "senkou_a": senkou_a, "senkou_b": senkou_b, "chikou": chikou},
        index=close.index,
    )


def reference_vwap(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    volume: pd.Series,
    *,
    session: pd.Series | None = None,
) -> pd.Series:
    """Independent cumulative/session VWAP reference."""
    typical = (high.astype(float) + low.astype(float) + close.astype(float)) / 3
    tp_vol = typical * volume.astype(float)
    if session is not None:
        cum_tp = tp_vol.groupby(session).cumsum()
        cum_vol = volume.astype(float).groupby(session).cumsum()
    else:
        cum_tp = tp_vol.cumsum()
        cum_vol = volume.astype(float).cumsum()
    return cum_tp / cum_vol


def pandas_ta_vwap(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    volume: pd.Series,
) -> pd.Series | None:
    """Return pandas-ta VWAP when the library is installed."""
    try:
        import pandas_ta as ta
    except ImportError:
        return None
    result = ta.vwap(high=high, low=low, close=close, volume=volume)
    return result


def pandas_ta_ichimoku(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    tenkan: int = 9,
    kijun: int = 26,
    senkou: int = 52,
) -> pd.DataFrame | None:
    """Return pandas-ta Ichimoku when the library is installed."""
    try:
        import pandas_ta as ta
    except ImportError:
        return None
    result = ta.ichimoku(high=high, low=low, close=close, tenkan=tenkan, kijun=kijun, senkou=senkou)
    if result is None:
        return None
    if isinstance(result, tuple):
        frame = pd.concat(result, axis=1)
    else:
        frame = result
    cols = frame.columns.tolist()
    mapping = {
        cols[0]: "tenkan",
        cols[1]: "kijun",
        cols[2]: "senkou_a",
        cols[3]: "senkou_b",
        cols[4]: "chikou",
    }
    return frame.rename(columns=mapping)


def reference_pivot_points(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
) -> pd.DataFrame:
    """Independent classic pivot reference from prior bar HLC."""
    prev_high = high.astype(float).shift(1)
    prev_low = low.astype(float).shift(1)
    prev_close = close.astype(float).shift(1)
    range_hl = prev_high - prev_low
    pivot = (prev_high + prev_low + prev_close) / 3
    return pd.DataFrame(
        {
            "pivot": pivot,
            "r1": 2 * pivot - prev_low,
            "r2": pivot + range_hl,
            "r3": prev_high + 2 * (pivot - prev_low),
            "s1": 2 * pivot - prev_high,
            "s2": pivot - range_hl,
            "s3": prev_low - 2 * (prev_high - pivot),
        },
        index=close.index,
    )


def pandas_ta_bbands(series: pd.Series, period: int = 20, std_dev: float = 2.0) -> pd.DataFrame | None:
    """Return pandas-ta Bollinger Bands when the library is installed."""
    try:
        import pandas_ta as ta
    except ImportError:
        return None
    result = ta.bbands(series, length=period, std=std_dev)
    if result is None:
        return None
    cols = result.columns.tolist()
    return pd.DataFrame(
        {
            "bb_lower": result[cols[0]],
            "bb_middle": result[cols[1]],
            "bb_upper": result[cols[2]],
        },
        index=series.index,
    )
