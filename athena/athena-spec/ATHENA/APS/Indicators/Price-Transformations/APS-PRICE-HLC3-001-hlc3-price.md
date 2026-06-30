# APS-PRICE-HLC3-001 — HLC3 Price

> **APS ID:** APS-PRICE-HLC3-001  
> **Requirement ID:** REQ-APS-PRICE-HLC3-001  
> **Maps to:** REQ-IND-PRICE-HLC3-001  
> **Phase:** 3 — Indicators  
> **Domain:** Price Transformations  
> **Source:** `References/PHASE 3 Architecture.docx`  
> **Implementation status:** MVP

## Objective

HLC3 Price for the Athena indicators platform (price transformations domain).

## Responsibilities

- HLC3 Price computation
- Configurable parameters
- OHLCV input contract
- NaN/warmup policy

## Code Wiring (`athena-core`)

- `athena-core/src/athena_core/domain/indicators/price_transforms.py`

## Dependencies

- Phase 1 Foundation APS (APS-001–015)
- Phase 2 Data Platform APS
- ATH-REL-004-Indicator-Framework.md

## Acceptance Criteria

- [ ] APS-PRICE-HLC3-001 responsibilities covered by wired `athena-core` modules
- [ ] Maps to REQ-IND-PRICE-HLC3-001 where applicable
- [ ] Unit tests pass for implemented behavior

## Unit Tests

`tests/test_indicator_framework.py`, `tests/test_indicator_aps.py`, `tests/test_indicator_architecture.py`

## Future Enhancements

- Full coverage per Indicator Specification Standard (formula, validation, benchmarks)
- Layered architecture: formulas / execution / adapters separation per CTO recommendation

---

*Template: [ATH-004 Requirement Standard](../../ATH-004-Requirement-Standard.md)*
