"""Tests for ML signal scorer — REQ-ML-SCORER-001."""

from __future__ import annotations

from datetime import date

import pytest

from athena_core.application.ml_scorer import (
    MLSignalScorer,
    SignalFeatures,
    TrainingSample,
)
from athena_core.application.ml_scorer_config import MLScorerConfig
from athena_core.domain.backtest.models import TradeRecord


def _trade(net_pnl: float) -> TradeRecord:
    return TradeRecord(
        symbol="TEST",
        side="long",
        entry_date=date(2024, 1, 2),
        exit_date=date(2024, 2, 1),
        entry_price=100.0,
        exit_price=100.0 + net_pnl,
        quantity=10,
        entry_fees=1.0,
        exit_fees=1.0,
        gross_pnl=net_pnl,
        net_pnl=net_pnl,
        exit_reason="signal",
    )


def _samples(n: int) -> list[TrainingSample]:
    rows: list[TrainingSample] = []
    for i in range(n):
        label = 1 if i % 2 == 0 else 0
        feat = SignalFeatures(
            breakout_score=0.5 + (0.1 if label else -0.1),
            rs_score=0.5 + (0.1 if label else -0.1),
            momentum_score=0.5 + (0.1 if label else -0.1),
            volume_ratio=1.0,
        )
        rows.append(TrainingSample(features=feat, label=label))
    return rows


def test_ml_scorer_trains_and_scores() -> None:
    scorer = MLSignalScorer(MLScorerConfig(min_training_samples=10, model_type="logistic"))
    scorer.fit(_samples(20))
    assert scorer.is_trained
    score = scorer.score(SignalFeatures(breakout_score=0.9, rs_score=0.8, momentum_score=0.85))
    assert 0.0 <= score.probability <= 1.0
    assert 0.0 <= score.confidence <= 1.0
    assert score.source == "ml"


def test_ml_scorer_fit_from_trades() -> None:
    trades = [_trade(10.0), _trade(-5.0)] * 12
    features = [
        SignalFeatures(breakout_score=0.8, rs_score=0.7, momentum_score=0.75),
        SignalFeatures(breakout_score=0.3, rs_score=0.4, momentum_score=0.35),
    ] * 12
    scorer = MLSignalScorer(MLScorerConfig(min_training_samples=10))
    scorer.fit_from_trades(trades, features)
    assert scorer.is_trained


def test_ml_scorer_heuristic_fallback() -> None:
    scorer = MLSignalScorer(MLScorerConfig(use_heuristic_fallback=True))
    score = scorer.score(SignalFeatures(breakout_score=0.9, rs_score=0.8, momentum_score=0.85))
    assert score.source == "heuristic"
    assert score.probability > 0.5


def test_ml_scorer_does_not_create_trades() -> None:
    """Scorer only scores; no trade generation API exists."""
    scorer = MLSignalScorer()
    assert not hasattr(scorer, "generate_trades")
    assert not hasattr(scorer, "create_signal")


def test_ml_scorer_insufficient_samples_raises() -> None:
    scorer = MLSignalScorer(MLScorerConfig(min_training_samples=20))
    with pytest.raises(ValueError, match="need at least"):
        scorer.fit(_samples(5))
