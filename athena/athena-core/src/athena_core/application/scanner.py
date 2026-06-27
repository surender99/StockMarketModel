"""Daily universe scanner — REQ-SCANNER-001."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Any

import pandas as pd
import structlog

from athena_core.application.backtest_engine import FeatureProviderPort
from athena_core.application.regime_engine import RegimeEngine
from athena_core.application.scanner_config import ScannerConfig
from athena_core.domain.ports.ohlcv_repository import OHLCVRepositoryPort
from athena_core.domain.strategy.config import StrategyConfig
from athena_core.domain.strategy.expression import evaluate_condition_at_index
from athena_core.domain.strategy.indicators import indicator_column_name, indicator_feature_id

log = structlog.get_logger(__name__)


@dataclass(frozen=True)
class ScanCandidate:
    """Ranked scan result with explainable reasons — REQ-SCANNER-001."""

    symbol: str
    score: float
    reasons: list[str] = field(default_factory=list)
    breakout_score: float = 0.0
    rs_score: float = 0.0
    momentum_score: float = 0.0
    signal_score: float = 0.0
    has_entry_signal: bool = False


@dataclass(frozen=True)
class ScanResult:
    """Scanner output bundle — REQ-SCANNER-001."""

    as_of: date
    candidates: list[ScanCandidate]
    scanned_count: int
    filtered_count: int


class DailyScanner:
    """Batch-evaluate universe and rank candidates — REQ-SCANNER-001."""

    def __init__(
        self,
        ohlcv_repo: OHLCVRepositoryPort,
        feature_provider: FeatureProviderPort,
        config: ScannerConfig | None = None,
        regime_engine: RegimeEngine | None = None,
    ) -> None:
        self._ohlcv = ohlcv_repo
        self._features = feature_provider
        self._config = config or ScannerConfig()
        self._regime = regime_engine

    def scan(
        self,
        strategy: StrategyConfig,
        symbols: list[str],
        as_of: date,
    ) -> ScanResult:
        """Evaluate symbols and return top-N ranked candidates."""
        if not symbols:
            return ScanResult(as_of=as_of, candidates=[], scanned_count=0, filtered_count=0)

        benchmark = self._load_benchmark(as_of)
        weights = self._normalized_weights()
        candidates: list[ScanCandidate] = []
        filtered = 0

        for symbol in symbols:
            frame = self._build_symbol_frame(strategy, symbol, as_of)
            if frame is None or frame.empty:
                filtered += 1
                continue
            idx = self._index_for_date(frame, as_of)
            if idx is None:
                filtered += 1
                continue
            if not self._passes_filters(strategy, frame, as_of, idx):
                filtered += 1
                continue

            has_signal = self._has_entry_signal(strategy, frame, idx)
            breakout = self._breakout_score(frame, idx)
            rs = self._relative_strength_score(frame, benchmark, as_of)
            momentum = self._momentum_score(frame, idx)
            signal_score = 1.0 if has_signal else 0.0
            composite = (
                weights["breakout"] * breakout
                + weights["relative_strength"] * rs
                + weights["momentum"] * momentum
                + weights["signal_probability"] * signal_score
            )
            if composite < self._config.min_score:
                filtered += 1
                continue

            reasons = self._build_reasons(
                breakout=breakout,
                rs=rs,
                momentum=momentum,
                has_signal=has_signal,
            )
            candidates.append(
                ScanCandidate(
                    symbol=symbol,
                    score=round(composite, 4),
                    reasons=reasons,
                    breakout_score=round(breakout, 4),
                    rs_score=round(rs, 4),
                    momentum_score=round(momentum, 4),
                    signal_score=round(signal_score, 4),
                    has_entry_signal=has_signal,
                )
            )

        candidates.sort(key=lambda c: c.score, reverse=True)
        top = candidates[: self._config.top_n]
        return ScanResult(
            as_of=as_of,
            candidates=top,
            scanned_count=len(symbols),
            filtered_count=filtered,
        )

    def _normalized_weights(self) -> dict[str, float]:
        w = self._config.weights
        total = w.breakout + w.relative_strength + w.momentum + w.signal_probability
        if total <= 0:
            return {
                "breakout": 0.25,
                "relative_strength": 0.25,
                "momentum": 0.25,
                "signal_probability": 0.25,
            }
        return {
            "breakout": w.breakout / total,
            "relative_strength": w.relative_strength / total,
            "momentum": w.momentum / total,
            "signal_probability": w.signal_probability / total,
        }

    def _load_benchmark(self, as_of: date) -> pd.DataFrame:
        start = as_of - timedelta(
            days=max(self._config.breakout_lookback_days, self._config.rs_lookback_days) + 30
        )
        df = self._ohlcv.read(self._config.benchmark_symbol, start=start, end=as_of)
        return df.sort_values("date").reset_index(drop=True)

    def _build_symbol_frame(
        self,
        strategy: StrategyConfig,
        symbol: str,
        as_of: date,
    ) -> pd.DataFrame | None:
        start = as_of - timedelta(days=max(self._config.breakout_lookback_days, 300))
        ohlcv = self._ohlcv.read(symbol, start=start, end=as_of)
        if ohlcv.empty:
            return None
        frame = ohlcv.sort_values("date").reset_index(drop=True)
        for spec in strategy.indicators:
            feature_id = indicator_feature_id(spec.type)
            indicator_df = self._features.get_indicator_frame(
                symbol,
                feature_id,
                spec.params,
                start,
                as_of,
            )
            col = indicator_column_name(spec)
            merged = indicator_df.sort_values("date").reset_index(drop=True)
            value_col = next(c for c in merged.columns if c != "date")
            indicator_values = merged.rename(columns={value_col: col})[["date", col]]
            frame = frame.merge(indicator_values, on="date", how="left")
            frame[spec.id] = frame[col]
        return frame

    @staticmethod
    def _index_for_date(frame: pd.DataFrame, session: date) -> int | None:
        matches = frame.index[frame["date"] == session].tolist()
        if not matches:
            return None
        return int(matches[0])

    def _passes_filters(
        self,
        strategy: StrategyConfig,
        frame: pd.DataFrame,
        session: date,
        idx: int,
    ) -> bool:
        for filt in strategy.filters:
            if filt.type == "min_volume":
                min_avg = float(filt.params.get("min_avg_volume_20d", 0))
                if "volume" not in frame.columns:
                    return False
                window = frame["volume"].iloc[max(0, idx - 19) : idx + 1]
                if window.mean() < min_avg:
                    return False
            elif filt.type == "regime":
                if self._regime is None:
                    continue
                state = self._regime.classify_as_of(
                    self._regime._config.benchmark_symbol,
                    session,
                )
                if state is None:
                    return False
                allowed_trends = filt.params.get("allowed_trends", [])
                allowed_vols = filt.params.get("allowed_volatility", [])
                if allowed_trends and state.trend.value not in allowed_trends:
                    return False
                if allowed_vols and state.volatility.value not in allowed_vols:
                    return False
        return True

    @staticmethod
    def _has_entry_signal(strategy: StrategyConfig, frame: pd.DataFrame, idx: int) -> bool:
        indicator_map = {spec.id: indicator_column_name(spec) for spec in strategy.indicators}
        for rule in strategy.entry.rules:
            if rule.side != "long":
                continue
            if evaluate_condition_at_index(rule.condition, frame, indicator_map, idx):
                return True
        return False

    def _breakout_score(self, frame: pd.DataFrame, idx: int) -> float:
        lookback = self._config.breakout_lookback_days
        start = max(0, idx - lookback + 1)
        window = frame["close"].iloc[start : idx + 1].astype(float)
        if window.empty:
            return 0.0
        high = float(window.max())
        close = float(window.iloc[-1])
        if high <= 0:
            return 0.0
        return min(max(close / high, 0.0), 1.0)

    def _relative_strength_score(
        self,
        frame: pd.DataFrame,
        benchmark: pd.DataFrame,
        as_of: date,
    ) -> float:
        lookback = self._config.rs_lookback_days
        sym = frame[frame["date"] <= as_of].tail(lookback + 1)
        bench = benchmark[benchmark["date"] <= as_of].tail(lookback + 1)
        if len(sym) < 2 or len(bench) < 2:
            return 0.0
        sym_ret = float(sym["close"].iloc[-1]) / float(sym["close"].iloc[0]) - 1.0
        bench_ret = float(bench["close"].iloc[-1]) / float(bench["close"].iloc[0]) - 1.0
        rs = sym_ret - bench_ret
        return min(max(0.5 + rs, 0.0), 1.0)

    def _momentum_score(self, frame: pd.DataFrame, idx: int) -> float:
        lookback = self._config.momentum_lookback_days
        start = max(0, idx - lookback)
        window = frame["close"].iloc[start : idx + 1].astype(float)
        if len(window) < 2:
            return 0.0
        roc = float(window.iloc[-1]) / float(window.iloc[0]) - 1.0
        return min(max(0.5 + roc, 0.0), 1.0)

    @staticmethod
    def _build_reasons(
        *,
        breakout: float,
        rs: float,
        momentum: float,
        has_signal: bool,
    ) -> list[str]:
        reasons: list[str] = []
        if breakout >= 0.95:
            reasons.append(f"near {breakout:.0%} of lookback high (breakout)")
        elif breakout >= 0.85:
            reasons.append(f"approaching lookback high ({breakout:.0%})")
        if rs >= 0.6:
            reasons.append(f"relative strength vs benchmark ({rs:.2f})")
        if momentum >= 0.6:
            reasons.append(f"positive momentum ({momentum:.2f})")
        if has_signal:
            reasons.append("strategy entry signal active")
        if not reasons:
            reasons.append("composite score above threshold")
        return reasons

    def candidates_to_dict(self, result: ScanResult) -> dict[str, Any]:
        """Serialize scan result for CLI/JSON output."""
        return {
            "as_of": result.as_of.isoformat(),
            "scanned_count": result.scanned_count,
            "filtered_count": result.filtered_count,
            "candidates": [
                {
                    "symbol": c.symbol,
                    "score": c.score,
                    "reasons": c.reasons,
                    "breakout_score": c.breakout_score,
                    "rs_score": c.rs_score,
                    "momentum_score": c.momentum_score,
                    "signal_score": c.signal_score,
                    "has_entry_signal": c.has_entry_signal,
                }
                for c in result.candidates
            ],
        }
