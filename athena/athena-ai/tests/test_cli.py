"""Tests for athena-ai CLI — REQ-AI-ASSISTANT-001."""

from __future__ import annotations

from athena_ai.interfaces.cli import build_parser, main


def test_parser_requires_query_or_help() -> None:
    parser = build_parser()
    args = parser.parse_args([])
    assert args.query is None


def test_dry_run_research() -> None:
    assert main(["Find the best EMA strategy for sideways markets", "--dry-run"]) == 0


def test_no_query_prints_help() -> None:
    assert main([]) == 0
