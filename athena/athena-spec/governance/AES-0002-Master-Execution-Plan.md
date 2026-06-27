# AES-0002 – Master Execution Plan

> **References source:** `References/Athena-Package-01-Governance/governance/AES-0002-Master-Execution-Plan.md`  
> **Platform status:** [PLATFORM-COMPLETE.md](../PLATFORM-COMPLETE.md)

Athena evolves through **fixed version milestones**. Never skip versions — each release must satisfy its Definition of Done before advancing.

---

## Version Ladder

| Version | Focus | ATH / Repo Mapping | Status |
|---------|-------|-------------------|--------|
| **v0.0** | Foundation — governance, monorepo, specs | Phase 0 | ✅ Complete |
| **v0.1** | Research Foundation — data, calendar, indicators, feature store | Phase 1 | ✅ Complete |
| **v0.2** | Strategy Framework — YAML strategies, backtest, experiments | Phase 2 | ✅ Complete |
| **v0.3** | Advanced Research — walk-forward, regime, scanner, compare | Phase 3 | ✅ Complete |
| **v0.4** | Machine Learning — optimizer, ML scorer, explainability | Phase 4 | ✅ Complete |
| **v0.5** | Research Intelligence — CLI, SDK, dashboard | Phase 5 | ✅ Complete |
| **v0.6** | AI Research Scientist — NL orchestration (`athena-ai`) | Phase 6 | ✅ Complete |
| **v0.7** | Paper Trading — profiles, scan output, research dry-run | Phase 5–6 polish | ✅ Partial (MVP) |
| **v1.0** | Production — CI, install, sign-off, research-ready platform | Phase 7 | ✅ Complete (research) |

**Rule:** Do not declare a higher version complete until the prior version's [Definition of Done](../checklists/Definition-of-Done.md) is satisfied.

---

## Sprint Alignment (AES Roadmap)

| Sprint | Package | Scope |
|--------|---------|-------|
| Sprint 0 | Package 01 — Governance | Constitution, standards, templates, DoD |
| Sprint 1 | Package 03 — Data Platform | Data contracts, OHLCV schema, quality |
| Sprint 2 | Package 04 — Market Intelligence | Regime, breadth, relative strength |
| Sprint 3 | Package 05–07 — Features, Patterns, Strategy | Indicators, patterns, strategy engine |
| Sprint 4 | Package 08 — Backtesting | Execution model, metrics |
| Sprint 5 | Package 09 — Portfolio | Risk, allocation |
| Sprint 6 | Package 10 — Research | Experiment lifecycle |
| Sprint 7 | Package 11–12 — Statistics, ML | Validation framework, ML lifecycle |
| Sprint 8 | Package 13 — AI Research Scientist | Knowledge, review workflows |
| Sprint 9 | Package 14–15 — Platform, Handbook | Production platform, operator handbook |

See [REFERENCES-INDEX.md](../REFERENCES-INDEX.md) for package integration status.

---

## Next Milestones (Post v1.0)

| Target | Scope |
|--------|-------|
| **v1.1** | Package 02–03 integration — architecture contracts, data platform hardening |
| **v1.2** | Live paper-trading hooks, broker adapter stubs |
| **v2.0** | Production trading (requires independent data vendor, risk controls, security review) |

---

## Related Documents

- [ATH-001 Vision & PRD](../ATH-001-Vision-PRD.md) — module roadmap
- [ATH-001-MVP-Scope.md](../ATH-001-MVP-Scope.md) — phased delivery detail
- [PLATFORM-COMPLETE.md](../PLATFORM-COMPLETE.md) — current sign-off
- [checklists/Definition-of-Done.md](../checklists/Definition-of-Done.md)
