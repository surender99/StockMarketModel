"""Strategy configuration schema — REQ-STRAT-CONFIG-001, REQ-REGIME-001."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator, model_validator

from athena_core.domain.regime.models import TrendRegime, VolatilityRegime


class StrategyMeta(BaseModel):
    """Strategy identity block."""

    id: str
    version: str
    description: str = ""


class UniverseConfig(BaseModel):
    """Universe selection."""

    source: str = "custom"
    symbols: list[str] = Field(default_factory=list)


class IndicatorSpec(BaseModel):
    """Indicator referenced by strategy rules."""

    id: str
    type: str
    params: dict[str, Any] = Field(default_factory=dict)

    @field_validator("id")
    @classmethod
    def id_not_empty(cls, value: str) -> str:
        if not value.strip():
            msg = "indicator id must not be empty"
            raise ValueError(msg)
        return value


class RuleSpec(BaseModel):
    """Entry rule with side."""

    condition: str
    side: Literal["long"] = "long"


class ExitRuleSpec(BaseModel):
    """Exit rule with reason label."""

    condition: str
    reason: str = "signal"


class EntryConfig(BaseModel):
    """Entry rule block."""

    rules: list[RuleSpec] = Field(min_length=1)


class ExitConfig(BaseModel):
    """Exit rule block."""

    rules: list[ExitRuleSpec] = Field(min_length=1)


class FilterSpec(BaseModel):
    """Pre-entry filter — REQ-STRAT-CONFIG-001, REQ-REGIME-001."""

    type: str
    params: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_regime_filter(self) -> FilterSpec:
        if self.type != "regime":
            return self
        trends = self.params.get("allowed_trends", [])
        vols = self.params.get("allowed_volatility", [])
        valid_trends = {r.value for r in TrendRegime}
        valid_vols = {r.value for r in VolatilityRegime}
        for trend in trends:
            if trend not in valid_trends:
                msg = f"invalid trend in regime filter: {trend}"
                raise ValueError(msg)
        for vol in vols:
            if vol not in valid_vols:
                msg = f"invalid volatility in regime filter: {vol}"
                raise ValueError(msg)
        if not trends and not vols:
            msg = "regime filter requires allowed_trends and/or allowed_volatility"
            raise ValueError(msg)
        return self


class PositionSizingConfig(BaseModel):
    """Position sizing method and parameters."""

    method: Literal["fixed_fraction", "fixed_amount"] = "fixed_fraction"
    params: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_params(self) -> PositionSizingConfig:
        if self.method == "fixed_fraction":
            fraction = float(self.params.get("fraction", 0.05))
            max_positions = int(self.params.get("max_positions", 10))
            if not 0 < fraction <= 1:
                msg = "fixed_fraction requires 0 < fraction <= 1"
                raise ValueError(msg)
            if max_positions < 1:
                msg = "max_positions must be >= 1"
                raise ValueError(msg)
        elif self.method == "fixed_amount":
            amount = float(self.params.get("amount", 0))
            if amount <= 0:
                msg = "fixed_amount requires amount > 0"
                raise ValueError(msg)
        return self


class RiskConfig(BaseModel):
    """Stop, target, and holding limits."""

    stop_loss_pct: float | None = Field(default=None, ge=0, le=1)
    take_profit_pct: float | None = Field(default=None, ge=0)
    max_holding_days: int | None = Field(default=None, ge=1)


class StrategyConfig(BaseModel):
    """Validated strategy configuration — REQ-STRAT-CONFIG-001."""

    strategy: StrategyMeta
    universe: UniverseConfig
    indicators: list[IndicatorSpec] = Field(default_factory=list)
    entry: EntryConfig
    exit: ExitConfig
    filters: list[FilterSpec] = Field(default_factory=list)
    position_sizing: PositionSizingConfig
    risk: RiskConfig = Field(default_factory=RiskConfig)

    @model_validator(mode="after")
    def unique_indicator_ids(self) -> StrategyConfig:
        ids = [spec.id for spec in self.indicators]
        if len(ids) != len(set(ids)):
            msg = "indicator ids must be unique"
            raise ValueError(msg)
        return self

    def indicator_ids(self) -> set[str]:
        """Return declared indicator ids."""
        return {spec.id for spec in self.indicators}

    def model_dump_roundtrip(self) -> dict[str, Any]:
        """Serialize for config round-trip tests."""
        return self.model_dump(mode="json")
