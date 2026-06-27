# REQ-STRAT-CONFIG-001

**Requirement ID:** REQ-STRAT-CONFIG-001

**Title:** YAML Strategy Configuration Schema

**Purpose:** Define a configuration-driven strategy format so entry rules, exit rules, filters, position sizing, and risk limits are declared in YAML — never hardcoded in Python.

**Description:** Strategies are loaded from YAML files validated against a Pydantic schema. The schema supports named strategies with version, universe, indicators referenced by ID, rule expressions (or structured rule blocks), position sizing, and risk parameters. The strategy loader produces a domain object consumed by the backtest engine; no executable Python strategy code in MVP.

**Inputs:**
- Path to strategy YAML file
- Optional environment overrides

**Outputs:**
- Validated `StrategyConfig` domain object
- Parse/validation errors with line-level context

**Configuration:** (example strategy YAML)
```yaml
strategy:
  id: ema_crossover_v1
  version: "1.0.0"
  description: Golden cross EMA 50/200 on NIFTY 500

universe:
  source: nifty500
  symbols: []  # empty = full universe

indicators:
  - id: ema_fast
    type: ema
    params: { period: 50 }
  - id: ema_slow
    type: ema
    params: { period: 200 }

entry:
  rules:
    - condition: "ema_fast > ema_slow and ema_fast.shift(1) <= ema_slow.shift(1)"
      side: long

exit:
  rules:
    - condition: "ema_fast < ema_slow"
      reason: signal_reversal

filters:
  - type: min_volume
    params: { min_avg_volume_20d: 100000 }

position_sizing:
  method: fixed_fraction
  params: { fraction: 0.05, max_positions: 10 }

risk:
  stop_loss_pct: 0.05
  take_profit_pct: 0.15
  max_holding_days: 60
```

**Algorithm:**
1. Load YAML with safe loader.
2. Validate against Pydantic `StrategyConfig` model (nested models for entry, exit, indicators, risk).
3. Resolve indicator references to registered indicator types (plugin registry).
4. Return immutable config object; no evaluation at load time.

**Dependencies:**
- pydantic, pyyaml
- Indicator registry (REQ-IND-EMA-001, REQ-IND-SMA-001)
- ATH-002: no hardcoded strategy logic in core

**Acceptance Criteria:**
- [ ] Valid example YAML parses without error
- [ ] Invalid YAML (missing required fields, bad types) raises validation error with field path
- [ ] Strategy `id` and `version` are required
- [ ] No Python `eval` of arbitrary code — conditions use safe expression subset or structured DSL (MVP: documented expression string evaluated in sandboxed context in Phase 1)
- [ ] Config round-trips: load → serialize → load produces equivalent object

**Performance Target:**
- Parse typical strategy file: < 10 ms

**Unit Tests:**
- Valid minimal strategy loads
- Missing `entry` or `strategy.id` fails validation
- Indicator reference validation
- Position sizing params bounds

**Integration Tests:**
- Load example strategy from `athena-examples/` (when available)

**Future Enhancements:**
- Visual strategy builder export
- JSON Schema export for IDE autocomplete
- Strategy composition / inheritance
- Regime-conditional rule blocks
