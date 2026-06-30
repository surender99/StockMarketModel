# Capability Map

> Organize Athena by **business capability**, not technology layer.

## Indicators

| Capability | APS Domain | Package | Status |
|------------|------------|---------|--------|
| EMA | Indicators/Trend | `athena-indicators` | Facade |
| RSI | Indicators/Momentum | `athena-indicators` | Facade |
| Volume (OBV, CMF) | Indicators/Volume | `athena-indicators` | Facade |

## Patterns

| Capability | APS Domain | Package | Status |
|------------|------------|---------|--------|
| Double Top | Chart-Patterns | `athena-patterns` | Facade |
| Candlestick Engulfing | Candlestick-Engine | `athena-patterns` | Facade |
| Wyckoff Spring | Wyckoff-Engine | `athena-patterns` | Facade |

## Strategies

| Capability | APS Domain | Package | Status |
|------------|------------|---------|--------|
| Momentum | Strategies | `athena-strategies` | Facade |
| Mean Reversion | Strategies | `athena-strategies` | Facade |
| Multi-factor | Strategies | `athena-strategies` | Facade |

## Portfolio & Risk

| Capability | Package | Status |
|------------|---------|--------|
| Position tracking | `athena-portfolio` | Facade |
| Rebalancing | `athena-portfolio` | Facade |
| Drawdown / VaR | `athena-risk` | Facade |

## Execution

| Capability | Package | Status |
|------------|---------|--------|
| Backtest | `athena-execution` | Facade |
| Paper trading | `athena-core.domain.paper` | In core |
| Live OMS | Future ETOP | Spec |

## Platform

| Capability | Package | Status |
|------------|---------|--------|
| Runtime assembly | `athena-platform` | Implemented |
| Infrastructure | `athena-os` | Implemented |
| Shared types | `athena-common` | Implemented |

## Navigation

- APS specs: [APS/README.md](../APS/README.md)
- Dependency rules: [DEPENDENCY-RULES.md](../DEPENDENCY-RULES.md)
- Build graph: [Dependency-Graph/BUILD-GRAPH.md](../Dependency-Graph/BUILD-GRAPH.md)
