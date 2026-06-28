"""Tests for daily scanner — REQ-SCANNER-001."""

from __future__ import annotations

from datetime import date, timedelta
from typing import Any

import pandas as pd

from athena_core.application.backtest_engine import FeatureProviderPort
from athena_core.application.explainability import ShapExplainer
from athena_core.application.ml_scorer import MLSignalScorer, SignalFeatures, TrainingSample
from athena_core.application.scanner import DailyScanner
from athena_core.application.scanner_config import ScannerConfig
from athena_core.domain.ports.ohlcv_repository import OHLCVRepositoryPort
from athena_core.domain.strategy.config import (
    EntryConfig,
    ExitConfig,
    ExitRuleSpec,
    IndicatorSpec,
    PositionSizingConfig,
    RuleSpec,
    StrategyConfig,
    StrategyMeta,
    UniverseConfig,
)


class _Repo(OHLCVRepositoryPort):
    def __init__(self, frames: dict[str, pd.DataFrame]) -> None:
        self._frames = frames

    def read(self, symbol: str, start: date | None = None, end: date | None = None) -> pd.DataFrame:
        df = self._frames.get(symbol, pd.DataFrame())
        if df.empty:
            return df
        out = df.copy()
        if start:
            out = out[out["date"] >= start]
        if end:
            out = out[out["date"] <= end]
        return out.reset_index(drop=True)

    def write(self, symbol: str, df: pd.DataFrame) -> int:
        return len(df)

    def exists(self, symbol: str) -> bool:
        return symbol in self._frames


class _Features(FeatureProviderPort):
    def get_indicator_frame(
        self,
        symbol: str,
        indicator_type: str,
        params: dict[str, Any],
        start: date | None,
        end: date | None,
    ) -> pd.DataFrame:
        return pd.DataFrame({"date": [], "ema_9": []})


def _series(symbol: str, start_close: float, drift: float, days: int = 80) -> pd.DataFrame:
    start = date(2024, 1, 2)
    dates = [start + timedelta(days=i) for i in range(days)]
    close = [start_close + drift * i for i in range(days)]
    return pd.DataFrame(
        {
            "date": dates,
            "open": close,
            "high": [c + 1 for c in close],
            "low": [c - 1 for c in close],
            "close": close,
            "volume": [500_000] * days,
            "symbol": [symbol] * days,
        }
    )


def _strategy() -> StrategyConfig:
    return StrategyConfig(
        strategy=StrategyMeta(id="scan_test", version="1.0.0"),
        universe=UniverseConfig(symbols=["STRONG", "WEAK"]),
        indicators=[IndicatorSpec(id="ema_fast", type="ema", params={"period": 9})],
        entry=EntryConfig(rules=[RuleSpec(condition="close > 0", side="long")]),
        exit=ExitConfig(rules=[ExitRuleSpec(condition="close < 0", reason="x")]),
        position_sizing=PositionSizingConfig(
            method="fixed_fraction",
            params={"fraction": 0.1, "max_positions": 2},
        ),
    )


def test_scanner_ranks_higher_momentum_first() -> None:
    as_of = date(2024, 1, 2) + timedelta(days=79)
    bench = _series("^NSEI", 100, 0.1)
    strong = _series("STRONG", 100, 1.0)
    weak = _series("WEAK", 100, 0.05)
    scanner = DailyScanner(
        _Repo({"^NSEI": bench, "STRONG": strong, "WEAK": weak}),
        _Features(),
        ScannerConfig(
            top_n=2, breakout_lookback_days=60, rs_lookback_days=20, momentum_lookback_days=20
        ),
    )
    result = scanner.scan(_strategy(), ["STRONG", "WEAK"], as_of)
    assert len(result.candidates) == 2
    assert result.candidates[0].symbol == "STRONG"
    assert result.candidates[0].score >= result.candidates[1].score
    assert result.candidates[0].reasons


def test_scanner_top_n_limit() -> None:
    as_of = date(2024, 1, 2) + timedelta(days=79)
    bench = _series("^NSEI", 100, 0.1)
    frames = {f"S{i}": _series(f"S{i}", 100, 0.2 + i * 0.1) for i in range(5)}
    frames["^NSEI"] = bench
    scanner = DailyScanner(_Repo(frames), _Features(), ScannerConfig(top_n=3))
    result = scanner.scan(_strategy(), [f"S{i}" for i in range(5)], as_of)
    assert len(result.candidates) <= 3


def test_scanner_empty_universe() -> None:
    scanner = DailyScanner(_Repo({}), _Features())
    result = scanner.scan(_strategy(), [], date(2024, 3, 1))
    assert result.candidates == []
    assert result.scanned_count == 0


def test_scanner_ml_scorer_augmented_signal_score() -> None:
    as_of = date(2024, 1, 2) + timedelta(days=79)
    bench = _series("^NSEI", 100, 0.1)
    strong = _series("STRONG", 100, 1.0)
    scorer = MLSignalScorer()
    samples = [
        TrainingSample(
            features=SignalFeatures(breakout_score=0.9, rs_score=0.8, momentum_score=0.85),
            label=1,
        ),
        TrainingSample(
            features=SignalFeatures(breakout_score=0.3, rs_score=0.4, momentum_score=0.35),
            label=0,
        ),
    ] * 12
    scorer.fit(samples)
    scanner = DailyScanner(
        _Repo({"^NSEI": bench, "STRONG": strong}),
        _Features(),
        ScannerConfig(top_n=1, use_ml_scorer=True),
        ml_scorer=scorer,
        explainer=ShapExplainer(),
    )
    result = scanner.scan(_strategy(), ["STRONG"], as_of)
    assert len(result.candidates) == 1
    candidate = result.candidates[0]
    assert candidate.has_entry_signal
    assert candidate.ml_probability is not None
    assert candidate.ml_rationale
