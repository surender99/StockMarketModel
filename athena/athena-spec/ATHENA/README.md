# ATHENA — Specification Tree

Canonical navigation for Athena planning (Releases), implementation (APS), and supporting artifacts.

```
ATHENA
│
├── Releases/          Planning packages REL-000 … REL-020
├── APS/               Implementation specs by domain
├── ADR/               Architecture decision records (index)
├── Schemas/           JSON/YAML schema index
├── Golden-Datasets/   Small fixtures for tests and validation
├── Benchmarks/          Performance targets and test references
├── Prompts/             AI coding agent prompts (index)
├── Reviews/             CTO and revision review archives
├── events/              Event catalog (publisher/subscriber contracts)
└── interfaces/          Public API interface catalog
```

## APS Traceability

Every APS document must include the traceability block defined in [APS/_TEMPLATE.md](APS/_TEMPLATE.md):

| Field | Description |
|-------|-------------|
| APS ID | Canonical identifier |
| Implemented In | Code path(s) |
| Tests | Pytest module(s) |
| Benchmarks | Performance test or N/A |
| Owner | Team or individual |
| Status | Draft / MVP / Partial / Complete / Deferred |
| Release | REL package |
| Example | Runnable example or golden dataset |

**Index:** [APS/TRACEABILITY-INDEX.md](APS/TRACEABILITY-INDEX.md)

## Packages

| Package | Role |
|---------|------|
| `athena-os` | Infrastructure layer (event bus, config, plugins, logging) |
| `athena-core` | Domain and application logic |
| `athena-testing` | Golden datasets, benchmarks, smoke tests |
| `athena-sdk`, `athena-cli`, `athena-ai`, `athena-dashboard` | Interface adapters |

See [DEPENDENCY-RULES.md](DEPENDENCY-RULES.md) and [ADR-0005](../adrs/ADR-0005-athena-os.md).

## Reading Order

1. [Releases/](Releases/README.md) — what to build (REL packages)
2. [APS/Foundation/](APS/Foundation/README.md) — Phase 1 foundation frameworks (APS-001–015)
3. [APS/Data/](APS/Data/README.md) — Phase 2 data platform APS (51 specs)
4. [APS/Indicators/](APS/Indicators/README.md) — Phase 3 indicators APS (102 specs)
5. [APS/Patterns/](APS/Patterns/README.md) — Phase 4 patterns APS
6. [APS/Strategies/](APS/Strategies/README.md) — Phase 5 strategies APS (169 specs)
7. [APS/Simulation/](APS/Simulation/README.md) — Phase 6 simulation APS
8. [APS/Portfolio-Intelligence/](APS/Portfolio-Intelligence/README.md) — Phase 7 portfolio APS
9. [APS/Quantitative-Analytics/](APS/Quantitative-Analytics/README.md) — Phase 8 analytics APS
10. [APS/Research-Experimentation/](APS/Research-Experimentation/README.md) — Phase 9 QREP APS (140 specs)
11. [APS/](APS/README.md) — domain implementation specs (Backtesting, Portfolio, …)
12. [ADR/](ADR/README.md) — accepted architecture decisions
13. [Golden-Datasets/](Golden-Datasets/README.md) — reproducible test inputs

## Relationship to Legacy Paths

Existing documents under `athena-spec/` remain authoritative. This tree adds **indexes and Phase 1 Foundation APS** without breaking prior links:

| Legacy path | ATHENA path |
|-------------|-------------|
| `ATH-REL-*.md`, `release-*/` | [Releases/](Releases/README.md) |
| `feature-engineering/`, `backtesting/`, … | [APS/](APS/README.md) |
| `adrs/` | [ADR/](ADR/README.md) |
| `schemas/` | [Schemas/](Schemas/README.md) |
| `prompts/`, `*/prompts/` | [Prompts/](Prompts/README.md) |
| `*/benchmarks/` | [Benchmarks/](Benchmarks/README.md) |

**Phase 1 validation:** [PHASE-1-FOUNDATION-COMPLETE.md](../PHASE-1-FOUNDATION-COMPLETE.md)

**Phase 2 validation:** [PHASE-2-DATA-PLATFORM-COMPLETE.md](../PHASE-2-DATA-PLATFORM-COMPLETE.md)

**Phase 3 validation:** [PHASE-3-INDICATORS-COMPLETE.md](../PHASE-3-INDICATORS-COMPLETE.md)

**Phase 4 validation:** [PHASE-4-PATTERNS-COMPLETE.md](../PHASE-4-PATTERNS-COMPLETE.md)

**Phase 5 validation:** [PHASE-5-STRATEGIES-COMPLETE.md](../PHASE-5-STRATEGIES-COMPLETE.md)

**Phase 6 validation:** [PHASE-6-SIMULATION-COMPLETE.md](../PHASE-6-SIMULATION-COMPLETE.md)

**Phase 7 validation:** [PHASE-7-PORTFOLIO-COMPLETE.md](../PHASE-7-PORTFOLIO-COMPLETE.md)

**Phase 8 validation:** [PHASE-8-ANALYTICS-COMPLETE.md](../PHASE-8-ANALYTICS-COMPLETE.md)

**Phase 9 validation:** [PHASE-9-QREP-COMPLETE.md](../PHASE-9-QREP-COMPLETE.md)

**Source documents:** `References/PHASE1 -ATHENA FOUNDATION APS.docx` through `References/PHASE9 - Quantitative Research & Experimentation Platform (QREP).docx` (not committed; content captured in APS/).
