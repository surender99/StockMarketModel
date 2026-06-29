# REQ-RS-EXPERIMENT-001

**Requirement ID:** REQ-RS-EXPERIMENT-001

**Title:** Experiment Lifecycle Management

**Purpose:** Manage experiment states through Draft → Running → Completed/Validated/Rejected → Archived.

**Acceptance Criteria:**
- [ ] Valid lifecycle transitions enforced
- [ ] Invalid transitions raise ValueError
- [ ] Experiments created within projects with metadata

**Unit Tests:** `tests/test_research_engine_framework.py`
