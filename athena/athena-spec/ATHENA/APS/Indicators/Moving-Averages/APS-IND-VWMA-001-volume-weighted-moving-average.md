# APS-IND-VWMA-001 — Volume Weighted Moving Average

> **APS ID:** APS-IND-VWMA-001  
> **Requirement ID:** REQ-APS-IND-VWMA-001  
> **Maps to:** REQ-IND-VWMA-001  
> **Phase:** 3 — Indicators  
> **Domain:** Moving Averages  
> **Source:** `References/ATH-REL-004-Indicator-Framework.zip (inferred PHASE-3)`  
> **Implementation status:** Deferred

## Objective

Volume Weighted Moving Average for the Athena indicators (moving averages domain).

## Responsibilities

- Volume-weighted prices
- Configurable period

## Code Wiring (`athena-core`)

- *(deferred — no MVP wiring yet)*

## Dependencies

- Phase 1 Foundation APS (APS-001–015)
- Phase 2 Data Platform APS
- ATH-REL-004-Indicator-Framework.md

## Acceptance Criteria

- [ ] APS-IND-VWMA-001 spec published with REQ ID
- [ ] Deferred — no silent stub in production path
- [ ] Future implementation traces to REQ-IND-VWMA-001

## Unit Tests

`tests/test_indicator_framework.py`, `tests/test_indicator_aps.py`

## Future Enhancements

- Full coverage of all responsibilities listed in source release package
- Extract to dedicated packages when surface area grows

---

*Template: [ATH-004 Requirement Standard](../../ATH-004-Requirement-Standard.md)*
