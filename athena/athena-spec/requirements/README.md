# Requirements Layout

Athena uses an **intentional hybrid model** for requirement documents. See [DEC-003](../decision-log/DEC-003-hybrid-requirements-layout.md).

---

## Two locations

### 1. Flat top-level (`requirements/`)

Cross-cutting and **MVP phase REQs** that span packages or define platform deliverables:

- Data ingest, feature store, calendar
- Backtest engine, experiment tracking
- CLI, SDK, dashboard, AI assistant
- Scanner, optimizer, ML scorer, explainability

**When to add here:** New work tied to a MVP phase or multiple domains.

### 2. Per-package (`<domain>/requirements/`)

Domain REQs co-located with AES specs and contracts:

| Folder | Examples |
|--------|----------|
| `feature-engineering/requirements/` | REQ-IND-MACD-001, REQ-IND-RSI-001 |
| `portfolio-engine/requirements/` | REQ-PF-001 … REQ-PF-003 |
| `statistics/requirements/` | REQ-STAT-001 … REQ-STAT-003 |
| `pattern-recognition/requirements/` | REQ-PAT-001 … REQ-PAT-003 |

**When to add here:** New REQ belongs to a single References package / AES domain.

---

## Rules

1. **Globally unique REQ IDs** — prefix by domain (`REQ-DATA-*`, `REQ-PF-*`, etc.).
2. **Do not mass-move** files between flat and package folders without an ADR/DEC update.
3. **Link both ways** — PLATFORM-COMPLETE and package validation reports should reference the canonical REQ path.
4. **Standard format** — follow [ATH-004 Requirement Standard](../ATH-004-Requirement-Standard.md).

---

## Traceability

| Status doc | Scope |
|------------|-------|
| [PLATFORM-COMPLETE.md](../PLATFORM-COMPLETE.md) | Implemented MVP REQs (code) |
| [SPEC-VS-CODE-STATUS.md](../SPEC-VS-CODE-STATUS.md) | Spec vs code gaps by package |
