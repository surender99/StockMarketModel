"""Production AthenaRuntime assembly."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from athena_os.runtime import AthenaRuntime
from athena_platform.config import PlatformConfig
from athena_platform.features import PlatformFeatures
from athena_platform.wiring import PlatformWiring, wire_platform


@dataclass
class ProductionRuntime:
    """Full production runtime: infrastructure + wired domain engines."""

    os_runtime: AthenaRuntime
    wiring: PlatformWiring
    features: PlatformFeatures = field(default_factory=PlatformFeatures)
    config: PlatformConfig = field(default_factory=PlatformConfig)

    @property
    def container(self):
        return self.wiring.container

    @property
    def event_bus(self):
        return self.os_runtime.event_bus


def assemble_runtime(
    *,
    config_path: Path | None = None,
    json_logs: bool = False,
    features: PlatformFeatures | None = None,
) -> ProductionRuntime:
    """Assemble the full Athena production runtime."""
    config = PlatformConfig(config_path=config_path, json_logs=json_logs)
    os_runtime = AthenaRuntime.bootstrap(config_path=config_path, json_logs=json_logs)
    config.load_into(os_runtime.configuration)
    features = features or PlatformFeatures()
    wiring = wire_platform(os_runtime, features=features)
    return ProductionRuntime(
        os_runtime=os_runtime,
        wiring=wiring,
        features=features,
        config=config,
    )
