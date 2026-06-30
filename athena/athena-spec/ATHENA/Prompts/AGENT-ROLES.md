# AI Agent Roles

> **Purpose:** Standard agent workflow for Athena development with AI coding assistants.

## Role Pipeline

```
Planner → Architect → Developer → Reviewer → QA → Documentation → Release
```

| Role | Responsibility | Outputs |
|------|----------------|---------|
| **Planner** | Break REL/APS scope into tasks; prioritize | Task list, acceptance criteria |
| **Architect** | Validate design against ADRs, dependency rules | Design notes, ADR drafts |
| **Developer** | Implement code against APS specs | PR, unit tests |
| **Reviewer** | Code review, security, quant correctness | Review comments, approval |
| **QA** | Run pytest, golden datasets, benchmarks | Test report |
| **Documentation** | Update APS traceability, README, catalogs | Spec updates |
| **Release** | Version bump, changelog, production checklist | Release tag, sign-off |

## Domain Expert Agents

Specialized agents for bounded-context development (pair with APS domain specs):

| Agent | Domain | Key Packages | Focus |
|-------|--------|--------------|-------|
| **Indicator Expert** | Technical indicators | `athena-indicators`, `athena-core.domain.indicators` | EMA, RSI, volume indicators, validation |
| **Pattern Expert** | Chart & candlestick patterns | `athena-patterns`, `athena-core.domain.patterns` | MSP pipeline, scoring, catalog |
| **Strategy Expert** | Strategy engine | `athena-strategies`, `athena-core.domain.strategy` | Signals, composition, sizing |
| **Portfolio Expert** | Portfolio management | `athena-portfolio`, `athena-core.domain.portfolio` | Positions, rebalancing, snapshots |
| **OMS Expert** | Order management & execution | `athena-execution`, simulation/OMS APS | Backtest, paper trading, order lifecycle |
| **Statistics Expert** | Quant analytics | `athena-math`, `athena-core.domain.statistics` | Correlation, regression, distributions |
| **ML Expert** | Machine learning | `athena-ai`, `athena-core.domain.ml` | Training, drift, model registry |
| **Database Expert** | Data platform | `athena-data`, ATH-005 catalog | OHLCV ingest, quality, versioning |

Each expert agent must validate changes against `athena-domain` contracts and update event YAML when emitting new domain events.

## Handoff Rules

1. Planner references APS ID and TRACEABILITY-INDEX row before coding.
2. Architect confirms no dependency rule violations (`check_dependencies.py`).
3. Developer links **Implemented In** and **Tests** in APS markdown.
4. QA runs `make test` including `athena-os` and `athena-testing`.
5. Documentation updates EVENT-CATALOG and INTERFACE-CATALOG for new public APIs.
6. Release verifies [PRODUCTION-READINESS-CHECKLIST.md](../Reviews/PRODUCTION-READINESS-CHECKLIST.md).

## Prompts

Agent prompts indexed under [Prompts/README.md](README.md).
