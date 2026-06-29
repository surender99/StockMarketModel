"""Production manager — ATH-REL-015, FR-012."""

from __future__ import annotations

from athena_core.domain.production import (
    AuditLogger,
    BrokerGateway,
    GatewayConfig,
    HealthChecker,
    HealthStatus,
    OrderManagementSystem,
    OrderRequest,
    RiskManagementSystem,
)


class ProductionManager:
    """Orchestrate production deployment workflows."""

    def __init__(self, gateway_config: GatewayConfig | None = None) -> None:
        self.gateway = BrokerGateway(gateway_config or GatewayConfig("paper", "local://"))
        self.oms = OrderManagementSystem()
        self.rms = RiskManagementSystem()
        self.health = HealthChecker()
        self.audit = AuditLogger()

    def startup(self) -> HealthStatus:
        connected = self.gateway.connect()
        self.audit.log("startup", "system", connected=connected)
        return self.health.check({"gateway": connected})

    def submit_order(self, order: OrderRequest, price: float) -> dict:
        ok, reason = self.rms.check(order, price)
        if not ok:
            self.audit.log("order_rejected", "rms", reason=reason)
            return {"status": "rejected", "reason": reason}
        result = self.oms.route(order, self.gateway)
        self.audit.log("order_submitted", "oms", result=result)
        return result
