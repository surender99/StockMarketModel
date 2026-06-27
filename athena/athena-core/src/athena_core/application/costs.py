"""Transaction cost calculations — REQ-BT-ENGINE-001."""

from __future__ import annotations

from athena_core.application.backtest_config import BacktestCostsConfig


def compute_trade_costs(
    notional: float,
    costs: BacktestCostsConfig,
    *,
    is_sell: bool,
) -> float:
    """Return total fees for a trade leg (brokerage + STT on sell; slippage is on fill price)."""
    brokerage = max(notional * costs.brokerage_pct, costs.brokerage_flat)
    brokerage *= 1.0 + costs.gst_on_brokerage_pct
    stt = notional * costs.stt_pct if is_sell else 0.0
    return brokerage + stt


def apply_slippage(price: float, costs: BacktestCostsConfig, *, is_buy: bool) -> float:
    """Adjust fill price for slippage (buy pays more, sell receives less)."""
    if is_buy:
        return price * (1.0 + costs.slippage_pct)
    return price * (1.0 - costs.slippage_pct)
