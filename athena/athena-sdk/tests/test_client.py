"""Tests for Athena SDK — REQ-SDK-001."""

from __future__ import annotations

from pathlib import Path

from athena_sdk import AthenaClient


def test_client_load_config(tmp_path: Path) -> None:
    config_path = tmp_path / "config.yaml"
    config_path.write_text("backtest:\n  initial_capital: 750000\n", encoding="utf-8")
    config = AthenaClient.load_config(config_path)
    assert config.backtest.initial_capital == 750_000


def test_client_list_profiles(tmp_path: Path) -> None:
    config_path = tmp_path / "config.yaml"
    config_path.write_text("profiles:\n  local: {}\n", encoding="utf-8")
    client = AthenaClient(config_path=config_path)
    assert client.list_profiles() == ["local"]
