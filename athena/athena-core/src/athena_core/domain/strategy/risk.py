"""Strategy risk limits — ATH-REL-006 §5.6, FR-007."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RiskLimits:
    """Portfolio-level risk constraints — ATH-REL-006 §5.6."""

    max_loss_pct: float | None = None
    max_daily_loss_pct: float | None = None
    max_drawdown_pct: float | None = None
    max_exposure_pct: float | None = None
    risk_per_trade_pct: float | None = None


@dataclass(frozen=True)
class RiskContext:
    """Current portfolio risk state for limit checks."""

    equity: float
    initial_equity: float
    daily_pnl_pct: float
    drawdown_pct: float
    gross_exposure_pct: float
    trade_risk_pct: float = 0.0


def check_risk_limits(context: RiskContext, limits: RiskLimits) -> list[str]:
    """Return list of violated risk limit messages (empty if within limits)."""
    violations: list[str] = []

    if limits.max_loss_pct is not None and context.initial_equity > 0:
        loss_pct = 1.0 - context.equity / context.initial_equity
        if loss_pct > limits.max_loss_pct:
            violations.append(f"max_loss_pct exceeded: {loss_pct:.4f}")

    if limits.max_daily_loss_pct is not None:
        if context.daily_pnl_pct < -limits.max_daily_loss_pct:
            violations.append(f"max_daily_loss_pct exceeded: {context.daily_pnl_pct:.4f}")

    if limits.max_drawdown_pct is not None:
        if context.drawdown_pct > limits.max_drawdown_pct:
            violations.append(f"max_drawdown_pct exceeded: {context.drawdown_pct:.4f}")

    if limits.max_exposure_pct is not None:
        if context.gross_exposure_pct > limits.max_exposure_pct:
            violations.append(f"max_exposure_pct exceeded: {context.gross_exposure_pct:.4f}")

    if limits.risk_per_trade_pct is not None:
        if context.trade_risk_pct > limits.risk_per_trade_pct:
            violations.append(f"risk_per_trade_pct exceeded: {context.trade_risk_pct:.4f}")

    return violations


def within_risk_limits(context: RiskContext, limits: RiskLimits) -> bool:
    """Return True when no risk limits are violated."""
    return not check_risk_limits(context, limits)
