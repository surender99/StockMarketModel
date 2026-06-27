# ATH-004 – Requirement Standard

Every requirement follows:

```
Requirement ID:
Title:
Purpose:
Description:
Inputs:
Outputs:
Configuration:
Algorithm:
Dependencies:
Acceptance Criteria:
Performance Target:
Unit Tests:
Integration Tests:
Future Enhancements:
```

## Example (abbreviated)

**REQ-IND-EMA-001** — see [requirements/REQ-IND-EMA-001.md](requirements/REQ-IND-EMA-001.md) for the full specification.

Acceptance:
- Matches pandas-ta
- Supports configurable periods
- Vectorized implementation

## REQ Naming Convention

| Prefix | Domain |
|--------|--------|
| `REQ-DATA-*` | Data ingestion, storage, calendar |
| `REQ-IND-*` | Technical indicators |
| `REQ-FEAT-*` | Feature store |
| `REQ-STRAT-*` | Strategy configuration |
| `REQ-BT-*` | Backtesting |
| `REQ-EXP-*` | Experiment tracking |
| `REQ-PORT-*` | Portfolio (future) |
| `REQ-ML-*` | Machine learning (future) |

All REQ documents live in [requirements/](requirements/).

**New requirements:** copy [templates/Requirement-Template.md](templates/Requirement-Template.md).
