"""Security manager — ATH-REL-017."""

from __future__ import annotations

from athena_core.domain.security import (
    Authenticator,
    ComplianceChecker,
    RBACAuthorizer,
    Role,
    SecretsVault,
    SecurityAuditTrail,
)


class SecurityManager:
    """Orchestrate security and compliance workflows."""

    def __init__(self) -> None:
        self.auth = Authenticator()
        self.rbac = RBACAuthorizer()
        self.vault = SecretsVault()
        self.compliance = ComplianceChecker()
        self.audit = SecurityAuditTrail()

    def login(self, username: str, password: str) -> bool:
        user = self.auth.authenticate(username, password)
        if user:
            self.audit.record("login", user.user_id, "auth")
            return True
        return False

    def check_permission(self, username: str, permission: str) -> bool:
        user = self.auth._users.get(username)
        if user is None:
            return False
        return self.rbac.authorize(user, permission)
