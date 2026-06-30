"""Probability utilities — stub."""

from __future__ import annotations

import math


def normal_cdf_stub(z: float) -> float:
    """Approximate standard normal CDF — stub implementation."""
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))
