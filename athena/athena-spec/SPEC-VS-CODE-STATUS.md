# Spec vs Code Status

> **Purpose:** Distinguish **spec integration complete** (References → `athena-spec`) from **code implementation complete** (running software in `athena-core` and sibling packages).  
> **Updated:** 2026-06-30 — PHASE 1–15 + ATH-000A–D + REL-000–020 integration.

---

## Terminology

| Term | Meaning |
|------|---------|
| **Spec integration complete** | References package markdown, PHASE APS trees, contracts, and validation reports exist under `athena/athena-spec/`. |
| **Code MVP** | Runnable Python with unit tests; covers core paths, not full APS catalog. |
| **Code Partial** | Some APS implemented; large deferred backlog in catalog. |
| **Code Deferred** | APS spec published; no production implementation yet. |
| **MVP platform complete** | Phases 0–7 REQs implemented — see [PLATFORM-COMPLETE.md](PLATFORM-COMPLETE.md). |

A package can be **spec-complete** while **code-partial** or **code-absent**.

---

## PHASE 1–9 — Spec vs Code

| Phase | Platform | APS | Spec | Code | Honest Notes |
|-------|----------|-----|------|------|--------------|
| **1** | Foundation | 15 | ✅ | **Partial** | `athena-os` infrastructure layer; config, DI, plugins, events, logging; see ADR-0005 |
| **2** | Data Platform | 51 | ✅ | **Partial** | Ingest, calendar, quality, lineage, registry MVP; connectors microservices not split out |
| **3** | Indicators | 102 | ✅ | **MVP** | 19 builtin indicators; 77 deferred catalog entries; pipeline + metadata store wired |
| **4** | Patterns | 164 | ✅ | **Partial** | 12 builtin detectors; 164-entry intelligence catalog; Elliott/Wyckoff/SMC specs only |
| **5** | Strategies | 169 | ✅ | **MVP** | YAML engine + templates; optimizer/risk/exit APS mostly catalog |
| **6** | Simulation | 56 | ✅ | **MVP** | Backtest engine covers core loop; simulation catalog + event stubs |
| **7** | Portfolio Intelligence | 72 | ✅ | **MVP** | `PortfolioEngine`, rebalancing, exposure limits; optimizer/risk-budget deferred |
| **8** | Quantitative Analytics | 160 | ✅ | **MVP** | Analytics in `domain/analytics` and `domain/statistics` — **not** in indicators (ADR-0005) |
| **9** | Research & Experimentation | 140 | ✅ | **MVP** | QREP catalog, hypothesis, reproducibility, events; notebook/collaboration deferred |

**Master sign-off:** [ATHENA/REFERENCES-COMPLETE.md](ATHENA/REFERENCES-COMPLETE.md)

---

## PHASE 10–15 — Spec vs Code

| Phase | Platform | APS | Spec | Code | Honest Notes |
|-------|----------|-----|------|------|--------------|
| **10** | Machine Learning | 148 | ✅ | **MVP** | Dataset builder, training, registry, drift; deep learning/serving mostly deferred |
| **11** | Autonomous Intelligence | 110 | ✅ | **MVP** | Rule-based `athena-ai` agents; LLM orchestration deferred |
| **12** | Visualization & UX | 106 | ✅ | **MVP** | Streamlit dashboard; full chart/workspace suite deferred |
| **13** | Paper Trading | 85 | ✅ | **Stub** | Paper trading framework stubs only |
| **14** | Enterprise Trading | 102 | ✅ | **Stub** | OMS/RMS/broker gateway stubs |
| **15** | Enterprise Governance | 91 | ✅ | **Partial** | CI/pre-commit; full observability platform deferred |

**ATH-000A–D:** Spec integrated — [ATH-000-SERIES-INDEX.md](ATH-000-SERIES-INDEX.md)

---

## REL-000 … REL-020 — Spec vs Code

