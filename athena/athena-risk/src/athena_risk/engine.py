"""Risk engine adapter implementing IRiskEngine."""
from __future__ import annotations

import pandas as pd

from athena_core.domain.analytics.risk import RiskReport, analyze_risk


class RiskEngineFacade:
    """Delegates to athena-core risk analytics — extraction path: ADR-0006."""

    def analyze(self, equity_curve: pd.DataFrame, **kwargs: object) -> RiskReport:
        return analyze_risk(equity_curve, **kwargs)  # type: ignore[arg-type]
