"""Tests for config profile loading — REQ-CLI-001."""

from __future__ import annotations

from pathlib import Path

import pytest

from athena_core.application.config_loader import list_profile_names, load_athena_config


def test_load_config_without_profile(tmp_path: Path) -> None:
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "backtest:\n  initial_capital: 1000000\nfeature_store:\n  data_version: v1\n",
        encoding="utf-8",
    )
    config = load_athena_config(config_path)
    assert config.backtest.initial_capital == 1_000_000
    assert config.feature_store.data_version == "v1"


def test_profile_overlay_merges_nested_keys(tmp_path: Path) -> None:
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        """
backtest:
  initial_capital: 1000000
feature_store:
  data_version: v1
profiles:
  paper:
    backtest:
      initial_capital: 500000
    feature_store:
      data_version: paper-v1
""".strip(),
        encoding="utf-8",
    )
    config = load_athena_config(config_path, profile="paper")
    assert config.backtest.initial_capital == 500_000
    assert config.feature_store.data_version == "paper-v1"


def test_unknown_profile_raises(tmp_path: Path) -> None:
    config_path = tmp_path / "config.yaml"
    config_path.write_text("profiles:\n  dev: {}\n", encoding="utf-8")
    with pytest.raises(ValueError, match="unknown config profile"):
        load_athena_config(config_path, profile="missing")


def test_list_profile_names(tmp_path: Path) -> None:
    config_path = tmp_path / "config.yaml"
    config_path.write_text("profiles:\n  dev: {}\n  prod: {}\n", encoding="utf-8")
    assert list_profile_names(config_path) == ["dev", "prod"]
