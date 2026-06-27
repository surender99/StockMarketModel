# Definition of Done

> **References source:** `References/Athena-Package-01-Governance/checklists/Definition-of-Done.md`  
> **Applies to:** Every REQ, phase gate, and References package integration

A deliverable is **done** only when all items below are satisfied.

---

## Checklist

| # | Criterion | Evidence |
|---|-----------|----------|
| 1 | **Requirements complete** | REQ spec in [requirements/](../requirements/) with acceptance criteria met |
| 2 | **Tests pass** | `pytest` green in affected packages; CI passing |
| 3 | **Benchmarks executed** | Performance or quant benchmarks run when REQ specifies targets (see package `benchmarks/`) |
| 4 | **Documentation updated** | Spec, README, or docstrings reflect new behavior |
| 5 | **Code reviewed** | PR reviewed or solo sign-off documented in phase validation |
| 6 | **Architecture compliant** | [ATH-003](../ATH-003-Repository-Architecture.md) layers; no domain I/O |
| 7 | **Quant standards** | [AES-0005](../governance/AES-0005-Quant-Standards.md) satisfied for research modules |

---

## Package Integration DoD (References → athena-spec)

When integrating an Athena References package:

- [ ] Source markdown read from `References/Athena-Package-NN-*`
- [ ] Canonical copy or merge in `athena/athena-spec/`
- [ ] `REFERENCES-INDEX.md` updated
- [ ] `packages/PACKAGE-NN-COMPLETE.md` validation report added
- [ ] No duplicate canonical specs (cross-link instead)
- [ ] Existing tests still pass

---

## Related Documents

- [AES-0002 Master Execution Plan](../governance/AES-0002-Master-Execution-Plan.md)
- [AES-0006 AI Coding Standards](../governance/AES-0006-AI-Coding-Standards.md)
- [PLATFORM-COMPLETE.md](../PLATFORM-COMPLETE.md)
