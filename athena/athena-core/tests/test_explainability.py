"""Tests for SHAP explainability — REQ-EXPLAIN-001."""

from __future__ import annotations

from athena_core.application.explainability import ShapExplainer
from athena_core.application.explainability_config import ExplainabilityConfig
from athena_core.application.ml_scorer import MLSignalScorer, SignalFeatures, TrainingSample


def _samples() -> list[TrainingSample]:
    rows: list[TrainingSample] = []
    for i in range(24):
        label = 1 if i % 2 == 0 else 0
        rows.append(
            TrainingSample(
                features=SignalFeatures(
                    breakout_score=0.5 + (0.15 if label else -0.15),
                    rs_score=0.5 + (0.1 if label else -0.1),
                    momentum_score=0.5 + (0.12 if label else -0.12),
                    volume_ratio=1.0 + (0.2 if label else -0.2),
                ),
                label=label,
            )
        )
    return rows


def test_explain_trained_model_returns_rationale() -> None:
    scorer = MLSignalScorer()
    scorer.fit(_samples())
    explainer = ShapExplainer(ExplainabilityConfig(enabled=True, top_features=3))
    result = explainer.explain(
        scorer,
        SignalFeatures(breakout_score=0.9, rs_score=0.75, momentum_score=0.8, volume_ratio=1.2),
    )
    assert 0.0 <= result.probability <= 1.0
    assert result.rationale
    assert "probability" in result.rationale.lower()


def test_explain_heuristic_when_untrained() -> None:
    scorer = MLSignalScorer()
    explainer = ShapExplainer()
    result = explainer.explain(
        scorer,
        SignalFeatures(breakout_score=0.95, rs_score=0.7, momentum_score=0.65),
    )
    assert result.rationale
    assert result.attributions == []


def test_explain_includes_feature_attributions_when_trained() -> None:
    scorer = MLSignalScorer()
    scorer.fit(_samples())
    explainer = ShapExplainer(ExplainabilityConfig(top_features=2, min_shap_magnitude=0.0))
    result = explainer.explain(
        scorer,
        SignalFeatures(breakout_score=0.85, rs_score=0.7, momentum_score=0.75),
    )
    assert len(result.attributions) >= 1
    assert result.attributions[0].label
