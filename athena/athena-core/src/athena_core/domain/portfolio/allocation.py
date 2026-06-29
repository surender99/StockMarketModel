"""Capital allocation models — ATH-REL-008 §5.2, REQ-PF-ALLOCATION-001."""

from __future__ import annotations

from typing import Literal

AllocationModelId = Literal[
    "equal_weight",
    "market_cap",
    "risk_weight",
    "volatility_weight",
    "custom",
]

ALLOCATION_MODELS: dict[str, str] = {
    "equal_weight": "Equal weight across symbols",
    "market_cap": "Market-cap weighted allocation",
    "risk_weight": "Inverse-volatility (risk parity) weights",
    "volatility_weight": "Volatility-proportional weights",
    "custom": "User-supplied custom weights",
}


def normalize_weights(weights: dict[str, float]) -> dict[str, float]:
    """Normalize weights to sum to 1.0."""
    total = sum(abs(w) for w in weights.values())
    if total <= 0:
        n = len(weights)
        return {s: 1.0 / n for s in weights} if n else {}
    return {s: w / total for s, w in weights.items()}


def compute_allocation_weights(
    model: AllocationModelId,
    symbols: list[str],
    *,
    market_caps: dict[str, float] | None = None,
    volatilities: dict[str, float] | None = None,
    custom_weights: dict[str, float] | None = None,
) -> dict[str, float]:
    """Compute target allocation weights — REQ-PF-ALLOCATION-001."""
    if not symbols:
        return {}

    if model == "custom":
        weights = {s: custom_weights.get(s, 0.0) if custom_weights else 0.0 for s in symbols}
        return normalize_weights(weights)

    if model == "equal_weight":
        w = 1.0 / len(symbols)
        return {s: w for s in symbols}

    if model == "market_cap":
        caps = market_caps or {}
        raw = {s: max(caps.get(s, 0.0), 0.0) for s in symbols}
        if sum(raw.values()) <= 0:
            return compute_allocation_weights("equal_weight", symbols)
        return normalize_weights(raw)

    if model in ("risk_weight", "volatility_weight"):
        vols = volatilities or {}
        if model == "risk_weight":
            raw = {s: 1.0 / max(vols.get(s, 0.0), 1e-8) for s in symbols}
        else:
            raw = {s: max(vols.get(s, 0.0), 0.0) for s in symbols}
        if sum(raw.values()) <= 0:
            return compute_allocation_weights("equal_weight", symbols)
        return normalize_weights(raw)

    raise ValueError(f"Unknown allocation model: {model}")
