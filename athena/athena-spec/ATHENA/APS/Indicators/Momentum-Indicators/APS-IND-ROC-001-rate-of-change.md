# APS-IND-ROC-001 — Rate of Change

> **APS ID:** APS-IND-ROC-001  
> **Requirement ID:** REQ-APS-IND-ROC-001  
> **Maps to:** REQ-IND-ROC-001  
> **Phase:** 3 — Indicators  
> **Domain:** Momentum Indicators  
> **Source:** `References/ATH-REL-004-Indicator-Framework.zip (inferred PHASE-3)`  
> **Implementation status:** MVP

## Objective

Rate of Change for the Athena indicators (momentum indicators domain).

## Responsibilities

- Momentum percent change
- Configurable period

## Code Wiring (`athena-core`)

- `athena-core/src/athena_core/domain/indicators/roc.py`

## Dependencies

- Phase 1 Foundation APS (APS-001–015)
- Phase 2 Data Platform APS
- ATH-REL-004-Indicator-Framework.md

## Acceptance Criteria

- [ ] APS-IND-ROC-001 responsibilities covered by wired `athena-core` modules
- [ ] Maps to REQ-IND-ROC-001 where applicable
- [ ] Unit tests pass for implemented behavior

## Unit Tests

`tests/test_indicator_framework.py`, `tests/test_indicator_aps.py`

## Future Enhancements

- Full coverage of all responsibilities listed in source release package
- Extract to dedicated packages when surface area grows

---

*Template: [ATH-004 Requirement Standard](../../ATH-004-Requirement-Standard.md)*
