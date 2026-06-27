"""ML signal scorer for strategy-generated trades — REQ-ML-SCORER-001."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np
import structlog
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from athena_core.application.ml_scorer_config import MLScorerConfig
from athena_core.domain.backtest.models import TradeRecord

log = structlog.get_logger(__name__)


@dataclass(frozen=True)
class SignalFeatures:
    """Feature vector at a strategy signal point — REQ-ML-SCORER-001."""

    breakout_score: float = 0.0
    rs_score: float = 0.0
    momentum_score: float = 0.0
    volume_ratio: float = 1.0
    holding_days_norm: float = 0.0
    extra: dict[str, float] = field(default_factory=dict)

    def to_vector(self, feature_names: list[str]) -> np.ndarray:
        base = {
            "breakout_score": self.breakout_score,
            "rs_score": self.rs_score,
            "momentum_score": self.momentum_score,
            "volume_ratio": self.volume_ratio,
            "holding_days_norm": self.holding_days_norm,
            **self.extra,
        }
        return np.array([float(base.get(name, 0.0)) for name in feature_names], dtype=float)


@dataclass(frozen=True)
class SignalScore:
    """ML probability output for one signal — REQ-ML-SCORER-001."""

    probability: float
    confidence: float
    source: str
    model_version: str = "untrained"


@dataclass(frozen=True)
class TrainingSample:
    """Labeled signal from backtest — REQ-ML-SCORER-001."""

    features: SignalFeatures
    label: int


class MLSignalScorer:
    """Scores strategy-generated signals; never creates trades — REQ-ML-SCORER-001."""

    def __init__(self, config: MLScorerConfig | None = None) -> None:
        self._config = config or MLScorerConfig()
        self._model: Pipeline | None = None
        self._model_version = "untrained"

    @property
    def is_trained(self) -> bool:
        return self._model is not None

    @property
    def config(self) -> MLScorerConfig:
        return self._config

    @property
    def model_version(self) -> str:
        return self._model_version

    @property
    def model(self) -> Pipeline | None:
        return self._model

    def fit(self, samples: list[TrainingSample]) -> None:
        """Train classifier on labeled strategy signal samples."""
        if len(samples) < self._config.min_training_samples:
            msg = (
                f"need at least {self._config.min_training_samples} samples, got {len(samples)}"
            )
            raise ValueError(msg)

        x = np.vstack([s.features.to_vector(self._config.feature_names) for s in samples])
        y = np.array([s.label for s in samples], dtype=int)

        if self._config.model_type == "random_forest":
            classifier: Any = RandomForestClassifier(
                n_estimators=50,
                max_depth=5,
                random_state=self._config.random_state,
            )
        else:
            classifier = LogisticRegression(max_iter=500, random_state=self._config.random_state)

        self._model = Pipeline([
            ("scaler", StandardScaler()),
            ("clf", classifier),
        ])
        self._model.fit(x, y)
        self._model_version = f"{self._config.model_type}_v1"
        log.info("ml_scorer.trained", samples=len(samples), model=self._model_version)

    def fit_from_trades(
        self,
        trades: list[TradeRecord],
        feature_rows: list[SignalFeatures],
    ) -> None:
        """Train from backtest trades and entry-time features (aligned by index)."""
        if len(trades) != len(feature_rows):
            msg = "trades and feature_rows must have equal length"
            raise ValueError(msg)
        samples = [
            TrainingSample(features=feat, label=1 if trade.net_pnl > 0 else 0)
            for trade, feat in zip(trades, feature_rows, strict=True)
        ]
        self.fit(samples)

    def score(self, features: SignalFeatures) -> SignalScore:
        """Return success probability for a strategy signal feature vector."""
        if self._model is None:
            if self._config.use_heuristic_fallback:
                heuristic = (
                    0.3 * features.breakout_score
                    + 0.3 * features.rs_score
                    + 0.4 * features.momentum_score
                )
                prob = min(max(heuristic, 0.0), 1.0)
                return SignalScore(
                    probability=prob,
                    confidence=abs(prob - 0.5) * 2,
                    source="heuristic",
                    model_version="heuristic_v1",
                )
            return SignalScore(probability=0.5, confidence=0.0, source="untrained")

        x = features.to_vector(self._config.feature_names).reshape(1, -1)
        proba = self._model.predict_proba(x)[0]
        success_idx = 1 if len(proba) > 1 else 0
        probability = float(proba[success_idx])
        confidence = float(abs(probability - 0.5) * 2)
        return SignalScore(
            probability=probability,
            confidence=confidence,
            source="ml",
            model_version=self._model_version,
        )

    def predict_proba_batch(self, features: list[SignalFeatures]) -> list[SignalScore]:
        """Score multiple signals."""
        return [self.score(f) for f in features]

    @staticmethod
    def features_from_scanner_scores(
        *,
        breakout: float,
        rs: float,
        momentum: float,
        volume_ratio: float = 1.0,
    ) -> SignalFeatures:
        """Build feature vector from scanner dimension scores."""
        return SignalFeatures(
            breakout_score=breakout,
            rs_score=rs,
            momentum_score=momentum,
            volume_ratio=volume_ratio,
        )

    @staticmethod
    def features_from_trade(trade: TradeRecord, *, volume_ratio: float = 1.0) -> SignalFeatures:
        """Minimal features when only trade record is available."""
        holding_days = max((trade.exit_date - trade.entry_date).days, 1)
        return SignalFeatures(
            volume_ratio=volume_ratio,
            holding_days_norm=min(holding_days / 60.0, 1.0),
        )
