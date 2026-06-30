"""Dependency wiring — inject athena-os and bounded-context engines."""

from __future__ import annotations

from dataclasses import dataclass, field

from athena_core.application.container import ServiceContainer
from athena_core.domain.plugins import PluginRegistry
from athena_domain import IExecutionEngine, IIndicatorEngine, IPatternEngine, IPortfolioEngine, IRiskEngine, IStrategyEngine
from athena_execution import ExecutionEngineFacade
from athena_indicators import IndicatorEngineFacade
from athena_os.runtime import AthenaRuntime
from athena_patterns import PatternEngineFacade
from athena_platform.features import PlatformFeatures
from athena_portfolio import PortfolioEngineFacade
from athena_risk import RiskEngineFacade
from athena_strategies import StrategyEngineFacade


@dataclass
class WiredEngines:
    """Bounded-context engine facades."""

    indicators: IIndicatorEngine | None = None
    patterns: IPatternEngine | None = None
    strategies: IStrategyEngine | None = None
    risk: IRiskEngine | None = None
    portfolio: IPortfolioEngine | None = None
    execution: IExecutionEngine | None = None


@dataclass
class PlatformWiring:
    """Fully wired platform services."""

    runtime: AthenaRuntime
    container: ServiceContainer
    plugin_registry: PluginRegistry
    engines: WiredEngines = field(default_factory=WiredEngines)


def wire_platform(
    runtime: AthenaRuntime,
    *,
    features: PlatformFeatures | None = None,
) -> PlatformWiring:
    """Wire infrastructure and domain engines into a service container."""
    features = features or PlatformFeatures()
    container = ServiceContainer()
    core_registry = PluginRegistry()
    runtime.service_registry.register("plugin_registry", core_registry)

    engines = WiredEngines()
    if features.indicators:
        engines.indicators = IndicatorEngineFacade(core_registry)
        container.register("indicator_engine", lambda: engines.indicators)
    if features.patterns:
        engines.patterns = PatternEngineFacade()
        container.register("pattern_engine", lambda: engines.patterns)
    if features.strategies:
        engines.strategies = StrategyEngineFacade()
        container.register("strategy_engine", lambda: engines.strategies)
    if features.risk:
        engines.risk = RiskEngineFacade()
        container.register("risk_engine", lambda: engines.risk)
    if features.portfolio:
        engines.portfolio = PortfolioEngineFacade()
        container.register("portfolio_engine", lambda: engines.portfolio)
    if features.execution:
        engines.execution = ExecutionEngineFacade()
        container.register("execution_engine", lambda: engines.execution)

    container.register("athena_runtime", lambda: runtime)
    return PlatformWiring(
        runtime=runtime,
        container=container,
        plugin_registry=core_registry,
        engines=engines,
    )
