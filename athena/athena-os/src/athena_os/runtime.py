"""Shared runtime composition root — ATH-REL-001."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from athena_os.configuration import ConfigurationManager
from athena_os.event_bus import EventBus
from athena_os.logging import configure_logging
from athena_os.metrics import MetricsCollector
from athena_os.messaging import MessageBroker
from athena_os.plugins import PluginRegistry
from athena_os.registry import Registry
from athena_os.scheduler import Scheduler
from athena_os.security import Authenticator, RBACAuthorizer, SecretsVault, SecurityAuditTrail
from athena_os.workflow import WorkflowEngine


@dataclass
class AthenaRuntime:
    """Wired infrastructure services shared across Athena packages."""

    event_bus: EventBus = field(default_factory=EventBus)
    plugin_registry: PluginRegistry = field(default_factory=PluginRegistry)
    configuration: ConfigurationManager = field(default_factory=ConfigurationManager)
    workflow_engine: WorkflowEngine = field(default_factory=WorkflowEngine)
    scheduler: Scheduler = field(default_factory=Scheduler)
    metrics: MetricsCollector = field(default_factory=MetricsCollector)
    messaging: MessageBroker = field(default_factory=MessageBroker)
    service_registry: Registry[object] = field(default_factory=Registry)
    authenticator: Authenticator = field(default_factory=Authenticator)
    authorizer: RBACAuthorizer = field(default_factory=RBACAuthorizer)
    secrets: SecretsVault = field(default_factory=SecretsVault)
    audit_trail: SecurityAuditTrail = field(default_factory=SecurityAuditTrail)

    @classmethod
    def bootstrap(
        cls,
        *,
        config_path: Path | None = None,
        json_logs: bool = False,
    ) -> AthenaRuntime:
        runtime = cls()
        configure_logging(json_logs=json_logs)
        if config_path is not None:
            runtime.configuration.load_file(config_path)
        return runtime
