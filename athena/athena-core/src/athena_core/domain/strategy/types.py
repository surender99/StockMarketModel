"""Strategy signal types — ATH-REL-006 §03, FR-009."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class SignalDirection(StrEnum):
    """Trade signal direction — ATH-REL-006 §5.3."""

    BUY = "buy"
    SELL = "sell"
    NEUTRAL = "neutral"


@dataclass(frozen=True)
class TradeSignal:
    """Evaluated strategy signal with confidence — ATH-REL-006 §5.3."""

    direction: SignalDirection
    confidence: float
    reason: str
    side: str | None = None

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            msg = f"confidence must be in [0, 1], got {self.confidence}"
            raise ValueError(msg)
