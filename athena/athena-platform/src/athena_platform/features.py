"""Feature toggles for platform assembly."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class PlatformFeatures:
    """Runtime feature flags — extend as capabilities are promoted."""

    indicators: bool = True
    patterns: bool = True
    strategies: bool = True
    risk: bool = True
    portfolio: bool = True
    execution: bool = True
    ai: bool = False
    dashboard: bool = False

    def enabled_modules(self) -> list[str]:
        flags = {
            "indicators": self.indicators,
            "patterns": self.patterns,
            "strategies": self.strategies,
            "risk": self.risk,
            "portfolio": self.portfolio,
            "execution": self.execution,
            "ai": self.ai,
            "dashboard": self.dashboard,
        }
        return [name for name, on in flags.items() if on]
