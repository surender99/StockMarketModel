"""SHAP explainability for ML signal scores — REQ-EXPLAIN-001."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np
import structlog

from athena_core.application.explainability_config import ExplainabilityConfig
from athena_core.application.ml_scorer import MLSignalScorer, SignalFeatures

log = structlog.get_logger(__name__)

FEATURE_LABELS: dict[str, str] = {
    "breakout_score": "breakout proximity",
    "rs_score": "relative strength vs benchmark",
    "momentum_score": "price momentum",
    "volume_ratio": "volume vs average",
    "holding_days_norm": "expected holding period",
}


@dataclass(frozen=True)
class FeatureAttribution:
    """Single feature SHAP contribution — REQ-EXPLAIN-001."""

    feature: str
    label: str
    shap_value: float
    feature_value: float


@dataclass
class ExplanationResult:
    """Explainability bundle for one signal score — REQ-EXPLAIN-001."""

    probability: float
    confidence: float
    attributions: list[FeatureAttribution] = field(default_factory=list)
    rationale: str = ""


class ShapExplainer:
    """Feature attribution and plain-English rationale — REQ-EXPLAIN-001."""

    def __init__(self, config: ExplainabilityConfig | None = None) -> None:
        self._config = config or ExplainabilityConfig()

    def explain(
        self,
        scorer: MLSignalScorer,
        features: SignalFeatures,
    ) -> ExplanationResult:
        """Compute SHAP values and build rationale for one signal."""
        score = scorer.score(features)
        if not self._config.enabled or not scorer.is_trained or scorer.model is None:
            return ExplanationResult(
                probability=score.probability,
                confidence=score.confidence,
                attributions=[],
                rationale=self._heuristic_rationale(features, score.probability),
            )

        try:
            import shap
        except ImportError:
            log.warning("explainability.shap_unavailable")
            return ExplanationResult(
                probability=score.probability,
                confidence=score.confidence,
                rationale=self._heuristic_rationale(features, score.probability),
            )

        vector = features.to_vector(scorer.config.feature_names)
        model = scorer.model
        clf_step = model.named_steps["clf"]
        scaler = model.named_steps["scaler"]
        scaled = scaler.transform(vector.reshape(1, -1))

        attributions = self._compute_attributions(
            shap_module=shap,
            classifier=clf_step,
            scaled_input=scaled,
            raw_vector=vector,
            feature_names=scorer.config.feature_names,
        )
        rationale = self._build_rationale(attributions, score.probability)
        return ExplanationResult(
            probability=score.probability,
            confidence=score.confidence,
            attributions=attributions,
            rationale=rationale,
        )

    def _compute_attributions(
        self,
        *,
        shap_module: Any,
        classifier: Any,
        scaled_input: np.ndarray,
        raw_vector: np.ndarray,
        feature_names: list[str],
    ) -> list[FeatureAttribution]:
        try:
            if hasattr(classifier, "coef_"):
                explainer = shap_module.LinearExplainer(
                    classifier,
                    scaled_input,
                    feature_perturbation="interventional",
                )
            else:
                explainer = shap_module.TreeExplainer(classifier)
            shap_values = explainer.shap_values(scaled_input)
            if isinstance(shap_values, list):
                values = shap_values[1] if len(shap_values) > 1 else shap_values[0]
            else:
                values = shap_values
            row = np.asarray(values).reshape(-1)
        except Exception as exc:
            log.warning("explainability.shap_failed", error=str(exc))
            return self._fallback_attributions(raw_vector, feature_names)

        pairs = [
            (feature_names[i], float(row[i]), float(raw_vector[i]))
            for i in range(len(feature_names))
        ]
        pairs.sort(key=lambda p: abs(p[1]), reverse=True)
        top = pairs[: self._config.top_features]
        return [
            FeatureAttribution(
                feature=name,
                label=FEATURE_LABELS.get(name, name.replace("_", " ")),
                shap_value=shap_val,
                feature_value=feat_val,
            )
            for name, shap_val, feat_val in top
            if abs(shap_val) >= self._config.min_shap_magnitude
        ]

    @staticmethod
    def _fallback_attributions(
        vector: np.ndarray,
        feature_names: list[str],
    ) -> list[FeatureAttribution]:
        pairs = sorted(
            zip(feature_names, vector, strict=True),
            key=lambda p: abs(float(p[1])),
            reverse=True,
        )
        return [
            FeatureAttribution(
                feature=name,
                label=FEATURE_LABELS.get(name, name.replace("_", " ")),
                shap_value=float(val),
                feature_value=float(val),
            )
            for name, val in pairs[:3]
        ]

    def _build_rationale(
        self,
        attributions: list[FeatureAttribution],
        probability: float,
    ) -> str:
        if not attributions:
            return self._probability_phrase(probability)

        positive = [a for a in attributions if a.shap_value > 0]
        negative = [a for a in attributions if a.shap_value < 0]

        parts: list[str] = [self._probability_phrase(probability)]
        if positive:
            drivers = ", ".join(a.label for a in positive[:2])
            parts.append(f"Key positive drivers: {drivers}.")
        if negative and self._config.include_negative_factors:
            drag = ", ".join(a.label for a in negative[:2])
            parts.append(f"Headwinds: {drag}.")
        return " ".join(parts)

    @staticmethod
    def _heuristic_rationale(features: SignalFeatures, probability: float) -> str:
        parts = [ShapExplainer._probability_phrase(probability)]
        if features.momentum_score >= 0.6:
            parts.append("Strong momentum supports the signal.")
        if features.rs_score >= 0.6:
            parts.append("Relative strength vs benchmark is favorable.")
        if features.breakout_score >= 0.9:
            parts.append("Price is near the lookback high.")
        return " ".join(parts)

    @staticmethod
    def _probability_phrase(probability: float) -> str:
        pct = probability * 100
        if probability >= 0.65:
            return f"Model estimates {pct:.0f}% probability of a successful trade."
        if probability <= 0.35:
            return f"Model estimates only {pct:.0f}% probability of success."
        return f"Model estimates roughly even odds ({pct:.0f}% success probability)."
