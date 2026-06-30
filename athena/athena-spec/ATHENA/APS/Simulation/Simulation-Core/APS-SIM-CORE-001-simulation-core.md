# APS-SIM-CORE-001 — Simulation Core

> **APS ID:** APS-SIM-CORE-001  
> **Requirement ID:** REQ-APS-SIM-CORE-001  
> **Phase:** 6 — Simulation  
> **Domain:** Simulation Core  
> **Source:** `References/PHASE6 - Simulation & Backtesting Platform (SBP).docx`  
> **Implementation status:** Partial

## Objective

Simulation Core for the Athena simulation platform.

## Code Wiring (`athena-core`)

- `athena-core/src/athena_core/domain/simulation/catalog.py`
- `athena-core/src/athena_core/application/backtest_engine.py`

## Dependencies

- Phase 1–5 APS prerequisites
- [ATH-REL-007-Backtesting-Engine.md](../../ATH-REL-007-Backtesting-Engine.md)

## Acceptance Criteria

- [ ] APS-SIM-CORE-001 spec published with REQ ID
- [ ] MVP modules wired where status is MVP/Partial
- [ ] Deferred APS have no silent production stub

---

*Template: [ATH-004 Requirement Standard](../../ATH-004-Requirement-Standard.md)*
