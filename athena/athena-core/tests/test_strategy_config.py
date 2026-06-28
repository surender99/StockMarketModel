"""Tests for strategy configuration — REQ-STRAT-CONFIG-001."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError

from athena_core.domain.strategy.config import StrategyConfig
from athena_core.infrastructure.strategy_yaml_loader import (
    StrategyLoadError,
    load_strategy_yaml,
    strategy_to_yaml,
)

EXAMPLES = Path(__file__).resolve().parents[2] / "athena-examples" / "config" / "ema_crossover.yaml"

MINIMAL = {
    "strategy": {"id": "test", "version": "1.0.0"},
    "universe": {"source": "custom", "symbols": ["AAA"]},
    "indicators": [{"id": "ema_fast", "type": "ema", "params": {"period": 9}}],
    "entry": {"rules": [{"condition": "ema_fast > 0", "side": "long"}]},
    "exit": {"rules": [{"condition": "ema_fast < 0", "reason": "x"}]},
    "position_sizing": {
        "method": "fixed_fraction",
        "params": {"fraction": 0.1, "max_positions": 5},
    },
}


def test_valid_minimal_strategy_loads() -> None:
    config = StrategyConfig.model_validate(MINIMAL)
    assert config.strategy.id == "test"
    assert config.entry.rules[0].side == "long"


def test_missing_strategy_id_fails() -> None:
    bad = dict(MINIMAL)
    bad["strategy"] = {"version": "1.0.0"}
    with pytest.raises(ValidationError):
        StrategyConfig.model_validate(bad)


def test_missing_entry_fails() -> None:
    bad = dict(MINIMAL)
    del bad["entry"]
    with pytest.raises(ValidationError):
        StrategyConfig.model_validate(bad)


def test_invalid_position_sizing_fraction() -> None:
    bad = dict(MINIMAL)
    bad["position_sizing"] = {
        "method": "fixed_fraction",
        "params": {"fraction": 1.5, "max_positions": 1},
    }
    with pytest.raises(ValidationError):
        StrategyConfig.model_validate(bad)


def test_indicator_validation_unknown_type() -> None:
    bad = dict(MINIMAL)
    bad["indicators"] = [{"id": "x", "type": "rsi", "params": {"period": 14}}]
    with pytest.raises(StrategyLoadError):
        load_strategy_yaml_from_dict(bad)


def test_config_roundtrip() -> None:
    config = StrategyConfig.model_validate(MINIMAL)
    yaml_text = strategy_to_yaml(config)
    reloaded = StrategyConfig.model_validate(yaml.safe_load(yaml_text))
    assert reloaded.model_dump() == config.model_dump()


def test_load_example_strategy() -> None:
    if not EXAMPLES.is_file():
        pytest.skip("athena-examples strategy not present")
    config = load_strategy_yaml(EXAMPLES)
    assert config.strategy.id == "ema_crossover_v1"
    assert len(config.indicators) == 2


def load_strategy_yaml_from_dict(data: dict) -> StrategyConfig:
    import tempfile

    with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False) as fh:
        yaml.safe_dump(data, fh)
        path = Path(fh.name)
    try:
        return load_strategy_yaml(path)
    finally:
        path.unlink(missing_ok=True)
