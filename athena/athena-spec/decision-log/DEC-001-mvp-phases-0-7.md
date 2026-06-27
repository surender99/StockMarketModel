# DEC-001 – MVP Phases 0–7 Scope and Completion

> **Date:** 2026-06-27  
> **Status:** Accepted  
> **Related:** [PLATFORM-COMPLETE.md](../PLATFORM-COMPLETE.md), [ATH-001 MVP Scope](../ATH-001-MVP-Scope.md)

## Decision

MVP delivery is defined as **Phases 0–7** in the `athena/` monorepo:

| Phase | Scope | Completion meaning |
|-------|-------|-------------------|
| 0 | Monorepo scaffold, ATH specs, REQ backlog | Spec + repo structure in place |
| 1 | Data ingest, calendar, EMA/SMA, feature store | Code + tests |
| 2 | Strategy YAML, backtest, experiment tracking | Code + tests |
| 3 | Walk-forward, scanner, regime, experiment compare | Code + tests |
| 4 | Optimizer, ML scorer, explainability | Code + tests |
| 5 | CLI, SDK, dashboard | Code + tests |
| 6 | AI research assistant | Code + tests |
| 7 | CI, install scripts, platform sign-off | CI + docs |

**Phase 7 "complete"** means the research loop is CI-gated and documented — not that every References package has full code implementation.

## Rationale

Phases 0–6 were the original delivery milestones. Phase 7 adds operational polish (CI matrix, install scripts, Optuna, model persistence) without expanding functional scope into portfolio engine or full pattern recognition.

## Consequences

- PLATFORM-COMPLETE.md sign-off applies to Phases 0–7 MVP REQs (22 implemented).
- Post-MVP work (portfolio engine code, statistics module, pattern detectors) is tracked in [SPEC-VS-CODE-STATUS.md](../SPEC-VS-CODE-STATUS.md).
