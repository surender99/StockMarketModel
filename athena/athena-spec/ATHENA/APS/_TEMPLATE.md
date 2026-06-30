# APS Specification Template

> **Standard:** ATH-004 Requirement Standard  
> **Traceability:** Required for all APS documents

---

## Traceability Block (required)

| Field | Value |
|-------|-------|
| **APS ID** | `APS-XXX-NNN` |
| **Implemented In** | `athena/athena-core/src/athena_core/...` or `athena/athena-os/src/athena_os/...` |
| **Tests** | `athena/athena-core/tests/test_*.py` |
| **Benchmarks** | `athena/athena-testing/benchmarks/` or N/A |
| **Owner** | `@team-or-individual` |
| **Status** | `Draft` \| `MVP` \| `Partial` \| `Complete` \| `Deferred` |
| **Release** | `REL-00N` |
| **Example** | Link to notebook, CLI command, or golden dataset |

---

## Header

> **APS ID:** APS-XXX-NNN  
> **Requirement ID:** REQ-APS-XXX-NNN  
> **Maps to:** REQ-...  
> **Phase:** N — Domain  
> **Source:** `References/PHASE N ...`

## Objective

One paragraph describing what this APS delivers.

## Responsibilities

- Primary responsibility
- Secondary responsibility

## Public API / Code Wiring

- Package path and public symbols

## Dependencies

- Upstream APS and REL packages

## Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Performance Target

N/A or link to [PERFORMANCE-GATES.md](../Benchmarks/PERFORMANCE-GATES.md)

## Unit Tests

List pytest modules and test function names.

## Integration Tests

Bootstrap, SDK, or end-to-end paths.

## Golden Dataset Validation

Link to `athena-spec/ATHENA/Golden-Datasets/` fixture used for validation. See [TRACEABILITY-INDEX.md](TRACEABILITY-INDEX.md).

## Future Enhancements

Deferred scope.

---

*Template: [ATH-004 Requirement Standard](../../ATH-004-Requirement-Standard.md)*
