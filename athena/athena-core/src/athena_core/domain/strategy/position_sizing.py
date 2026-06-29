"""Position sizing calculators — ATH-REL-006 §5.7, FR-008."""

from __future__ import annotations

from typing import Any


def compute_position_quantity(
    method: str,
    params: dict[str, Any],
    *,
    price: float,
    cash: float,
    open_positions: int = 0,
    atr: float | None = None,
) -> int:
    """Compute share quantity for a new position — ATH-REL-006 §5.7."""
    if price <= 0:
        return 0

    if method == "fixed_fraction":
        fraction = float(params.get("fraction", 0.05))
        max_positions = int(params.get("max_positions", 10))
        allocation = cash * fraction
        slots = max(max_positions - open_positions, 1)
        budget = min(allocation, cash / slots)
        return int(budget / price)

    if method == "fixed_amount":
        amount = float(params.get("amount", 0))
        return int(amount / price)

    if method == "fixed_quantity":
        return int(params.get("quantity", 0))

    if method == "pct_risk":
        risk_pct = float(params.get("risk_pct", 0.01))
        stop_pct = float(params.get("stop_pct", 0.05))
        if stop_pct <= 0:
            return 0
        risk_capital = cash * risk_pct
        per_share_risk = price * stop_pct
        return int(risk_capital / per_share_risk)

    if method == "atr_based":
        if atr is None or atr <= 0:
            return 0
        risk_pct = float(params.get("risk_pct", 0.01))
        atr_multiplier = float(params.get("atr_multiplier", 2.0))
        risk_capital = cash * risk_pct
        per_share_risk = atr * atr_multiplier
        return int(risk_capital / per_share_risk)

    return 0
