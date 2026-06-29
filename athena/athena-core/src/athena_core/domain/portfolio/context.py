"""Portfolio lifecycle context — ATH-REL-008 §5.1."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from athena_core.domain.portfolio.allocation import AllocationModelId
from athena_core.domain.portfolio.models import PortfolioState
from athena_core.domain.portfolio.risk_budget import RiskBudget


@dataclass
class PortfolioConfig:
    """Portfolio configuration — FR-003, FR-006."""

    allocation_model: AllocationModelId = "equal_weight"
    initial_capital: float = 100_000.0
    risk_budget: RiskBudget = field(default_factory=RiskBudget)
    currency: str = "INR"
    reserved_cash_pct: float = 0.05


@dataclass
class PortfolioContext:
    """Managed portfolio with metadata and mutable state — FR-001."""

    portfolio_id: str
    name: str
    config: PortfolioConfig
    state: PortfolioState
    metadata: dict[str, Any] = field(default_factory=dict)
    version: int = 1

    @property
    def free_cash(self) -> float:
        reserve = self.config.initial_capital * self.config.reserved_cash_pct
        return max(self.state.cash - reserve, 0.0)