| REL | Spec | Code | Gap Summary |
|-----|------|------|-------------|
| **000** | ✅ | ✅ | CI/pre-commit enforced |
| **001** | ✅ | **Partial** | Core frameworks MVP; not all APS-001–015 modules extracted |
| **002** | ✅ | **Partial** | Single-package data MVP vs multi-service target |
| **003** | ✅ | **MVP** | Feature store + extended indicators |
| **004** | ✅ | **Partial** | 19/102 indicator APS implemented |
| **005** | ✅ | **Partial** | 12/164 pattern APS implemented |
| **006** | ✅ | **MVP** | Strategy engine + catalog |
| **007** | ✅ | **MVP** | Walk-forward backtest; advanced execution models partial |
| **008** | ✅ | **MVP** | PortfolioEngine; full PIP optimizer deferred |
| **009** | ✅ | **MVP** | Core metrics + bootstrap; full QARIP analytics deferred |
| **010** | ✅ | **MVP** | Experiment tracker + QREP modules; full notebook platform deferred |
| **011** | ✅ | **MVP** | ML scorer; deep learning/serving deferred |
| **012** | ✅ | **MVP** | Rule-based `athena-ai`; LLM generators stubbed |
| **013** | ✅ | **MVP** | Streamlit dashboard; full chart suite deferred |
| **014** | ✅ | **Stub** | Paper trading framework only |
| **015** | ✅ | **Stub** | Production gateway stubs |
| **016** | ✅ | **MVP** | Review framework; automated bots deferred |
| **017** | ✅ | **Stub** | Security framework; OAuth/encryption deferred |
| **018** | ✅ | **MVP** | CI/install; K8s/Terraform deferred |
| **019** | ✅ | **Stub** | Observability interfaces; Prometheus/Grafana deferred |
| **020** | ✅ | **MVP** | `AthenaClient`; REST/WS servers not running |

---

## References Packages 01–15 — Known Gaps

| Pkg | Name | Spec | Code | Notes |
|-----|------|------|------|-------|
| **04** | Market Intelligence | ✅ | **Partial** | Breadth engine done; sector rotation backlog |
| **06** | Pattern Recognition | ✅ | **Partial** | 12 patterns; 152 APS deferred |
| **09** | Portfolio Engine | ✅ | **MVP** | Rebalancing + limits; full AES-0901 backlog |
| **11** | Statistics | ✅ | **MVP** | Bootstrap Sharpe + Monte Carlo; sensitivity backlog |

Packages **01–03, 05, 07–08, 10, 12–15** are spec-integrated with MVP code where listed in [PLATFORM-COMPLETE.md](PLATFORM-COMPLETE.md) (22 core REQs).

---

## Test Coverage (2026-06-30)

| Package | Passed | Skipped |
|---------|--------|---------|
| athena-core | 354 | 10 |
| athena-sdk | 6 | 0 |
| athena-ai | 21 | 0 |
| athena-cli | 4 | 0 |
| athena-dashboard | 6 | 0 |
| **Total** | **391** | **10** |

Phase 9 adds `tests/test_qrep_aps.py` (7 tests) in athena-core. Phase 3–8 APS tests in `test_indicator_aps.py`, `test_pattern_aps.py`, `test_strategy_aps.py`, `test_phase678_aps.py`, `test_phase6_simulation.py`, `test_portfolio_intelligence_depth.py`.

---

## Quick Reference

| Document | What "complete" means there |
|----------|----------------------------|
| [ATHENA/REFERENCES-COMPLETE.md](ATHENA/REFERENCES-COMPLETE.md) | Master sign-off — PHASE 1–15, ATH-000A–D, REL 000–020, packages 01–15 |
| [REFERENCES-INTEGRATION-COMPLETE.md](REFERENCES-INTEGRATION-COMPLETE.md) | References packages 01–15 **specs** integrated |
| [REL-011-020-INTEGRATION-COMPLETE.md](REL-011-020-INTEGRATION-COMPLETE.md) | REL-011–020 spec + framework tests |
| [PLATFORM-COMPLETE.md](PLATFORM-COMPLETE.md) | MVP Phases 0–7 **code** + CI sign-off |
| [REV-2-IMPLEMENTATION-STATUS.md](REV-2-IMPLEMENTATION-STATUS.md) | Rev 2 portfolio/statistics/patterns **MVP** |
| [packages/PACKAGE-NN-COMPLETE.md](packages/) | Per-package **spec** validation |

---

## Related

- [ADRs](adrs/) — architectural decisions (data, plugins, monorepo)
- [decision-log/](decision-log/) — DEC-001 (phases), DEC-002 (References), DEC-003 (requirements layout)
