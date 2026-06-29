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
└── Reviews/             CTO and revision review archives
```

## Reading Order

1. [Releases/](Releases/README.md) — what to build (REL packages)
2. [APS/Foundation/](APS/Foundation/README.md) — Phase 1 foundation frameworks (APS-001–015)
3. [APS/](APS/README.md) — domain implementation specs (Indicators, Patterns, …)
4. [ADR/](ADR/README.md) — accepted architecture decisions
5. [Golden-Datasets/](Golden-Datasets/README.md) — reproducible test inputs

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

**Source document:** `References/PHASE1 -ATHENA FOUNDATION APS.docx` (not committed; content captured in APS/Foundation/).
