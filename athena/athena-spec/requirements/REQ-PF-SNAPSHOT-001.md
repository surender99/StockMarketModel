# REQ-PF-SNAPSHOT-001

**Requirement ID:** REQ-PF-SNAPSHOT-001

**Title:** Immutable Portfolio Snapshots

**Purpose:** Capture immutable point-in-time portfolio state for auditability and reproducibility.

**Acceptance Criteria:**
- [ ] `PortfolioSnapshot` is frozen/immutable
- [ ] Snapshot deep-copies portfolio state at capture time
- [ ] PortfolioManager increments version on each snapshot
- [ ] Snapshot history retrievable per portfolio

**Unit Tests:** `tests/test_portfolio_engine_framework.py`
