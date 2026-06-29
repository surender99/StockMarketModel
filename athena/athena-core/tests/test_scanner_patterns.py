"""Scanner pattern integration tests — AES-0600, REQ-PAT-001."""

from __future__ import annotations

from datetime import date, timedelta

import pandas as pd

from athena_core.application.backtest_engine import FeatureProviderPort
from athena_core.application.scanner import DailyScanner
from athena_core.application.scanner_config import ScannerConfig, ScannerWeightsConfig
from athena_core.domain.patterns.base import PatternDetector
from tests.memory_ohlcv_repo import MemoryOHLCVRepo
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


class _Features(FeatureProviderPort):
    def get_indicator_frame(self, symbol, indicator_type, params, start, end):
        return pd.DataFrame({"date": [], "ema_9": []})


def _strategy() -> StrategyConfig:
    return StrategyConfig(
        strategy=StrategyMeta(id="pat_scan", version="1.0.0"),
        universe=UniverseConfig(symbols=["PAT"]),
        indicators=[IndicatorSpec(id="ema_fast", type="ema", params={"period": 9})],
        entry=EntryConfig(rules=[RuleSpec(condition="close > 0", side="long")]),
        exit=ExitConfig(rules=[ExitRuleSpec(condition="close < 0", reason="x")]),
        position_sizing=PositionSizingConfig(
            method="fixed_fraction",
            params={"fraction": 0.1, "max_positions": 2},
        ),
    )


def test_scanner_pattern_score_boosts_candidate() -> None:
    start = date(2024, 1, 2)
    dates = [start + timedelta(days=i) for i in range(5)]
    bench = pd.DataFrame(
        {
            "date": dates,
            "open": [100, 101, 102, 103, 104],
            "high": [101, 102, 103, 104, 105],
            "low": [99, 100, 101, 102, 103],
            "close": [100, 101, 102, 103, 104],
            "volume": [1000] * 5,
            "symbol": ["^NSEI"] * 5,
        }
    )
    pat = pd.DataFrame(
        {
            "date": dates,
            "open": [100, 101, 102, 110, 100],
            "high": [101, 102, 103, 112, 115],
            "low": [99, 100, 101, 100, 99],
            "close": [100.5, 101.5, 102.5, 101, 114],
            "volume": [1000] * 5,
            "symbol": ["PAT"] * 5,
        }
    )
    as_of = dates[-1]
    scanner = DailyScanner(
        MemoryOHLCVRepo({"^NSEI": bench, "PAT": pat}),
        _Features(),
        ScannerConfig(
            top_n=1,
            weights=ScannerWeightsConfig(
                breakout=0.0,
                relative_strength=0.0,
                momentum=0.0,
                signal_probability=0.0,
                pattern=1.0,
            ),
            pattern_ids=["bullish_engulfing"],
        ),
        pattern_detector=PatternDetector(),
    )
    result = scanner.scan(_strategy(), ["PAT"], as_of)
    assert len(result.candidates) == 1
    candidate = result.candidates[0]
    assert candidate.pattern_score > 0
    assert any("bullish engulfing" in r for r in candidate.reasons)
