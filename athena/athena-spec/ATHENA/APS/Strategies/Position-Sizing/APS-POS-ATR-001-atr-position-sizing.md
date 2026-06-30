# APS-POS-ATR-001 — ATR Position Sizing

> **APS ID:** APS-POS-ATR-001  
> **Requirement ID:** REQ-APS-POS-ATR-001  
> **Phase:** 5 — Strategies  
> **Domain:** Position Sizing  
> **Source:** `References/PHASE5 - Strategy Intelligence Platform (SIP).docx`  
> **Implementation status:** Deferred

## Objective

ATR Position Sizing for the Athena strategies platform (position sizing domain).

## Responsibilities

- ATR Position Sizing
- Strategy decision layer integration
- Signal/risk qualification
- Explainable trade decisions

## Code Wiring (`athena-core`)

- *(deferred — no MVP wiring yet)*

## Dependencies

- Phase 1 Foundation APS (APS-001–015)
- Phase 2 Data Platform APS
- Phase 3 Indicators APS
- [ATH-REL-006-Strategy-Engine.md](../../ATH-REL-006-Strategy-Engine.md)

## Acceptance Criteria

- [ ] APS-POS-ATR-001 spec published with REQ ID
- [ ] MVP modules wired where status is MVP/Partial
- [ ] Deferred APS have no silent production stub

## Unit Tests

`tests/test_strategy_engine_framework.py`, `tests/test_strategy_aps.py`, `tests/test_phase45_aps.py`

---

*Template: [ATH-004 Requirement Standard](../../ATH-004-Requirement-Standard.md)*
