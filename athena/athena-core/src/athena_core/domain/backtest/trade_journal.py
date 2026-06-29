"""Trade journal — ATH-REL-007 §5.12, FR-010."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from athena_core.domain.backtest.models import TradeRecord


@dataclass(frozen=True)
class TradeJournalEntry:
    """Structured trade journal row — FR-010."""

    symbol: str
    strategy_id: str
    side: str
    entry_date: date
    exit_date: date
    entry_price: float
    exit_price: float
    quantity: int
    gross_pnl: float
    net_pnl: float
    commission: float
    slippage_estimate: float
    exit_reason: str
    duration_days: int
    signal_reason: str = ""


def build_trade_journal(
    trades: list[TradeRecord],
    *,
    strategy_id: str,
    slippage_pct: float = 0.0,
) -> list[TradeJournalEntry]:
    """Build trade journal from completed trades — FR-010."""
    journal: list[TradeJournalEntry] = []
    for trade in trades:
        commission = trade.entry_fees + trade.exit_fees
        mid_entry = trade.entry_price
        mid_exit = trade.exit_price
        slip_est = abs(mid_entry * slippage_pct) + abs(mid_exit * slippage_pct)
        journal.append(
            TradeJournalEntry(
                symbol=trade.symbol,
                strategy_id=strategy_id,
                side=trade.side,
                entry_date=trade.entry_date,
                exit_date=trade.exit_date,
                entry_price=trade.entry_price,
                exit_price=trade.exit_price,
                quantity=trade.quantity,
                gross_pnl=trade.gross_pnl,
                net_pnl=trade.net_pnl,
                commission=commission,
                slippage_estimate=slip_est,
                exit_reason=trade.exit_reason,
                duration_days=(trade.exit_date - trade.entry_date).days,
                signal_reason=trade.exit_reason,
            )
        )
    return journal
