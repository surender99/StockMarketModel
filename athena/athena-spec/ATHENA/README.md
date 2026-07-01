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
├── Phase-Requirements/  Product phases PR-01 … PR-10 (Paper Trader)
├── Epics/               Delivery epics EPIC-001 … EPIC-015
├── Features/            Feature packages (75) under epics
├── Stories/             User stories (32) by domain
├── Tasks/               Engineering tasks (32) by domain
├── Milestones/          Delivery milestones MS-1 … MS-17 (engineering + IPs)
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
| `athena-common` | Shared domain types (Money, OHLC, TimeFrame, enums) |
| `athena-os` | Infrastructure layer (event bus, config, plugins, logging) |
| `athena-domain` | Engine interface contracts (Protocol) |
| `athena-core` | Domain and application logic |
| `athena-core-runtime`, `athena-core-events`, `athena-core-engine`, `athena-core-metadata` | Core facades (Phase 3 extraction) |
| `athena-data`, `athena-indicators`, `athena-patterns`, `athena-strategies`, `athena-risk`, `athena-portfolio`, `athena-execution` | Bounded-context facades (re-export core) |
| `athena-metadata`, `athena-observability`, `athena-market`, `athena-brokers` | Extension facades (metadata, ops, market, brokers) |
| `athena-platform` | Production runtime assembly |
| `athena-math` | Statistics/math utilities (independent from trading logic) |
| `athena-research` | Research workspace (non-production) |
| `athena-testing` | Golden datasets, benchmarks, architecture tests |
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
11. [APS/Machine-Learning/](APS/Machine-Learning/README.md) — Phase 10 MLP APS (148 specs)
12. [APS/Autonomous-Intelligence/](APS/Autonomous-Intelligence/README.md) — Phase 11 AQIP APS (110 specs)
13. [APS/Visualization-UX/](APS/Visualization-UX/README.md) — Phase 12 VDSUX APS (106 specs)
14. [APS/Paper-Trading/](APS/Paper-Trading/README.md) — Phase 13 PTEVP APS (85 specs)
15. [APS/Enterprise-Trading/](APS/Enterprise-Trading/README.md) — Phase 14 ETOP APS (102 specs)
16. [APS/Enterprise-Governance/](APS/Enterprise-Governance/README.md) — Phase 15 EGPCI APS (91 specs)
17. [Architecture/](Architecture/00-README.md) — ATH-000A core architecture reference
18. [AthenaOS/](AthenaOS/00-README.md) — ATH-001 runtime/infrastructure specification
19. [Dependency-Graph/](Dependency-Graph/00-README.md) — ATH-002 module dependency graph
20. [Contracts-Standards/](Contracts-Standards/00-README.md) — ATH-000C contracts/events/API standards
21. [../events/](../events/README.md) — ATH-003 event catalog + standards
22. [../interfaces/](../interfaces/README.md) — ATH-004 interface catalog + standards
23. [../database/](../database/00-README.md) — ATH-005 database catalog
24. [../implementation-packages/](../implementation-packages/ATH-IP-Starter-Pack/README.md) — ATH-IP starter IPs
25. [Epics/](Epics/README.md) — EPIC-001 … EPIC-015 delivery epics
26. [Features/](Features/README.md) — feature packages under epics
27. [Stories/](Stories/README.md) — user stories
28. [Tasks/](Tasks/README.md) — engineering tasks
29. [Milestones/](Milestones/README.md) — MS-1 … MS-17 milestone delivery specs
30. [APS/](APS/README.md) — domain implementation specs (Backtesting, Portfolio, …)
31. [ADR/](ADR/README.md) — accepted architecture decisions
32. [Golden-Datasets/](Golden-Datasets/README.md) — reproducible test inputs

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

**Phase 10 validation:** [PHASE-10-MLP-COMPLETE.md](../PHASE-10-MLP-COMPLETE.md)

**Phase 11 validation:** [PHASE-11-AQIP-COMPLETE.md](../PHASE-11-AQIP-COMPLETE.md)

**Phase 12 validation:** [PHASE-12-VDSUX-COMPLETE.md](../PHASE-12-VDSUX-COMPLETE.md)

**Phase 13 validation:** [PHASE-13-PTEVP-COMPLETE.md](../PHASE-13-PTEVP-COMPLETE.md)

**Phase 14 validation:** [PHASE-14-ETOP-COMPLETE.md](../PHASE-14-ETOP-COMPLETE.md)

**Phase 15 validation:** [PHASE-15-EGPCI-COMPLETE.md](../PHASE-15-EGPCI-COMPLETE.md)

**ATH-000 series:** [ATH-000-SERIES-INDEX.md](../ATH-000-SERIES-INDEX.md)

**ATH-001 series:** [ATH-001-SERIES-INDEX.md](../ATH-001-SERIES-INDEX.md)

**Milestone series:** [MILESTONE-SERIES-INDEX.md](../MILESTONE-SERIES-INDEX.md)

**Delivery hierarchy:** [DELIVERY-HIERARCHY-INDEX.md](../DELIVERY-HIERARCHY-INDEX.md)

**Product phases:** [PHASE-REQUIREMENTS-INDEX.md](../PHASE-REQUIREMENTS-INDEX.md)

**Source documents:** `References/PHASE1 -ATHENA FOUNDATION APS.docx` through `References/PHASE15 - Enterprise Governance...docx`, `References/ATH-000*.zip`, and `References/ATH-001*.zip` … `ATH-005*.zip`, `ATH-IP-Starter-Pack.zip`, `ATH-Milestone-*.zip`, `ATH-*-MASTER.zip`, `ATH-PHASE-REQUIREMENTS.zip` (not committed; content captured in spec).
