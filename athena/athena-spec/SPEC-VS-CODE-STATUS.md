# Spec vs Code Status

> **Purpose:** Distinguish **spec integration complete** (References → `athena-spec`) from **code implementation complete** (running software in `athena-core` and sibling packages).

---

## Terminology

| Term | Meaning |
|------|---------|
| **Spec integration complete** | References package markdown, contracts, and validation report exist under `athena/athena-spec/` (or handbook under `athena-docs/`). |
| **Code implementation complete** | Production Python (or interface) code exists, is tested, and meets linked REQ acceptance criteria. |
| **MVP platform complete** | Phases 0–7 REQs implemented — see [PLATFORM-COMPLETE.md](PLATFORM-COMPLETE.md). |
| **Rev 2 implementation** | Portfolio, statistics, and pattern MVPs — see [REV-2-IMPLEMENTATION-STATUS.md](REV-2-IMPLEMENTATION-STATUS.md). |

A package can be **spec-complete** while **code-partial** or **code-absent**.

---

## Packages with Spec–Code Gaps

| Pkg | Name | Spec | Code | Notes |
|-----|------|------|------|-------|
| **06** | Pattern Recognition | ✅ Integrated | ✅ **Rev 2+** | Scanner + feature store wired; 5 patterns (`bullish_engulfing`, `hammer`, `doji`, `morning_star`, `bull_flag`); catalog backlog |
| **09** | Portfolio Engine | ✅ Integrated | ✅ **Rev 2+** | Rebalancing + correlation/exposure limits in backtest; full AES-0901 backlog remains |
| **11** | Statistics | ✅ Integrated | ✅ **Rev 2+** | Bootstrap Sharpe + Monte Carlo robustness; parameter sensitivity backlog |

All other References packages (01–05, 07–08, 10, 12–15) are spec-integrated; MVP code exists where listed in PLATFORM-COMPLETE REQ table (22 REQs). Package **04** breadth engine (`REQ-MI-001`) implemented; sector rotation backlog remains. Package **05** adds STOCH (`REQ-IND-STOCH-001`).

---

## Quick Reference

| Document | What "complete" means there |
|----------|----------------------------|
| [REFERENCES-INTEGRATION-COMPLETE.md](REFERENCES-INTEGRATION-COMPLETE.md) | All 15 References **specs** integrated |
| [PLATFORM-COMPLETE.md](PLATFORM-COMPLETE.md) | MVP Phases 0–7 **code** + CI sign-off |
| [REV-2-IMPLEMENTATION-STATUS.md](REV-2-IMPLEMENTATION-STATUS.md) | Rev 2 portfolio/statistics/patterns **MVP** |
| [packages/PACKAGE-NN-COMPLETE.md](packages/) | Per-package **spec** validation |

---

## Related

- [ADRs](adrs/) — architectural decisions (data, plugins, monorepo)
- [decision-log/](decision-log/) — DEC-001 (phases), DEC-002 (References), DEC-003 (requirements layout)
