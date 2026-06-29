"""Slippage models — ATH-REL-007 §5.8, FR-004."""

from __future__ import annotations

from enum import StrEnum

from athena_core.application.backtest_config import BacktestCostsConfig
from athena_core.application.costs import apply_slippage


class SlippageModel(StrEnum):
    """Supported slippage models."""

    FIXED = "fixed"
    PERCENTAGE = "percentage"
    ATR_BASED = "atr_based"
    VOLUME_BASED = "volume_based"


def apply_slippage_model(
    price: float,
    costs: BacktestCostsConfig,
    *,
    model: str | SlippageModel,
    is_buy: bool,
    atr: float | None = None,
    avg_volume: float | None = None,
    volume: float | None = None,
) -> float:
    """Apply slippage according to configured model — FR-004."""
    slippage_model = SlippageModel(model) if isinstance(model, str) else model

    if slippage_model == SlippageModel.PERCENTAGE:
        return apply_slippage(price, costs, is_buy=is_buy)

    if slippage_model == SlippageModel.FIXED:
        tick = float(costs.slippage_pct) * price if costs.slippage_pct else 0.0
        return price + tick if is_buy else price - tick

    if slippage_model == SlippageModel.ATR_BASED:
        if atr is None or atr <= 0:
            return apply_slippage(price, costs, is_buy=is_buy)
        slip = atr * costs.slippage_pct
        return price + slip if is_buy else price - slip

    if slippage_model == SlippageModel.VOLUME_BASED:
        if volume is None or avg_volume is None or avg_volume <= 0:
            return apply_slippage(price, costs, is_buy=is_buy)
        participation = min(volume / avg_volume, 2.0)
        slip_pct = costs.slippage_pct * participation
        return price * (1.0 + slip_pct) if is_buy else price * (1.0 - slip_pct)

    msg = f"unsupported slippage model: {slippage_model}"
    raise ValueError(msg)
