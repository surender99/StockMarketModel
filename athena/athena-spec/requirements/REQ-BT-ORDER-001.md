# REQ-BT-ORDER-001

**Requirement ID:** REQ-BT-ORDER-001

**Title:** Order Engine and State Machine

**Purpose:** Model buy/sell/stop/limit order types with a validated lifecycle state machine for backtest simulation.

**Acceptance Criteria:**
- [ ] `OrderType` supports market, limit, stop, stop_limit
- [ ] `OrderStatus` state machine enforces valid transitions
- [ ] `validate_order` checks required fields per order type
- [ ] Orders integrate with backtest entry/exit simulation

**Unit Tests:** `tests/test_backtest_engine_framework.py`
