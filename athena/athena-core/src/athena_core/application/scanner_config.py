"""Daily scanner configuration — REQ-SCANNER-001."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ScannerWeightsConfig(BaseModel):
    """Scoring dimension weights — REQ-SCANNER-001."""

    breakout: float = Field(default=0.2, ge=0)
    relative_strength: float = Field(default=0.2, ge=0)
    momentum: float = Field(default=0.2, ge=0)
    signal_probability: float = Field(default=0.2, ge=0)
    pattern: float = Field(default=0.2, ge=0)


class ScannerConfig(BaseModel):
    """Daily universe scanner settings — REQ-SCANNER-001, REQ-ML-SCORER-001."""

    top_n: int = Field(default=20, ge=1)
    min_score: float = Field(default=0.0, ge=0, le=1)
    weights: ScannerWeightsConfig = Field(default_factory=ScannerWeightsConfig)
    breakout_lookback_days: int = Field(default=252, ge=5)
    momentum_lookback_days: int = Field(default=20, ge=2)
    rs_lookback_days: int = Field(default=63, ge=5)
    benchmark_symbol: str = "^NSEI"
    use_ml_scorer: bool = Field(
        default=False, description="Use ML scorer for signal_probability weight"
    )
    require_entry_signal: bool = Field(
        default=False,
        description="Only rank symbols with active strategy entry signals",
    )
    pattern_ids: list[str] = Field(
        default_factory=lambda: ["bullish_engulfing", "hammer", "morning_star"],
        description="Patterns contributing to scan score",
    )
    min_breadth_score: float | None = Field(
        default=None,
        ge=0,
        le=100,
        description="Skip scan when universe breadth score is below threshold",
    )
