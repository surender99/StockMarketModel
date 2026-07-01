"""Delivery hierarchy implementation package registry — ATH-IP-000001 … 000033."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

ProbeKind = Literal["import", "script"]


@dataclass(frozen=True, slots=True)
class DeliveryIP:
    """Maps a delivery-hierarchy IP spec to its MVP code entry point."""

    ip_id: str
    name: str
    domain: str
    probe_kind: ProbeKind
    target: str
    """Import path ``module:symbol`` or script name under ``athena/scripts/``."""


DELIVERY_IPS: tuple[DeliveryIP, ...] = (
    DeliveryIP("ATH-IP-000001", "Architecture-Validator", "Engineering", "script", "validate_architecture.py"),
    DeliveryIP("ATH-IP-000002", "Dependency-Analyzer", "Engineering", "script", "check_dependencies.py"),
    DeliveryIP("ATH-IP-000003", "Code-Generator", "Engineering", "script", "codegen/run_all.py"),
    DeliveryIP("ATH-IP-000004", "Athena-Inspector", "Engineering", "script", "athena_inspector.py"),
    DeliveryIP("ATH-IP-000005", "Event-Bus", "AthenaOS", "import", "athena_os.event_bus:EventBus"),
    DeliveryIP("ATH-IP-000006", "Event-Registry", "AthenaOS", "import", "athena_common.events_generated:EVENT_REGISTRY"),
    DeliveryIP("ATH-IP-000007", "Plugin-Registry", "AthenaOS", "import", "athena_os.plugins:PluginRegistry"),
    DeliveryIP("ATH-IP-000008", "Workflow-Engine", "AthenaOS", "import", "athena_os.workflow:WorkflowEngine"),
    DeliveryIP(
        "ATH-IP-000009",
        "Instrument-Registry",
        "Data",
        "import",
        "athena_core.infrastructure.instrument_master:YamlInstrumentMaster",
    ),
    DeliveryIP(
        "ATH-IP-000010",
        "Historical-Repository",
        "Data",
        "import",
        "athena_core.infrastructure.parquet_ohlcv_store:ParquetOHLCVStore",
    ),
    DeliveryIP("ATH-IP-000011", "Tick-Repository", "Data", "import", "athena_data.tick_repository:TickRepository"),
    DeliveryIP("ATH-IP-000012", "Bar-Engine", "Data", "import", "athena_data.bar_engine:BarEngine"),
    DeliveryIP("ATH-IP-000013", "EMA", "Indicators", "import", "athena_core.domain.indicators.engine:IndicatorEngine"),
    DeliveryIP("ATH-IP-000014", "SMA", "Indicators", "import", "athena_core.domain.indicators.engine:IndicatorEngine"),
    DeliveryIP("ATH-IP-000015", "RSI", "Indicators", "import", "athena_core.domain.indicators.engine:IndicatorEngine"),
    DeliveryIP("ATH-IP-000016", "MACD", "Indicators", "import", "athena_core.domain.indicators.engine:IndicatorEngine"),
    DeliveryIP("ATH-IP-000017", "ATR", "Indicators", "import", "athena_core.domain.indicators.engine:IndicatorEngine"),
    DeliveryIP(
        "ATH-IP-000018",
        "Market-Structure",
        "Patterns",
        "import",
        "athena_core.domain.patterns.pipeline:PatternPipeline",
    ),
    DeliveryIP(
        "ATH-IP-000019",
        "Candlestick-Engine",
        "Patterns",
        "import",
        "athena_core.domain.patterns.pipeline:PatternPipeline",
    ),
    DeliveryIP(
        "ATH-IP-000020",
        "Chart-Patterns",
        "Patterns",
        "import",
        "athena_core.domain.patterns.pipeline:PatternPipeline",
    ),
    DeliveryIP(
        "ATH-IP-000021",
        "Divergence",
        "Patterns",
        "import",
        "athena_core.domain.patterns.pipeline:PatternPipeline",
    ),
    DeliveryIP(
        "ATH-IP-000022",
        "Momentum",
        "Strategies",
        "import",
        "athena_core.domain.strategy.engine:StrategyEngine",
    ),
    DeliveryIP(
        "ATH-IP-000023",
        "Swing",
        "Strategies",
        "import",
        "athena_core.domain.strategy.engine:StrategyEngine",
    ),
    DeliveryIP(
        "ATH-IP-000024",
        "Breakout",
        "Strategies",
        "import",
        "athena_core.domain.strategy.engine:StrategyEngine",
    ),
    DeliveryIP(
        "ATH-IP-000025",
        "Mean-Reversion",
        "Strategies",
        "import",
        "athena_core.domain.strategy.engine:StrategyEngine",
    ),
    DeliveryIP(
        "ATH-IP-000026",
        "Portfolio-Engine",
        "Portfolio",
        "import",
        "athena_core.application.portfolio_manager:PortfolioManager",
    ),
    DeliveryIP(
        "ATH-IP-000027",
        "Risk-Engine",
        "Portfolio",
        "import",
        "athena_risk.engine:RiskEngineFacade",
    ),
    DeliveryIP(
        "ATH-IP-000028",
        "Position-Sizing",
        "Portfolio",
        "import",
        "athena_core.domain.strategy.position_sizing:compute_position_quantity",
    ),
    DeliveryIP(
        "ATH-IP-000029",
        "Exposure",
        "Portfolio",
        "import",
        "athena_core.domain.portfolio.models:ExposureMetrics",
    ),
    DeliveryIP(
        "ATH-IP-000030",
        "Order-Management",
        "OMS",
        "import",
        "athena_core.domain.simulation.oms:SimOrderManager",
    ),
    DeliveryIP(
        "ATH-IP-000031",
        "Paper-Trading",
        "OMS",
        "import",
        "athena_core.application.paper_trading_engine:PaperTradingEngine",
    ),
    DeliveryIP(
        "ATH-IP-000032",
        "Order-Routing",
        "OMS",
        "import",
        "athena_execution.order_routing:OrderRouter",
    ),
    DeliveryIP(
        "ATH-IP-000033",
        "Execution-Monitor",
        "OMS",
        "import",
        "athena_execution.execution_monitor:ExecutionMonitor",
    ),
)
