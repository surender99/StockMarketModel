"""Strategy optimizer configuration — REQ-OPT-001."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator


class ParameterSpec(BaseModel):
    """One tunable strategy parameter — REQ-OPT-001."""

    path: str = Field(description="Dot path, e.g. risk.stop_loss_pct or indicators.ema_fast.params.period")
    type: Literal["int", "float", "choice"] = "float"
    values: list[Any] | None = Field(default=None, description="Grid/choice values")
    min: float | None = None
    max: float | None = None
    step: float | None = None

    @model_validator(mode="after")
    def validate_range(self) -> ParameterSpec:
        if self.type == "choice":
            if not self.values:
                msg = "choice parameters require values list"
                raise ValueError(msg)
            return self
        if self.values:
            return self
        if self.min is None or self.max is None:
            msg = f"{self.type} parameters require min/max or explicit values"
            raise ValueError(msg)
        if self.min > self.max:
            msg = "parameter min must be <= max"
            raise ValueError(msg)
        return self


class OptimizerConfig(BaseModel):
    """Walk-forward parameter search settings — REQ-OPT-001."""

    method: Literal["grid", "random", "bayesian"] = "grid"
    max_trials: int = Field(default=50, ge=1)
    random_seed: int = 42
    parameters: list[ParameterSpec] = Field(default_factory=list)
    objectives: list[str] = Field(
        default_factory=lambda: ["sharpe", "max_drawdown", "profit_factor"],
    )
    objective_weights: dict[str, float] = Field(
        default_factory=lambda: {
            "sharpe": 0.4,
            "max_drawdown": 0.3,
            "profit_factor": 0.3,
        },
    )

    @model_validator(mode="after")
    def validate_objectives(self) -> OptimizerConfig:
        if not self.objectives:
            msg = "optimizer requires at least one objective"
            raise ValueError(msg)
        return self
