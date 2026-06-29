# REQ-PAT-REGISTRY-001

**Requirement ID:** REQ-PAT-REGISTRY-001

**Title:** Pattern Provider Plugin Registry

**Purpose:** Register pattern detectors as AES-0202 PatternProvider plugins in PluginRegistry, mirroring the indicator registry pattern from REL-003.

**Acceptance Criteria:**
- [ ] `register_builtin_patterns` registers all built-in pattern detectors
- [ ] `resolve_pattern` returns execute callable for active pattern plugins
- [ ] Patterns wired at bootstrap alongside indicators
- [ ] Pattern features available via feature pipeline (`pattern` indicator plugin)

**Unit Tests:** `tests/test_pattern_recognition_framework.py`
