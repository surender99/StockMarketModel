"""Research assistant configuration — REQ-AI-ASSISTANT-001."""

from __future__ import annotations

import os
from datetime import date
from pathlib import Path

import yaml
from pydantic import BaseModel, Field


class ResearchAssistantConfig(BaseModel):
    """YAML-driven settings for the AI research assistant."""

    athena_config_path: str | None = None
    default_strategy_path: str = "../athena-examples/config/ema_crossover.yaml"
    strategy_paths: dict[str, str] = Field(
        default_factory=lambda: {
            "ema": "../athena-examples/config/ema_crossover.yaml",
            "sma": "../athena-examples/config/ema_crossover.yaml",
            "crossover": "../athena-examples/config/ema_crossover.yaml",
        }
    )
    default_start: date = date(2022, 1, 1)
    default_end: date = date(2024, 6, 1)
    default_compare_latest: int = 3
    full_research_include_optimize: bool = False
    ai_session_log_path: str = "./experiments/ai_sessions"
    use_openai_when_available: bool = True
    openai_model: str = "gpt-4o-mini"


def load_research_config(path: Path | str | None = None) -> ResearchAssistantConfig:
    """Load assistant config from YAML or return defaults."""
    if path is None:
        env_path = os.environ.get("ATHENA_AI_CONFIG")
        if env_path:
            path = Path(env_path)
        else:
            bundled = Path(__file__).resolve().parents[2] / "config" / "research_assistant.yaml"
            path = bundled if bundled.is_file() else None
    if path is None:
        return ResearchAssistantConfig()
    config_path = Path(path)
    raw = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    research = raw.get("research_assistant", raw)
    return ResearchAssistantConfig.model_validate(research)
