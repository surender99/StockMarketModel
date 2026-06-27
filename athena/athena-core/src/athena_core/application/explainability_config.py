"""SHAP explainability configuration — REQ-EXPLAIN-001."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ExplainabilityConfig(BaseModel):
    """SHAP and rationale settings — REQ-EXPLAIN-001."""

    enabled: bool = True
    top_features: int = Field(default=3, ge=1, le=20)
    min_shap_magnitude: float = Field(default=0.01, ge=0)
    include_negative_factors: bool = True
