# ATH-REL-010 – Research Engine (Release-10)

> **Version:** v0.1  
> **Source:** `References/REL-010 TO REL- 020.docx` (REL-010 section)  
> **Status:** Spec-integrated (skeleton release package)  
> **Validation:** [packages/PACKAGE-REL-010-COMPLETE.md](packages/PACKAGE-REL-010-COMPLETE.md)

ATH-REL-010 is the **research engine release package** for Athena Release-10. It extends Package 10 research engine with a reproducible research workspace, experiment lifecycle management, dataset snapshots, research pipelines, result repositories, and a knowledge base.

---

## Purpose

| Aspect | Detail |
|--------|--------|
| **What** | Research workspace, experiment manager, dataset manager, pipeline, results, knowledge base |
| **When** | After REL-009 statistics and analytics engine |
| **Who** | `athena-core` developers, quant researchers, AI coding agents |

Release-10 v0.1 ships as a **skeleton**: the Word document defines module taxonomy; canonical content lives in ATH/AES documents, REQ files, and `athena-core` modules cross-linked from [release-10/](release-10/README.md).

---

## Relationship to Prior Releases

| ID | Role | Canonical Path |
|----|------|----------------|
| **ATH-REL-009** | Statistics & analytics | [ATH-REL-009-Statistics-and-Analytics-Engine.md](ATH-REL-009-Statistics-and-Analytics-Engine.md) |
| **Package 10** | Research AES specs | [research-engine/](research-engine/) |
| **AES-1000** | Research engine framework | [AES-1000](research-engine/framework/AES-1000-Research-Engine.md) |
| **AES-1001** | Experiment lifecycle | [AES-1001](research-engine/framework/AES-1001-Experiment-Lifecycle.md) |

**Reading order:** ATH-REL-009 → Package 10 → ATH-REL-010 (this index) → REQ-RS-*.

---

## Release Package Sections (v0.1)

| # | Section | Doc Module | Canonical Spec / Code |
|---|---------|------------|------------------------|
| 00 | Executive Summary | §1 | This document |
| 01 | Research Workspace | §5.1 | `application/research_manager.py`, REQ-RS-WORKSPACE-001 |
| 02 | Experiment Manager | §5.2 | `domain/research/lifecycle.py`, REQ-RS-EXPERIMENT-001 |
| 03 | Dataset Manager | §5.3 | `domain/research/dataset.py`, REQ-RS-DATASET-001 |
| 04 | Research Pipeline | §5.4 | `application/research_pipeline.py`, REQ-RS-PIPELINE-001 |
| 05 | Result Repository | §5.5 | `application/result_repository.py`, REQ-RS-RESULTS-001 |
| 06 | Knowledge Base | §5.6 | `domain/research/knowledge.py` |
| 07 | Testing | §9 | `tests/test_research_engine_framework.py` |
| 08 | Benchmarks | §10 | [athena-core/benchmarks/](../athena-core/benchmarks/README.md) |
| 09 | AI Coding | §11 | [AES-0006](governance/AES-0006-AI-Coding-Standards.md) |
| 10 | Agent Packages | §8 | [prompts/](prompts/) |
| 11 | Playbooks | — | [athena-docs/handbook/](../athena-docs/handbook/) |

Full section index: [release-10/README.md](release-10/README.md).

---

## Functional Requirements (FR-001–FR-015)

| ID | Requirement | v0.1 Status |
|----|-------------|-------------|
| FR-001 | Research workspace projects | ✅ ResearchManager.create_project |
| FR-002 | Experiment creation with metadata | ✅ ExperimentSpec |
| FR-003 | Experiment lifecycle management | ✅ ExperimentState transitions |
| FR-004 | Dataset snapshots | ✅ DatasetSnapshot.capture |
| FR-005 | Dataset comparison | ✅ compare_snapshots |
| FR-006 | Research pipeline execution | ✅ ResearchPipeline |
| FR-007 | Experiment history | ✅ ResultRepository.history |
| FR-008 | Experiment ranking | ✅ ResultRepository.rank |
| FR-009 | Result comparison | ✅ ResultRepository.compare |
| FR-010 | Dataset lineage | ✅ DatasetSnapshot.lineage |
| FR-011 | Knowledge base entries | ✅ KnowledgeEntry |
| FR-012 | Reusable research APIs | ✅ ResearchManager |
| FR-013 | Experiment versioning | ✅ ExperimentSpec.version |
| FR-014 | Reproducible datasets | ✅ reproducibility_hash |
| FR-015 | Plugin-based pipeline stages | ✅ research_plugins |

---

## Implemented vs Documented-Only (v0.1)

| Category | Status | Evidence |
|----------|--------|----------|
| ResearchManager / ResearchPipeline | ✅ Implemented | `application/research_manager.py`, `research_pipeline.py` |
| Experiment lifecycle | ✅ Implemented | `domain/research/lifecycle.py` |
| Dataset snapshots + comparison | ✅ Implemented | `domain/research/dataset.py` |
| Result repository + ranking | ✅ Implemented | `application/result_repository.py` |
| Knowledge base | ✅ Implemented | `domain/research/knowledge.py` |
| Research notebooks, templates UI | 📋 Documented-only | Deferred |
| Full pipeline backtest integration | 📋 Documented-only | Deferred |

---

## Related Documents

- [release-10/README.md](release-10/README.md) — section index
- [research-engine/](research-engine/) — Package 10 AES specs
- [ATH-REL-009-Statistics-and-Analytics-Engine.md](ATH-REL-009-Statistics-and-Analytics-Engine.md) — prior release
