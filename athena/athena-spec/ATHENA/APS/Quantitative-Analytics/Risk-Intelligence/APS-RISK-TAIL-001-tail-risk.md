# APS-RISK-TAIL-001 — Tail Risk

> **APS ID:** APS-RISK-TAIL-001  
> **Requirement ID:** REQ-APS-RISK-TAIL-001  
> **Phase:** 8 — Quantitative Analytics  
> **Domain:** Risk Intelligence  
> **Source:** `References/PHASE8 - Quantitative Analytics & Risk Intelligence Platform (QARIP).docx`  
> **Implementation status:** Partial

## Objective

Tail Risk for the Athena quantitative analytics and risk intelligence platform (QARIP).

## Code Wiring (`athena-core`)

- `athena-core/src/athena_core/domain/analytics/risk.py`
- `athena-core/src/athena_core/domain/statistics/risk_metrics.py`

## Dependencies

- Phase 1–7 APS prerequisites
- [ATH-REL-009-Statistics-and-Analytics-Engine.md](../../ATH-REL-009-Statistics-and-Analytics-Engine.md)

## Acceptance Criteria

- [ ] APS-RISK-TAIL-001 spec published with REQ ID
- [ ] MVP modules wired where status is MVP/Partial
- [ ] Deferred APS have no silent production stub

---

*Template: [ATH-004 Requirement Standard](../../ATH-004-Requirement-Standard.md)*
