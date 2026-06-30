# APS-IND-WMA-001 — Weighted Moving Average

> **APS ID:** APS-IND-WMA-001  
> **Requirement ID:** REQ-APS-IND-WMA-001  
> **Maps to:** REQ-IND-IND-WMA-001  
> **Phase:** 3 — Indicators  
> **Domain:** Moving Averages  
> **Source:** `References/PHASE 3 Architecture.docx`  
> **Implementation status:** MVP

## Objective

Weighted Moving Average for the Athena indicators platform (moving averages domain).

## Responsibilities

- Weighted Moving Average computation
- Configurable parameters
- OHLCV input contract
- NaN/warmup policy

## Code Wiring (`athena-core`)

- `athena-core/src/athena_core/domain/indicators/wma.py`

## Dependencies

- Phase 1 Foundation APS (APS-001–015)
- Phase 2 Data Platform APS
- ATH-REL-004-Indicator-Framework.md

## Acceptance Criteria

- [ ] APS-IND-WMA-001 responsibilities covered by wired `athena-core` modules
- [ ] Maps to REQ-IND-IND-WMA-001 where applicable
- [ ] Unit tests pass for implemented behavior

## Unit Tests

`tests/test_indicator_framework.py`, `tests/test_indicator_aps.py`, `tests/test_indicator_architecture.py`

## Future Enhancements

- Full coverage per Indicator Specification Standard (formula, validation, benchmarks)
- Layered architecture: formulas / execution / adapters separation per CTO recommendation

---

*Template: [ATH-004 Requirement Standard](../../ATH-004-Requirement-Standard.md)*
