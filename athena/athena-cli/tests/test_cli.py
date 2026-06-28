"""Tests for polished Athena CLI — REQ-CLI-001."""

from __future__ import annotations

from athena_cli.main import build_parser, main


def test_parser_includes_all_commands() -> None:
    parser = build_parser()
    commands = {
        action.dest: action.choices for action in parser._actions if action.dest == "command"
    }
    assert "command" in commands
    assert set(commands["command"]) >= {
        "health",
        "profiles",
        "ingest",
        "backtest",
        "scan",
        "walk-forward",
        "optimize",
        "compare-experiments",
        "research",
    }


def test_health_command() -> None:
    assert main(["health"]) == 0


def test_profiles_without_config() -> None:
    assert main(["profiles"]) == 0


def test_research_dry_run() -> None:
    assert main(["research", "Find the best EMA strategy for sideways markets", "--dry-run"]) == 0
