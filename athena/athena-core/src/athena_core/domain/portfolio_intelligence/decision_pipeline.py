"""Portfolio decision pipeline — PHASE 7 PIP staged allocation flow."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Callable

from athena_core.application.portfolio_engine import PortfolioEngine
from athena_core.application.portfolio_optimizer import minimum_variance_weights
from athena_core.application.portfolio_risk import PortfolioLimits, PortfolioRiskService
from athena_core.domain.portfolio.allocation import compute_allocation_weights
from athena_core.domain.portfolio.context import PortfolioConfig
from athena_core.domain.portfolio.models import PortfolioState
from athena_core.domain.portfolio.risk_budget import passes_risk_budget

DECISION_STAGES: tuple[str, ...] = (
    "trade_recommendations",
    "constraint_evaluation",
    "risk_budget_allocation",
    "portfolio_construction",
    "optimization",
    "rebalancing_decision",
    "execution_proposal",
)

StageHandler = Callable[["PortfolioDecisionContext", dict[str, Any]], dict[str, Any]]


@dataclass(frozen=True, slots=True)
class TradeRecommendation:
    """Strategy output — WHAT to buy."""

    symbol: str
    side: str
    conviction: float = 1.0
    strategy_id: str = ""


@dataclass(frozen=True, slots=True)
class ExecutionProposal:
    """Final pipeline output — HOW MUCH to execute."""

    symbol: str
    side: str
    target_weight: float
    weight_delta: float
    notional_delta: float


@dataclass
class PortfolioDecisionContext:
    """Inputs for a single portfolio decision run."""

    portfolio_id: str
    state: PortfolioState
    marks: dict[str, float]
    recommendations: list[TradeRecommendation] = field(default_factory=list)
    config: PortfolioConfig = field(default_factory=PortfolioConfig)
    returns: Any | None = None
    sector_map: dict[str, str] | None = None


@dataclass
class DecisionStageResult:
    stage: str
    status: str
    output: dict[str, Any] = field(default_factory=dict)
    completed_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass
class DecisionRunResult:
    """Aggregated portfolio decision pipeline output."""

    portfolio_id: str
    stages: list[DecisionStageResult] = field(default_factory=list)
    proposals: list[ExecutionProposal] = field(default_factory=list)
    artifacts: dict[str, Any] = field(default_factory=dict)

    @property
    def success(self) -> bool:
        return all(s.status == "ok" for s in self.stages)


def list_decision_stages() -> tuple[str, ...]:
    return DECISION_STAGES


def _default_trade_recommendations(
    ctx: PortfolioDecisionContext,
    prior: dict[str, Any],
) -> dict[str, Any]:
    return {
        "recommendations": [
            {"symbol": r.symbol, "side": r.side, "conviction": r.conviction}
            for r in ctx.recommendations
        ],
        "count": len(ctx.recommendations),
    }


def _default_constraint_evaluation(
    ctx: PortfolioDecisionContext,
    prior: dict[str, Any],
) -> dict[str, Any]:
    engine = PortfolioEngine()
    risk = PortfolioRiskService()
    evaluation = engine.evaluate(ctx.state, ctx.marks, sector_map=ctx.sector_map)
    limits = PortfolioLimits()
    violations: list[str] = []
    for rec in ctx.recommendations:
        if rec.side != "buy":
            continue
        weight = rec.conviction / max(len(ctx.recommendations), 1)
        sector = (ctx.sector_map or {}).get(rec.symbol)
        if not risk.passes_exposure_limits(
            evaluation,
            limits=limits,
            candidate_symbol=rec.symbol,
            candidate_weight=weight,
            candidate_sector=sector,
        ):
            violations.append(rec.symbol)
    return {"passed": len(violations) == 0, "violations": violations}


def _default_risk_budget_allocation(
    ctx: PortfolioDecisionContext,
    prior: dict[str, Any],
) -> dict[str, Any]:
    if not prior.get("passed", True):
        return {"allocated": False, "reason": "constraint_violation"}
    engine = PortfolioEngine()
    evaluation = engine.evaluate(ctx.state, ctx.marks, sector_map=ctx.sector_map)
    ok = passes_risk_budget(evaluation, budget=ctx.config.risk_budget)
    return {"allocated": ok, "within_budget": ok}


def _default_portfolio_construction(
    ctx: PortfolioDecisionContext,
    prior: dict[str, Any],
) -> dict[str, Any]:
    if not prior.get("allocated", True):
        return {"weights": {}, "reason": "risk_budget_blocked"}
    symbols = sorted({r.symbol for r in ctx.recommendations if r.side == "buy"})
    if not symbols:
        symbols = list(ctx.state.positions.keys())
    weights = compute_allocation_weights(ctx.config.allocation_model, symbols)
    return {"weights": weights, "model": ctx.config.allocation_model}


def _default_optimization(
    ctx: PortfolioDecisionContext,
    prior: dict[str, Any],
) -> dict[str, Any]:
    weights = dict(prior.get("weights") or {})
    if ctx.returns is not None and not getattr(ctx.returns, "empty", True):
        optimized = minimum_variance_weights(ctx.returns, list(weights))
        if optimized:
            weights = optimized
    return {"weights": weights, "optimizer": "minimum_variance"}


def _default_rebalancing_decision(
    ctx: PortfolioDecisionContext,
    prior: dict[str, Any],
) -> dict[str, Any]:
    target = dict(prior.get("weights") or {})
    risk = PortfolioRiskService()
    orders = risk.suggest_rebalance(ctx.state, ctx.marks, target)
    return {
        "orders": [
            {
                "symbol": o.symbol,
                "side": o.side,
                "weight_delta": o.weight_delta,
                "notional_delta": o.notional_delta,
            }
            for o in orders
        ],
        "target_weights": target,
    }


def _default_execution_proposal(
    ctx: PortfolioDecisionContext,
    prior: dict[str, Any],
) -> dict[str, Any]:
    target = dict(prior.get("target_weights") or {})
    proposals: list[ExecutionProposal] = []
    for order in prior.get("orders") or []:
        proposals.append(
            ExecutionProposal(
                symbol=order["symbol"],
                side=order["side"],
                target_weight=target.get(order["symbol"], 0.0),
                weight_delta=order["weight_delta"],
                notional_delta=order["notional_delta"],
            )
        )
    return {"proposals": proposals}


_DEFAULT_HANDLERS: dict[str, StageHandler] = {
    "trade_recommendations": _default_trade_recommendations,
    "constraint_evaluation": _default_constraint_evaluation,
    "risk_budget_allocation": _default_risk_budget_allocation,
    "portfolio_construction": _default_portfolio_construction,
    "optimization": _default_optimization,
    "rebalancing_decision": _default_rebalancing_decision,
    "execution_proposal": _default_execution_proposal,
}


class PortfolioDecisionPipeline:
    """Staged portfolio allocation pipeline — APS-PORT-CORE-001."""

    def __init__(self, handlers: dict[str, StageHandler] | None = None) -> None:
        self._handlers = {**_DEFAULT_HANDLERS, **(handlers or {})}

    def run(
        self,
        ctx: PortfolioDecisionContext,
        *,
        stages: list[str] | None = None,
    ) -> DecisionRunResult:
        stage_ids = stages or list(DECISION_STAGES)
        result = DecisionRunResult(portfolio_id=ctx.portfolio_id)
        prior: dict[str, Any] = {}
        for stage_id in stage_ids:
            if stage_id not in DECISION_STAGES:
                result.stages.append(
                    DecisionStageResult(stage=stage_id, status="skipped", output={"reason": "unknown"})
                )
                continue
            handler = self._handlers.get(stage_id)
            if handler is None:
                result.stages.append(
                    DecisionStageResult(stage=stage_id, status="ok", output={"note": "pass-through"})
                )
                prior[stage_id] = {"status": "ok"}
                continue
            try:
                output = handler(ctx, prior)
                result.stages.append(DecisionStageResult(stage=stage_id, status="ok", output=output))
                prior[stage_id] = output
                if stage_id == "execution_proposal":
                    result.proposals = list(output.get("proposals") or [])
            except Exception as exc:  # noqa: BLE001 — pipeline captures stage failures
                result.stages.append(
                    DecisionStageResult(stage=stage_id, status="error", output={"error": str(exc)})
                )
                break
        result.artifacts = prior
        return result
