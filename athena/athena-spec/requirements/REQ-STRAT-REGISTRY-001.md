# REQ-STRAT-REGISTRY-001

**Requirement ID:** REQ-STRAT-REGISTRY-001

**Title:** Strategy Provider Plugin Registry

**Purpose:** Register strategy templates as AES-0202 StrategyProvider plugins in PluginRegistry, mirroring the pattern and indicator registry patterns from REL-005 and REL-003.

**Acceptance Criteria:**
- [ ] `register_builtin_strategies` registers all built-in strategy templates
- [ ] `resolve_strategy` returns StrategyConfig for active strategy plugins
- [ ] Strategies wired at bootstrap alongside indicators and patterns
- [ ] StrategyEngine loads strategies by id from registry

**Unit Tests:** `tests/test_strategy_engine_framework.py`
