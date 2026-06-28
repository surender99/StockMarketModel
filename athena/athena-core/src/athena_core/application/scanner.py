"""Daily universe scanner — REQ-SCANNER-001, REQ-ML-SCORER-001, REQ-EXPLAIN-001."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Any

import pandas as pd
import structlog

from athena_core.application.backtest_engine import FeatureProviderPort
from athena_core.application.breadth_engine import BreadthEngine
from athena_core.application.explainability import ShapExplainer
from athena_core.application.ml_scorer import MLSignalScorer
from athena_core.application.regime_engine import RegimeEngine
from athena_core.application.scanner_config import ScannerConfig
from athena_core.domain.patterns.base import PatternDetector
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
    pattern_score: float = 0.0
    pattern_reasons: list[str] = field(default_factory=list)
    has_entry_signal: bool = False
    ml_probability: float | None = None
    ml_confidence: float | None = None
    ml_rationale: str | None = None
    ml_attributions: list[dict[str, Any]] | None = None


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
        ml_scorer: MLSignalScorer | None = None,
        explainer: ShapExplainer | None = None,
        pattern_detector: PatternDetector | None = None,
        breadth_engine: BreadthEngine | None = None,
    ) -> None:
        self._ohlcv = ohlcv_repo
        self._features = feature_provider
        self._config = config or ScannerConfig()
        self._regime = regime_engine
        self._ml_scorer = ml_scorer
        self._explainer = explainer
        self._patterns = pattern_detector or PatternDetector()
        self._breadth = breadth_engine

    def scan(
        self,
        strategy: StrategyConfig,
        symbols: list[str],
        as_of: date,
    ) -> ScanResult:
        """Evaluate symbols and return top-N ranked candidates."""
        if not symbols:
            return ScanResult(as_of=as_of, candidates=[], scanned_count=0, filtered_count=0)

        if self._config.min_breadth_score is not None and self._breadth is not None:
            breadth = self._breadth.compute(symbols, as_of)
            if breadth.breadth_score < self._config.min_breadth_score:
                return ScanResult(
                    as_of=as_of,
                    candidates=[],
                    scanned_count=len(symbols),
                    filtered_count=len(symbols),
                )

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
            if self._config.require_entry_signal and not has_signal:
                filtered += 1
                continue

            breakout = self._breakout_score(frame, idx)
            rs = self._relative_strength_score(frame, benchmark, as_of)
            momentum = self._momentum_score(frame, idx)
            volume_ratio = self._volume_ratio(frame, idx)
            pattern_score, pattern_reasons = self._pattern_score(frame, idx)

            ml_probability: float | None = None
            ml_confidence: float | None = None
            ml_rationale: str | None = None
            ml_attributions: list[dict[str, Any]] | None = None

            if has_signal and self._config.use_ml_scorer and self._ml_scorer is not None:
                feat = MLSignalScorer.features_from_scanner_scores(
                    breakout=breakout,
                    rs=rs,
                    momentum=momentum,
                    volume_ratio=volume_ratio,
                )
                ml_score = self._ml_scorer.score(feat)
                ml_probability = round(ml_score.probability, 4)
                ml_confidence = round(ml_score.confidence, 4)
                signal_score = ml_score.probability
                if self._explainer is not None:
                    explanation = self._explainer.explain(self._ml_scorer, feat)
                    ml_rationale = explanation.rationale
                    if explanation.attributions:
                        ml_attributions = [
                            {
                                "feature": attr.feature,
                                "label": attr.label,
                                "shap_value": round(attr.shap_value, 6),
                                "feature_value": round(attr.feature_value, 4),
                            }
                            for attr in explanation.attributions
                        ]
            else:
                signal_score = 1.0 if has_signal else 0.0
            composite = (
                weights["breakout"] * breakout
                + weights["relative_strength"] * rs
                + weights["momentum"] * momentum
                + weights["signal_probability"] * signal_score
                + weights["pattern"] * pattern_score
            )
            if composite < self._config.min_score:
                filtered += 1
                continue

            reasons = self._build_reasons(
                breakout=breakout,
                rs=rs,
                momentum=momentum,
                has_signal=has_signal,
                ml_rationale=ml_rationale,
                pattern_reasons=pattern_reasons,
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
                    pattern_score=round(pattern_score, 4),
                    pattern_reasons=pattern_reasons,
                    has_entry_signal=has_signal,
                    ml_probability=ml_probability,
                    ml_confidence=ml_confidence,
                    ml_rationale=ml_rationale,
                    ml_attributions=ml_attributions,
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
                "breakout": 0.2,
                "relative_strength": 0.2,
                "momentum": 0.2,
                "signal_probability": 0.2,
                "pattern": 0.2,
            }
        return {
            "breakout": w.breakout / total,
            "relative_strength": w.relative_strength / total,
            "momentum": w.momentum / total,
            "signal_probability": w.signal_probability / total,
            "pattern": w.pattern / total,
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
            elif filt.type == "breadth":
                if self._breadth is None:
                    continue
                universe = filt.params.get("universe_symbols", [])
                if not universe:
                    continue
                metrics = self._breadth.compute(universe, session)
                min_score = float(filt.params.get("min_breadth_score", 0))
                if metrics.breadth_score < min_score:
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

    def _pattern_score(self, frame: pd.DataFrame, idx: int) -> tuple[float, list[str]]:
        """Score bullish patterns on the as-of bar — AES-0600."""
        window = frame.iloc[: idx + 1]
        if window.empty:
            return 0.0, []
        score = 0.0
        reasons: list[str] = []
        for pattern_id in self._config.pattern_ids:
            events = self._patterns.detect(window, pattern_id)
            on_bar = [e for e in events if e.bar_index == idx]
            if not on_bar:
                continue
            best = max(on_bar, key=lambda e: e.confidence)
            score = max(score, best.confidence)
            reasons.append(f"{pattern_id.replace('_', ' ')} detected (conf {best.confidence:.2f})")
        return min(score, 1.0), reasons

    @staticmethod
    def _volume_ratio(frame: pd.DataFrame, idx: int) -> float:
        if "volume" not in frame.columns:
            return 1.0
        window = frame["volume"].iloc[max(0, idx - 19) : idx + 1].astype(float)
        if window.empty:
            return 1.0
        avg = float(window.mean())
        if avg <= 0:
            return 1.0
        return min(float(window.iloc[-1]) / avg, 3.0)

    @staticmethod
    def _build_reasons(
        *,
        breakout: float,
        rs: float,
        momentum: float,
        has_signal: bool,
        ml_rationale: str | None = None,
        pattern_reasons: list[str] | None = None,
    ) -> list[str]:
        reasons: list[str] = []
        if ml_rationale:
            reasons.append(ml_rationale)
        if pattern_reasons:
            reasons.extend(pattern_reasons)
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
        return scan_result_to_dict(result)


def scan_result_to_dict(result: ScanResult) -> dict[str, Any]:
    """Serialize scan result for CLI, SDK, and dashboard."""
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
                "pattern_score": c.pattern_score,
                "pattern_reasons": c.pattern_reasons,
                "has_entry_signal": c.has_entry_signal,
                "ml_probability": c.ml_probability,
                "ml_confidence": c.ml_confidence,
                "ml_rationale": c.ml_rationale,
                "ml_attributions": c.ml_attributions,
            }
            for c in result.candidates
        ],
    }
