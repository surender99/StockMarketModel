# APS-IND-ADX-001 — Average Directional Index

> **APS ID:** APS-IND-ADX-001  
> **Requirement ID:** REQ-APS-IND-ADX-001  
> **Maps to:** REQ-IND-ADX-001  
> **Phase:** 3 — Indicators  
> **Domain:** Trend Indicators  
> **Source:** `References/ATH-REL-004-Indicator-Framework.zip (inferred PHASE-3)`  
> **Implementation status:** MVP

## Objective

Average Directional Index for the Athena indicators (trend indicators domain).

## Responsibilities

- Trend strength
- +DI/-DI
- Configurable period

## Code Wiring (`athena-core`)

- `athena-core/src/athena_core/domain/indicators/adx.py`

## Dependencies

- Phase 1 Foundation APS (APS-001–015)
- Phase 2 Data Platform APS
- ATH-REL-004-Indicator-Framework.md

## Acceptance Criteria

- [ ] APS-IND-ADX-001 responsibilities covered by wired `athena-core` modules
- [ ] Maps to REQ-IND-ADX-001 where applicable
- [ ] Unit tests pass for implemented behavior

## Unit Tests

`tests/test_indicator_framework.py`, `tests/test_indicator_aps.py`

## Future Enhancements

- Full coverage of all responsibilities listed in source release package
- Extract to dedicated packages when surface area grows

---

*Template: [ATH-004 Requirement Standard](../../ATH-004-Requirement-Standard.md)*
