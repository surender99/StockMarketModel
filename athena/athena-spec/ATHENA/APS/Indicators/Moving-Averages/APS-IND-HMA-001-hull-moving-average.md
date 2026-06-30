# APS-IND-HMA-001 — Hull Moving Average

> **APS ID:** APS-IND-HMA-001  
> **Requirement ID:** REQ-APS-IND-HMA-001  
> **Maps to:** REQ-IND-IND-HMA-001  
> **Phase:** 3 — Indicators  
> **Domain:** Moving Averages  
> **Source:** `References/PHASE 3 Architecture.docx`  
> **Implementation status:** Deferred

## Objective

Hull Moving Average for the Athena indicators platform (moving averages domain).

## Responsibilities

- Hull Moving Average computation
- Configurable parameters
- OHLCV input contract
- NaN/warmup policy

## Code Wiring (`athena-core`)

- *(deferred — no MVP wiring yet)*

## Dependencies

- Phase 1 Foundation APS (APS-001–015)
- Phase 2 Data Platform APS
- ATH-REL-004-Indicator-Framework.md

## Acceptance Criteria

- [ ] APS-IND-HMA-001 spec published with REQ ID
- [ ] Deferred — no silent stub in production path
- [ ] Future implementation traces to REQ-IND-IND-HMA-001

## Unit Tests

`tests/test_indicator_framework.py`, `tests/test_indicator_aps.py`, `tests/test_indicator_architecture.py`

## Future Enhancements

- Full coverage per Indicator Specification Standard (formula, validation, benchmarks)
- Layered architecture: formulas / execution / adapters separation per CTO recommendation

---

*Template: [ATH-004 Requirement Standard](../../ATH-004-Requirement-Standard.md)*
