"""Production framework tests — ATH-REL-015."""

from __future__ import annotations

from athena_core.application.production_manager import ProductionManager
from athena_core.domain.production import GatewayConfig, HealthStatus, OrderRequest


def test_req_prod_gateway_001() -> None:
    """REQ-PROD-GATEWAY-001 — broker gateway."""
    mgr = ProductionManager(GatewayConfig("ibkr", "tcp://localhost"))
    status = mgr.startup()
    assert status == HealthStatus.HEALTHY


def test_req_prod_oms_001() -> None:
    """REQ-PROD-OMS-001 — OMS."""
    mgr = ProductionManager()
    mgr.startup()
    result = mgr.submit_order(OrderRequest("AAPL", "buy", 10), 150.0)
    assert result["status"] == "accepted"
    assert len(mgr.oms.list_orders()) == 1


def test_req_prod_rms_001() -> None:
    """REQ-PROD-RMS-001 — RMS."""
    mgr = ProductionManager()
    mgr.rms.max_notional = 100.0
    mgr.startup()
    result = mgr.submit_order(OrderRequest("AAPL", "buy", 10), 150.0)
    assert result["status"] == "rejected"


def test_req_prod_health_001() -> None:
    """REQ-PROD-HEALTH-001 — health checks."""
    mgr = ProductionManager()
    assert mgr.startup() == HealthStatus.HEALTHY


def test_req_prod_audit_001() -> None:
    """REQ-PROD-AUDIT-001 — audit logging."""
    mgr = ProductionManager()
    mgr.startup()
    mgr.submit_order(OrderRequest("X", "buy", 1), 10.0)
    assert len(mgr.audit.trail()) >= 2
