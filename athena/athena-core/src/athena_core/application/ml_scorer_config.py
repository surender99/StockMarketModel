"""ML signal scorer configuration — REQ-ML-SCORER-001."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field


class MLScorerConfig(BaseModel):
    """Settings for trade signal probability model — REQ-ML-SCORER-001."""

    enabled: bool = False
    model_type: Literal["logistic", "random_forest"] = "logistic"
    min_training_samples: int = Field(default=20, ge=5)
    probability_threshold: float = Field(default=0.5, ge=0, le=1)
    model_path: Path | None = Field(default=None, description="Optional persisted model path")
    random_state: int = 42
    use_heuristic_fallback: bool = True
    feature_names: list[str] = Field(
        default_factory=lambda: [
            "breakout_score",
            "rs_score",
            "momentum_score",
            "volume_ratio",
            "holding_days_norm",
        ],
    )
