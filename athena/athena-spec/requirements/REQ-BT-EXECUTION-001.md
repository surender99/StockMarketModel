# REQ-BT-EXECUTION-001

**Requirement ID:** REQ-BT-EXECUTION-001

**Title:** Backtest Execution Models

**Purpose:** Support configurable fill policies for simulated order execution, avoiding look-ahead bias while modeling realistic bar-level fills.

**Acceptance Criteria:**
- [ ] `FillModel` enum defines current_bar_close and next_bar_open policies
- [ ] `resolve_fill_price` returns correct price for each model
- [ ] BacktestEngine honors `execution_model` config setting
- [ ] next_bar_open defers entry to following session open
- [ ] Fill models registered via `register_builtin_backtest_plugins`

**Unit Tests:** `tests/test_backtest_engine_framework.py`
