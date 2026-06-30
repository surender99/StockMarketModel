# APS-STRAT-SIZE-001 — Position Sizing

> **APS ID:** APS-STRAT-SIZE-001  
> **Requirement ID:** REQ-APS-STRAT-SIZE-001  
> **Maps to:** REQ-STRAT-SIZE-001  
> **Phase:** 5 — Strategies  
> **Domain:** Position Sizing  
> **Source:** `References/REL-006-Strategy Engine.docx (inferred PHASE-5)`  
> **Implementation status:** MVP

## Objective

Position Sizing for the Athena strategies (position sizing domain).

## Responsibilities

- Fixed fractional
- Risk-based sizing
- Max position cap

## Code Wiring (`athena-core`)

- `athena-core/src/athena_core/domain/strategy/position_sizing.py`

## Dependencies

- Phase 1 Foundation APS (APS-001–015)
- Phase 2 Data Platform APS
- ATH-REL-006-Strategy-Engine.md

## Acceptance Criteria

- [ ] APS-STRAT-SIZE-001 responsibilities covered by wired `athena-core` modules
- [ ] Maps to REQ-STRAT-SIZE-001 where applicable
- [ ] Unit tests pass for implemented behavior

## Unit Tests

`tests/test_strategy_engine_framework.py`, `tests/test_strategy_aps.py`

## Future Enhancements

- Full coverage of all responsibilities listed in source release package
- Extract to dedicated packages when surface area grows

---

*Template: [ATH-004 Requirement Standard](../../ATH-004-Requirement-Standard.md)*
