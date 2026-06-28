"""Market regime classification — REQ-REGIME-001."""

from __future__ import annotations

from datetime import date

import pandas as pd
import structlog

from athena_core.application.regime_config import RegimeConfig
from athena_core.domain.ports.ohlcv_repository import OHLCVRepositoryPort
from athena_core.domain.regime.indicators import compute_regime_features
from athena_core.domain.regime.models import RegimeState, TrendRegime, VolatilityRegime

log = structlog.get_logger(__name__)


class RegimeEngine:
    """Classify trend and volatility regimes — REQ-REGIME-001."""

    def __init__(
        self,
        ohlcv_repo: OHLCVRepositoryPort,
        config: RegimeConfig | None = None,
    ) -> None:
        self._ohlcv = ohlcv_repo
        self._config = config or RegimeConfig()

    def build_regime_series(
        self,
        symbol: str,
        start: date | None = None,
        end: date | None = None,
    ) -> pd.DataFrame:
        """Return date-indexed regime labels using data ≤ each row's date."""
        ohlcv = self._ohlcv.read(symbol, start=start, end=end)
        if ohlcv.empty:
            return pd.DataFrame(
                columns=["date", "trend", "volatility", "adx", "atr_pct", "rolling_vol"]
            )

        features = compute_regime_features(
            ohlcv,
            ema_fast_period=self._config.ema_fast_period,
            ema_slow_period=self._config.ema_slow_period,
            adx_period=self._config.adx_period,
            atr_period=self._config.atr_period,
            rolling_vol_window=self._config.rolling_vol_window,
        )
        vol_threshold = self._vol_threshold(features["rolling_vol"])
        trends: list[str] = []
        vols: list[str] = []
        for _, row in features.iterrows():
            trends.append(self._classify_trend(row).value)
            vols.append(self._classify_volatility(float(row["rolling_vol"]), vol_threshold).value)

        out = features[["date", "adx", "atr_pct", "rolling_vol"]].copy()
        out["trend"] = trends
        out["volatility"] = vols
        return out

    def classify_as_of(
        self,
        symbol: str,
        as_of: date,
        *,
        nifty_trend: TrendRegime | None = None,
    ) -> RegimeState | None:
        """Regime state for a single date (no lookahead)."""
        series = self.build_regime_series(symbol, end=as_of)
        if series.empty:
            return None
        matches = series[series["date"] == as_of]
        if matches.empty:
            matches = series.iloc[[-1]]
        row = matches.iloc[-1]
        return RegimeState(
            as_of=row["date"],
            trend=TrendRegime(row["trend"]),
            volatility=VolatilityRegime(row["volatility"]),
            adx=float(row["adx"]) if pd.notna(row["adx"]) else 0.0,
            atr_pct=float(row["atr_pct"]) if pd.notna(row["atr_pct"]) else 0.0,
            rolling_vol=float(row["rolling_vol"]) if pd.notna(row["rolling_vol"]) else 0.0,
            nifty_trend=nifty_trend,
        )

    def benchmark_trend_as_of(self, as_of: date) -> TrendRegime | None:
        """NIFTY/benchmark trend at as_of — REQ-REGIME-001."""
        state = self.classify_as_of(self._config.benchmark_symbol, as_of)
        return state.trend if state else None

    def _classify_trend(self, row: pd.Series) -> TrendRegime:
        close = float(row["close"])
        ema_fast = row["ema_fast"]
        ema_slow = row["ema_slow"]
        adx = row["adx"]
        if pd.isna(ema_fast) or pd.isna(ema_slow):
            return TrendRegime.SIDEWAYS
        if pd.notna(adx) and float(adx) < self._config.adx_sideways_threshold:
            return TrendRegime.SIDEWAYS
        if close > float(ema_slow) and float(ema_fast) > float(ema_slow):
            return TrendRegime.BULL
        if close < float(ema_slow) and float(ema_fast) < float(ema_slow):
            return TrendRegime.BEAR
        return TrendRegime.SIDEWAYS

    def _vol_threshold(self, rolling_vol: pd.Series) -> float:
        valid = rolling_vol.dropna()
        if valid.empty:
            return 0.0
        lookback = valid.iloc[-self._config.vol_lookback_days :]
        return float(lookback.quantile(self._config.vol_high_percentile))

    @staticmethod
    def _classify_volatility(rolling_vol: float, threshold: float) -> VolatilityRegime:
        if rolling_vol >= threshold:
            return VolatilityRegime.HIGH
        return VolatilityRegime.LOW
