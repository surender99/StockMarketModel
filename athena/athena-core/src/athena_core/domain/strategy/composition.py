"""Strategy signal composition — ATH-REL-006 §5.9, FR-012."""

from __future__ import annotations

from enum import StrEnum

from athena_core.domain.strategy.types import SignalDirection, TradeSignal


class CompositionMode(StrEnum):
    """Signal composition operators — ATH-REL-006 §5.9."""

    AND = "and"
    OR = "or"
    NOT = "not"
    WEIGHTED = "weighted"
    VOTING = "voting"


def compose_signals(
    signals: list[TradeSignal],
    mode: CompositionMode,
    *,
    weights: list[float] | None = None,
    threshold: float = 0.5,
) -> TradeSignal | None:
    """Combine multiple signals into one composite signal."""
    if not signals:
        return None

    if mode == CompositionMode.NOT:
        if len(signals) != 1:
            msg = "NOT composition requires exactly one signal"
            raise ValueError(msg)
        base = signals[0]
        direction = (
            SignalDirection.NEUTRAL
            if base.direction != SignalDirection.NEUTRAL
            else SignalDirection.BUY
        )
        return TradeSignal(
            direction=direction,
            confidence=base.confidence,
            reason=f"not:{base.reason}",
            side=base.side,
        )

    if mode == CompositionMode.AND:
        if any(s.direction == SignalDirection.NEUTRAL for s in signals):
            return None
        buy_count = sum(1 for s in signals if s.direction == SignalDirection.BUY)
        sell_count = sum(1 for s in signals if s.direction == SignalDirection.SELL)
        if buy_count == len(signals):
            direction = SignalDirection.BUY
        elif sell_count == len(signals):
            direction = SignalDirection.SELL
        else:
            return None
        confidence = min(s.confidence for s in signals)
        return TradeSignal(
            direction=direction,
            confidence=confidence,
            reason="and:" + "+".join(s.reason for s in signals),
            side=signals[0].side,
        )

    if mode == CompositionMode.OR:
        non_neutral = [s for s in signals if s.direction != SignalDirection.NEUTRAL]
        if not non_neutral:
            return TradeSignal(
                direction=SignalDirection.NEUTRAL,
                confidence=0.0,
                reason="or:none",
            )
        best = max(non_neutral, key=lambda s: s.confidence)
        return TradeSignal(
            direction=best.direction,
            confidence=best.confidence,
            reason=f"or:{best.reason}",
            side=best.side,
        )

    if mode == CompositionMode.WEIGHTED:
        w = weights or [1.0] * len(signals)
        if len(w) != len(signals):
            msg = "weights length must match signals length"
            raise ValueError(msg)
        score = sum(s.confidence * weight for s, weight in zip(signals, w, strict=True))
        total_w = sum(w)
        confidence = score / total_w if total_w else 0.0
        if confidence < threshold:
            return TradeSignal(
                direction=SignalDirection.NEUTRAL,
                confidence=confidence,
                reason="weighted:below_threshold",
            )
        buys = sum(w for s, w in zip(signals, w, strict=True) if s.direction == SignalDirection.BUY)
        sells = sum(w for s, w in zip(signals, w, strict=True) if s.direction == SignalDirection.SELL)
        direction = SignalDirection.BUY if buys >= sells else SignalDirection.SELL
        return TradeSignal(
            direction=direction,
            confidence=confidence,
            reason="weighted:composite",
            side=signals[0].side,
        )

    if mode == CompositionMode.VOTING:
        votes: dict[SignalDirection, int] = {}
        for signal in signals:
            votes[signal.direction] = votes.get(signal.direction, 0) + 1
        winner = max(votes, key=lambda d: votes[d])
        if votes[winner] < len(signals) * threshold:
            return TradeSignal(
                direction=SignalDirection.NEUTRAL,
                confidence=votes[winner] / len(signals),
                reason="voting:below_threshold",
            )
        confidence = votes[winner] / len(signals)
        return TradeSignal(
            direction=winner,
            confidence=confidence,
            reason="voting:composite",
            side=signals[0].side,
        )

    msg = f"unsupported composition mode: {mode}"
    raise ValueError(msg)
