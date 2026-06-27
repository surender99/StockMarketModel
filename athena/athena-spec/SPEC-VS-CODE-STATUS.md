# Spec vs Code Status

> **Purpose:** Distinguish **spec integration complete** (References → `athena-spec`) from **code implementation complete** (running software in `athena-core` and sibling packages).

---

## Terminology

| Term | Meaning |
|------|---------|
| **Spec integration complete** | References package markdown, contracts, and validation report exist under `athena/athena-spec/` (or handbook under `athena-docs/`). |
| **Code implementation complete** | Production Python (or interface) code exists, is tested, and meets linked REQ acceptance criteria. |
| **MVP platform complete** | Phases 0–7 REQs implemented — see [PLATFORM-COMPLETE.md](PLATFORM-COMPLETE.md). |

A package can be **spec-complete** while **code-partial** or **code-absent**.

---

## Packages with Spec–Code Gaps

| Pkg | Name | Spec | Code | Notes |
|-----|------|------|------|-------|
| **06** | Pattern Recognition | ✅ Integrated | ⚠️ **Stub only** | `PatternDetector` stub in `athena_core.domain.patterns`; no chart/candlestick detectors |
| **09** | Portfolio Engine | ✅ Integrated | ❌ **Spec only** | REQ-PF-* documented; no portfolio engine service in `athena-core` |
| **11** | Statistics | ✅ Integrated | ❌ **Spec only** | AES-1100/1101 specs; robustness validation not yet a code module |

All other References packages (01–05, 07–08, 10, 12–15) are spec-integrated; MVP code exists where listed in PLATFORM-COMPLETE REQ table (22 REQs).

---

## Quick Reference

| Document | What "complete" means there |
|----------|----------------------------|
| [REFERENCES-INTEGRATION-COMPLETE.md](REFERENCES-INTEGRATION-COMPLETE.md) | All 15 References **specs** integrated |
| [PLATFORM-COMPLETE.md](PLATFORM-COMPLETE.md) | MVP Phases 0–7 **code** + CI sign-off |
| [packages/PACKAGE-NN-COMPLETE.md](packages/) | Per-package **spec** validation |

---

## Related

- [ADRs](adrs/) — architectural decisions (data, plugins, monorepo)
- [decision-log/](decision-log/) — DEC-001 (phases), DEC-002 (References), DEC-003 (requirements layout)
