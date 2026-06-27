# StrategyProvider Contract

> **References source:** `References/Athena-Package-02-Architecture/contracts/StrategyProvider.md`  
> **Architecture:** [AES-0202 Plugin Architecture](../architecture/AES-0202-Plugin-Architecture.md)  
> **Implementation:** `athena-core/src/athena_core/domain/strategy/`

Contract for strategy plugins — declarative rules that emit trade signals without executing orders.

---

## Interface

### Inputs (Configuration)

| Block | Description |
|-------|-------------|
| **Entry Rules** | Conditions that open positions (`entry.rules`) |
| **Exit Rules** | Conditions that close positions (`exit.rules`) |
| **Risk Rules** | Stop loss, take profit, max holding (`risk`) |
| **Position Rules** | Sizing method and limits (`position_sizing`) |
| **Filters** | Pre-entry gates (e.g. regime filter) |
| **Indicators** | Referenced features (`indicators`) |
| **Universe** | Symbols to evaluate |

### Output

| Output | Type | Description |
|--------|------|-------------|
| Trade Signals | Boolean conditions per bar | Evaluated by `BacktestEngine` / `Scanner` |

**Strategies must not execute orders directly.** Signal evaluation is separate from portfolio execution and cost modeling.

---

## Requirements

| # | Rule | Rationale |
|---|------|-----------|
| 1 | **Signals only** | Strategy layer evaluates conditions; backtester applies fills |
| 2 | **Declarative config** | Rules expressed in YAML, not imperative code |
| 3 | **No lookahead** | Conditions use features available at bar close |
| 4 | **Validated schema** | `StrategyConfig` Pydantic model rejects invalid configs at load time |

---

## Live Implementation Mapping

| Contract element | `athena-core` location |
|------------------|------------------------|
| Strategy identity | `StrategyMeta` (`id`, `version`, `description`) |
| Entry rules | `EntryConfig` → `RuleSpec` (`condition`, `side`) |
| Exit rules | `ExitConfig` → `ExitRuleSpec` (`condition`, `reason`) |
| Risk rules | `RiskConfig` (`stop_loss_pct`, `take_profit_pct`, `max_holding_days`) |
| Position rules | `PositionSizingConfig` (`fixed_fraction`, `fixed_amount`) |
| Condition evaluation | `domain/strategy/expression.py` |
| YAML loading | `infrastructure/strategy_yaml_loader.py` |
| Signal → execution | `application/backtest_engine.py`, `application/scanner.py` |

### Example YAML

```yaml
strategy:
  id: ema_crossover
  version: "1.0.0"
  description: Fast/slow EMA crossover

universe:
  symbols: [RELIANCE.NS]

indicators:
  - id: fast_ema
    type: ema
    params: { period: 12 }
  - id: slow_ema
    type: ema
    params: { period: 26 }

entry:
  rules:
    - condition: "fast_ema > slow_ema"
      side: long

exit:
  rules:
    - condition: "fast_ema < slow_ema"
      reason: signal

position_sizing:
  method: fixed_fraction
  params: { fraction: 0.05, max_positions: 5 }

risk:
  stop_loss_pct: 0.05
  max_holding_days: 20
```

---

## Separation of Concerns

```
StrategyConfig  →  expression evaluator  →  entry/exit booleans
                                              ↓
BacktestEngine  →  position sizing, costs, fills  →  TradeRecord[]
```

The strategy provider answers *whether* to enter or exit. The backtester answers *how much* and *at what price*.

---

## Future (Package 07)

Package 07 will formalize strategy lifecycle (draft → validate → backtest → promote) and may introduce imperative `StrategyProvider` plugins alongside declarative YAML.

---

## Related Documents

| Document | Purpose |
|----------|---------|
| [REQ-STRAT-CONFIG-001](../requirements/REQ-STRAT-CONFIG-001.md) | Strategy YAML requirement |
| [REQ-BT-ENGINE-001](../requirements/REQ-BT-ENGINE-001.md) | Backtest engine |
| [IndicatorProvider](IndicatorProvider.md) | Indicator contract |
