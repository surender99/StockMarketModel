"""Configuration aggregation — athena-os config + environment."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from athena_os.configuration import ConfigurationManager


@dataclass
class PlatformConfig:
    """Aggregated platform configuration."""

    config_path: Path | None = None
    json_logs: bool = False
    features_env_prefix: str = "ATHENA_FEATURE_"
    extra: dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_env(cls) -> PlatformConfig:
        config_path = os.environ.get("ATHENA_CONFIG")
        json_logs = os.environ.get("ATHENA_JSON_LOGS", "").lower() in {"1", "true", "yes"}
        return cls(
            config_path=Path(config_path) if config_path else None,
            json_logs=json_logs,
        )

    def load_into(self, manager: ConfigurationManager) -> None:
        if self.config_path is not None:
            manager.load_file(self.config_path)
