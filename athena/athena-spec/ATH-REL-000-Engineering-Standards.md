# ATH-REL-000 – Engineering Standards (Release-00)

> **Version:** v0.1  
> **Source:** `References/ATH-REL-000-Engineering-Standards-v0.1.zip`  
> **Status:** Spec-integrated (skeleton release package)  
> **Validation:** [packages/PACKAGE-REL-000-COMPLETE.md](packages/PACKAGE-REL-000-COMPLETE.md)

ATH-REL-000 is the **master engineering standards release package** for Athena Release-00. It defines the taxonomy and folder structure for all mandatory engineering standards that govern future development.

---

## Purpose

| Aspect | Detail |
|--------|--------|
| **What** | Top-level release artifact bundling constitution, governance, coding, testing, quality gates, and playbooks |
| **When** | Applied before and during all Athena package and MVP development |
| **Who** | Human developers and AI coding agents (see [AES-0006](governance/AES-0006-AI-Coding-Standards.md)) |

Release-00 v0.1 ships as a **skeleton**: section READMEs are placeholders. Canonical, actionable content lives in existing ATH and AES documents cross-linked from [engineering-standards/](engineering-standards/README.md).

---

## Relationship to Existing Standards

| ID | Role | Canonical Path |
|----|------|----------------|
| **ATH-REL-000** | Release package index and section taxonomy | This document |
| **ATH-002** | Engineering standards (coding, architecture, testing policy) | [ATH-002-Engineering-Standards.md](ATH-002-Engineering-Standards.md) |
| **AES-0004** | Engineering standards (References Package 01) | Merged into ATH-002 — no standalone file ([PACKAGE-01-COMPLETE](packages/PACKAGE-01-COMPLETE.md)) |
| **AES-0006** | AI coding workflow and agent rules | [governance/AES-0006-AI-Coding-Standards.md](governance/AES-0006-AI-Coding-Standards.md) |
| **AES-0001** | Engineering constitution principles | [governance/AES-0001-Constitution.md](governance/AES-0001-Constitution.md) / [ATH-000](ATH-000-Philosophy.md) |
| **AES-0005** | Quant research standards | [governance/AES-0005-Quant-Standards.md](governance/AES-0005-Quant-Standards.md) |

**Reading order:** ATH-REL-000 (this index) → ATH-002 (rules) → AES-0006 (AI workflow) → domain REQ and contracts.

---

## Release Package Sections (v0.1)

| # | Section | Zip Folder | Canonical Spec |
|---|---------|------------|----------------|
| 00 | Engineering Constitution | `00-Constitution` | [ATH-000](ATH-000-Philosophy.md), [AES-0001](governance/AES-0001-Constitution.md) |
| 01 | Governance | `01-Governance` | [governance/](governance/), [adrs/](adrs/), [decision-log/](decision-log/) |
| 02 | Repository Standards | `02-Repository` | [ATH-003](ATH-003-Repository-Architecture.md), [architecture/AES-0203](architecture/) |
| 03 | Architecture Standards | `03-Architecture` | [ATH-003](ATH-003-Repository-Architecture.md), [architecture/](architecture/) |
| 04 | Coding Standards | `04-Coding-Standards` | [ATH-002](ATH-002-Engineering-Standards.md) |
| 05 | Documentation Standards | `05-Documentation` | [ATH-004](ATH-004-Requirement-Standard.md), [templates/](templates/) |
| 06 | Requirement Engineering | `06-Requirement-Engineering` | [ATH-004](ATH-004-Requirement-Standard.md), [requirements/](requirements/) |
| 07 | AI Development | `07-AI-Development` | [AES-0006](governance/AES-0006-AI-Coding-Standards.md), [prompts/](prompts/) |
| 08 | Testing Standards | `08-Testing` | [ATH-002](ATH-002-Engineering-Standards.md), [checklists/Definition-of-Done](checklists/Definition-of-Done.md) |
| 09 | Benchmark Standards | `09-Benchmarks` | [athena-core/benchmarks/](../athena-core/benchmarks/README.md) |
| 10 | Quality Gates | `10-Quality-Gates` | [.github/workflows/ci.yml](../../.github/workflows/ci.yml), [.pre-commit-config.yaml](../../.pre-commit-config.yaml) |
| 11 | Templates | `11-Templates` | [templates/](templates/) |
| 12 | Developer Playbooks | `12-Developer-Playbooks` | [athena-docs/handbook/](../athena-docs/handbook/) |
| 13 | ADR & RFC | `13-ADR-RFC` | [adrs/](adrs/), [templates/ADR-Template.md](templates/ADR-Template.md) |
| 14 | Release Management | `14-Release-Management` | [CHANGELOG.md](../../CHANGELOG.md), [PLATFORM-COMPLETE](PLATFORM-COMPLETE.md) |
| 15 | Master Index | `15-Master-Index` | [README.md](README.md), [REFERENCES-INDEX](REFERENCES-INDEX.md) |

Full section index: [engineering-standards/README.md](engineering-standards/README.md).

---

## Implemented vs Documented-Only (v0.1)

| Category | Status | Evidence |
|----------|--------|----------|
| Constitution principles | ✅ Implemented | ATH-000, AES-0001 |
| Governance (ADR, DoD, AI workflow) | ✅ Implemented | governance/, checklists/, prompts/ |
| Repository & architecture | ✅ Implemented | ATH-003, architecture/ |
| Coding (ruff, mypy, type hints) | ✅ Implemented | `pyproject.toml`, `.pre-commit-config.yaml` |
| Testing (unit, integration, benchmark markers) | ✅ Implemented | `athena-core/pyproject.toml` pytest config |
| CI quality gates | ✅ Implemented | `.github/workflows/ci.yml` |
| Pre-commit hooks | ✅ Implemented | `.pre-commit-config.yaml` |
| Benchmark suite | ✅ Implemented | `athena-core/tests/benchmarks/` |
| Regression / property test markers | 📋 Documented-only | Deferred — add when REQ specifies |
| Section placeholder READMEs in zip | 📋 Skeleton only | Not copied; mapped to canonical paths above |
| `ATH-REL-000-Overview.docx` | 📋 Binary only | Not integrated into markdown spec |

---

## Related Documents

- [ATH-002 Engineering Standards](ATH-002-Engineering-Standards.md)
- [REFERENCES-INDEX](REFERENCES-INDEX.md)
- [REFERENCES-INTEGRATION-COMPLETE](REFERENCES-INTEGRATION-COMPLETE.md)
