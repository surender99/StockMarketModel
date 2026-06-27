# AES-0202 – Plugin Architecture

> **References source:** `References/Athena-Package-02-Architecture/architecture/AES-0202-Plugin-Architecture.md`  
> **Implementation stub:** `athena-core/src/athena_core/domain/plugins/`

Athena extends behavior through registered plugins rather than modifying core engines. Every pluggable component exposes a stable contract.

---

## Plugin Contract

Every plugin must expose:

| Field | Description |
|-------|-------------|
| `id` | Unique identifier (e.g. `ema`, `sma`) |
| `version` | Semantic version string |
| `metadata` | Human-readable name, description, author |
| `configuration_schema` | Validated parameter schema (Pydantic or JSON Schema) |
| `execute()` | Callable that performs the plugin's work |

Plugins are **registered**, not hardcoded. The composition root (`runtime.py`) or a `PluginRegistry` resolves plugins by `id` at runtime.

---

## Plugin Types

| Type | Contract | MVP Implementation |
|------|----------|-------------------|
| **Indicators** | [IndicatorProvider](../contracts/IndicatorProvider.md) | `_INDICATOR_REGISTRY` in `FeatureService` |
| **Patterns** | PatternProvider (Package 06) | ⏳ Not yet |
| **Strategies** | [StrategyProvider](../contracts/StrategyProvider.md) | `StrategyConfig` YAML |
| **Risk** | Risk rules in strategy config | `RiskConfig` in `StrategyConfig` |
| **Reports** | Experiment / backtest reports | Experiment tracker |
| **ML Models** | ML scorer plugins | `MLScorer` application service |

---

## Registration Model

```
PluginRegistry
  ├── register(plugin: Plugin) → None
  ├── get(plugin_id: str) → Plugin
  └── list(plugin_type: PluginType) → list[Plugin]
```

MVP stub: `athena_core.domain.plugins.PluginRegistry` — minimal registry for future indicator/pattern/strategy plugins. Current indicators remain in `FeatureService._INDICATOR_REGISTRY` until Package 05 formalizes the indicator framework.

---

## Rules

1. **Plugins are pure where possible** — indicators must be deterministic and vectorized ([IndicatorProvider](../contracts/IndicatorProvider.md)).
2. **Plugins do not execute orders** — strategies emit signals only; the backtester/portfolio layer executes ([StrategyProvider](../contracts/StrategyProvider.md)).
3. **Configuration is external** — plugin parameters come from YAML/JSON config, not code constants.
4. **Versioning is explicit** — breaking parameter changes require a version bump.

---

## Evolution Path

| Phase | Action |
|-------|--------|
| Package 02 (now) | `PluginRegistry` stub, contracts documented |
| Package 05 | Migrate indicators to `IndicatorProvider` plugins |
| Package 06 | Add `PatternProvider` plugins |
| Package 07 | Formalize `StrategyProvider` lifecycle |

---

## Related Documents

| Document | Purpose |
|----------|---------|
| [AES-0200 System Architecture](AES-0200-System-Architecture.md) | Layer model |
| [IndicatorProvider](../contracts/IndicatorProvider.md) | Indicator plugin contract |
| [StrategyProvider](../contracts/StrategyProvider.md) | Strategy plugin contract |
| [ATH-000 Philosophy](../ATH-000-Philosophy.md) | Principle 5: Plugin-first |
