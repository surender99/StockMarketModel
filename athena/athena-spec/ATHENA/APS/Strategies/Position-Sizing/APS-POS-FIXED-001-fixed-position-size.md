# APS-POS-FIXED-001 — Fixed Position Size

> **APS ID:** APS-POS-FIXED-001  
> **Requirement ID:** REQ-APS-POS-FIXED-001  
> **Phase:** 5 — Strategies  
> **Domain:** Position Sizing  
> **Source:** `References/PHASE5 - Strategy Intelligence Platform (SIP).docx`  
> **Implementation status:** MVP

## Objective

Fixed Position Size for the Athena strategies platform (position sizing domain).

## Responsibilities

- Fixed Position Size
- Strategy decision layer integration
- Signal/risk qualification
- Explainable trade decisions

## Code Wiring (`athena-core`)

- `athena-core/src/athena_core/domain/strategy/position_sizing.py`

## Dependencies

- Phase 1 Foundation APS (APS-001–015)
- Phase 2 Data Platform APS
- Phase 3 Indicators APS
- [ATH-REL-006-Strategy-Engine.md](../../ATH-REL-006-Strategy-Engine.md)

## Acceptance Criteria

- [ ] APS-POS-FIXED-001 spec published with REQ ID
- [ ] MVP modules wired where status is MVP/Partial
- [ ] Deferred APS have no silent production stub

## Unit Tests

`tests/test_strategy_engine_framework.py`, `tests/test_strategy_aps.py`, `tests/test_phase45_aps.py`

---

*Template: [ATH-004 Requirement Standard](../../ATH-004-Requirement-Standard.md)*
