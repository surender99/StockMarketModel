"""Security framework tests — ATH-REL-017."""

from __future__ import annotations

from athena_core.application.security_manager import SecurityManager
from athena_core.domain.security import Role


def test_req_sec_auth_001_authentication() -> None:
    """REQ-SEC-AUTH-001 — authentication."""
    mgr = SecurityManager()
    mgr.auth.register("alice", "secret", Role.RESEARCHER)
    assert mgr.login("alice", "secret")
    assert not mgr.login("alice", "wrong")


def test_req_sec_rbac_001_authorization() -> None:
    """REQ-SEC-RBAC-001 — RBAC."""
    mgr = SecurityManager()
    mgr.auth.register("bob", "pass", Role.VIEWER)
    assert mgr.check_permission("bob", "read")
    assert not mgr.check_permission("bob", "write")


def test_req_sec_secrets_001_vault() -> None:
    """REQ-SEC-SECRETS-001 — secrets management."""
    mgr = SecurityManager()
    mgr.vault.store("api_key", "abc123")
    assert mgr.vault.retrieve("api_key") == "abc123"


def test_req_sec_audit_001_trail() -> None:
    """REQ-SEC-AUDIT-001 — audit trails."""
    mgr = SecurityManager()
    mgr.auth.register("carol", "pass")
    mgr.login("carol", "pass")
    assert len(mgr.audit.events()) >= 1
