"""Portfolio optimization — ATH-REL-008 §5.10."""

from __future__ import annotations

import numpy as np
import pandas as pd

from athena_core.domain.portfolio.allocation import normalize_weights


def inverse_volatility_weights(
    returns: pd.DataFrame,
    symbols: list[str] | None = None,
) -> dict[str, float]:
    """Risk-parity approximation via inverse volatility — FR-005."""
    cols = symbols or list(returns.columns)
    cols = [c for c in cols if c in returns.columns]
    if not cols:
        return {}
    vols = returns[cols].std()
    raw = {s: 1.0 / max(float(vols[s]), 1e-8) for s in cols}
    return normalize_weights(raw)


def minimum_variance_weights(
    returns: pd.DataFrame,
    symbols: list[str] | None = None,
) -> dict[str, float]:
    """Minimum-variance portfolio weights — FR-005."""
    cols = symbols or list(returns.columns)
    cols = [c for c in cols if c in returns.columns]
    if not cols:
        return {}
    if len(cols) == 1:
        return {cols[0]: 1.0}

    cov = returns[cols].cov().to_numpy(dtype=float)
    ones = np.ones(len(cols))
    try:
        inv = np.linalg.inv(cov)
    except np.linalg.LinAlgError:
        return inverse_volatility_weights(returns, cols)

    w = inv @ ones
    w = w / w.sum()
    w = np.clip(w, 0.0, None)
    if w.sum() <= 0:
        return inverse_volatility_weights(returns, cols)
    w = w / w.sum()
    return {sym: float(weight) for sym, weight in zip(cols, w)}
