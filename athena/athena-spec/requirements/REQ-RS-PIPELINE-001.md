# REQ-RS-PIPELINE-001

**Requirement ID:** REQ-RS-PIPELINE-001

**Title:** Research Pipeline Execution

**Purpose:** Execute ordered research pipeline stages (feature generation, indicators, strategy evaluation, result storage).

**Acceptance Criteria:**
- [ ] Default pipeline runs four stages in order
- [ ] Custom stage handlers can be injected
- [ ] Pipeline advances experiment lifecycle on completion
- [ ] Stage failures mark experiment as rejected

**Unit Tests:** `tests/test_research_engine_framework.py`
