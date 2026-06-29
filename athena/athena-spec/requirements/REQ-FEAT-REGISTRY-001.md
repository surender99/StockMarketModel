# REQ-FEAT-REGISTRY-001

**Requirement ID:** REQ-FEAT-REGISTRY-001

**Title:** Indicator Feature Registry

**Purpose:** Register all built-in indicators as AES-0202 plugins resolved at runtime via `PluginRegistry`.

**Description:** `register_builtin_indicators()` discovers EMA, SMA, MACD, RSI, STOCH, ATR, ADX, Bollinger, and pattern plugins. `FeatureService` resolves indicators through `resolve_indicator()` instead of a hardcoded dict.

**Acceptance Criteria:**
- [ ] All catalog indicators registered with `PluginType.INDICATOR`
- [ ] `FeatureService` requires `PluginRegistry` for computation
- [ ] Bootstrap wires registry at composition root

**Unit Tests:** `tests/test_feature_engineering_framework.py`
