# APS-IND-WILLR-001 — Williams Percent R

> **APS ID:** APS-IND-WILLR-001  
> **Requirement ID:** REQ-APS-IND-WILLR-001  
> **Maps to:** REQ-IND-WILLR-001  
> **Phase:** 3 — Indicators  
> **Domain:** Oscillators  
> **Source:** `References/ATH-REL-004-Indicator-Framework.zip (inferred PHASE-3)`  
> **Implementation status:** MVP

## Objective

Williams Percent R for the Athena indicators (oscillators domain).

## Responsibilities

- Overbought/oversold oscillator
- Configurable period

## Code Wiring (`athena-core`)

- `athena-core/src/athena_core/domain/indicators/willr.py`

## Dependencies

- Phase 1 Foundation APS (APS-001–015)
- Phase 2 Data Platform APS
- ATH-REL-004-Indicator-Framework.md

## Acceptance Criteria

- [ ] APS-IND-WILLR-001 responsibilities covered by wired `athena-core` modules
- [ ] Maps to REQ-IND-WILLR-001 where applicable
- [ ] Unit tests pass for implemented behavior

## Unit Tests

`tests/test_indicator_framework.py`, `tests/test_indicator_aps.py`

## Future Enhancements

- Full coverage of all responsibilities listed in source release package
- Extract to dedicated packages when surface area grows

---

*Template: [ATH-004 Requirement Standard](../../ATH-004-Requirement-Standard.md)*
