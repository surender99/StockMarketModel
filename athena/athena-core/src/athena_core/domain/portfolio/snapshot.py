"""Immutable portfolio snapshots — ATH-REL-008 §5.1, REQ-PF-SNAPSHOT-001."""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime, timezone

from athena_core.domain.portfolio.models import PortfolioEvaluation, PortfolioState
from athena_core.domain.portfolio.positions import OpenPosition


def _copy_state(state: PortfolioState) -> PortfolioState:
    positions = {
        sym: OpenPosition(
            symbol=pos.symbol,
            side=pos.side,
            entry_date=pos.entry_date,
            entry_price=pos.entry_price,
            quantity=pos.quantity,
            entry_fees=pos.entry_fees,
            stop_price=pos.stop_price,
        )
        for sym, pos in state.positions.items()
    }
    return PortfolioState(cash=state.cash, positions=positions)


@dataclass(frozen=True)
class PortfolioSnapshot:
    """Immutable point-in-time portfolio record — FR-014."""

    snapshot_id: str
    portfolio_id: str
    version: int
    captured_at: datetime
    state: PortfolioState
    evaluation: PortfolioEvaluation | None = None

    @classmethod
    def capture(
        cls,
        portfolio_id: str,
        state: PortfolioState,
        *,
        version: int = 1,
        evaluation: PortfolioEvaluation | None = None,
    ) -> PortfolioSnapshot:
        return cls(
            snapshot_id=str(uuid.uuid4()),
            portfolio_id=portfolio_id,
            version=version,
            captured_at=datetime.now(timezone.utc),
            state=_copy_state(state),
            evaluation=evaluation,
        )
