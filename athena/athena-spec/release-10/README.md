# ATH-REL-010 Research Engine — Section Index

> **Release package:** [ATH-REL-010-Research-Engine.md](../ATH-REL-010-Research-Engine.md)  
> **Source doc:** `References/REL-010 TO REL- 020.docx` (REL-010 section)

This index maps the ATH-REL-010 Release-10 module taxonomy to canonical specs and `athena-core` modules.

---

## Section Map

| Section | Doc Status (v0.1) | Canonical Spec | Code / Tooling |
|---------|-------------------|----------------|----------------|
| **00 Executive Summary** | From docx §1 | [ATH-REL-010](../ATH-REL-010-Research-Engine.md) | — |
| **01 Research Workspace** | From docx §5.1 | [REQ-RS-WORKSPACE-001](../requirements/REQ-RS-WORKSPACE-001.md) | `application/research_manager.py` |
| **02 Experiment Manager** | From docx §5.2 | [REQ-RS-EXPERIMENT-001](../requirements/REQ-RS-EXPERIMENT-001.md) | `domain/research/lifecycle.py` |
| **03 Dataset Manager** | From docx §5.3 | [REQ-RS-DATASET-001](../requirements/REQ-RS-DATASET-001.md) | `domain/research/dataset.py` |
| **04 Research Pipeline** | From docx §5.4 | [REQ-RS-PIPELINE-001](../requirements/REQ-RS-PIPELINE-001.md) | `application/research_pipeline.py` |
| **05 Result Repository** | From docx §5.5 | [REQ-RS-RESULTS-001](../requirements/REQ-RS-RESULTS-001.md) | `application/result_repository.py` |
| **06 Knowledge Base** | From docx §5.6 | — | `domain/research/knowledge.py` |
| **07 Testing** | From docx §9 | [ATH-002](../ATH-002-Engineering-Standards.md) | `tests/test_research_engine_framework.py` |
| **08 Benchmarks** | From docx §10 | [athena-core/benchmarks/](../../athena-core/benchmarks/README.md) | `tests/benchmarks/` |
| **09 AI Coding** | From docx §11 | [AES-0006](../governance/AES-0006-AI-Coding-Standards.md) | — |
| **10 Agent Packages** | From docx §8 | [prompts/](../prompts/) | — |
| **11 Playbooks** | — | [athena-docs/handbook/](../../athena-docs/handbook/) | — |

---

## REQ Traceability (Release-10)

| REQ ID | Section | Module |
|--------|---------|--------|
| REQ-RS-WORKSPACE-001 | 01 Research Workspace | `application/research_manager.py` |
| REQ-RS-EXPERIMENT-001 | 02 Experiment Manager | `domain/research/lifecycle.py` |
| REQ-RS-DATASET-001 | 03 Dataset Manager | `domain/research/dataset.py` |
| REQ-RS-PIPELINE-001 | 04 Research Pipeline | `application/research_pipeline.py` |
| REQ-RS-RESULTS-001 | 05 Result Repository | `application/result_repository.py` |
| FR-001 | 01 Research Workspace | `application/research_manager.py` |
| FR-014 | 03 Dataset Manager | `domain/research/dataset.py` |
| FR-015 | 04 Research Pipeline | `domain/research/research_plugins.py` |
