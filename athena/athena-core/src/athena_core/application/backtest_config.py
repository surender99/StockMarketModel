"""Backtest configuration — REQ-BT-ENGINE-001."""

from __future__ import annotations

from datetime import date

from pydantic import BaseModel, Field


class BacktestCostsConfig(BaseModel):
    """Transaction cost parameters."""

    brokerage_pct: float = Field(default=0.0003, ge=0)
    brokerage_flat: float = Field(default=20.0, ge=0)
    slippage_pct: float = Field(default=0.001, ge=0)
    stt_pct: float = Field(default=0.001, ge=0)
    gst_on_brokerage_pct: float = Field(default=0.18, ge=0)


class BacktestSettings(BaseModel):
    """Backtest settings without date range (from YAML)."""

    initial_capital: float = Field(default=1_000_000.0, gt=0)
    currency: str = "INR"
    costs: BacktestCostsConfig = Field(default_factory=BacktestCostsConfig)
    benchmark: str = "^NSEI"
    fill_price: str = "close"
    allow_fractional: bool = False


class BacktestConfig(BacktestSettings):
    """Backtest run settings — REQ-BT-ENGINE-001."""

    start: date
    end: date


class ExperimentTrackingConfig(BaseModel):
    """Experiment persistence settings — REQ-EXP-TRACK-001."""

    base_path: str = "./experiments"
    auto_capture_git: bool = True
    required_fields: list[str] = Field(
        default_factory=lambda: [
            "strategy_id",
            "strategy_version",
            "dataset_version",
            "train_start",
            "train_end",
            "metrics",
            "git_commit",
            "created_at",
        ]
    )
