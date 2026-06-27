"""CLI entrypoint for athena-ai — REQ-AI-ASSISTANT-001."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from athena_core.infrastructure.logging import configure_logging, get_logger

from athena_ai import __version__
from athena_ai.application.research_assistant import ResearchAssistant


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="athena-ai",
        description="Athena AI research assistant — natural-language experiment orchestration",
    )
    parser.add_argument("--version", action="version", version=f"athena-ai {__version__}")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable debug logging")
    parser.add_argument(
        "query",
        nargs="?",
        help='Natural-language research query, e.g. "Find the best EMA strategy for sideways markets"',
    )
    parser.add_argument("--config", type=Path, help="Athena YAML config path")
    parser.add_argument("--ai-config", type=Path, help="Research assistant YAML config path")
    parser.add_argument("--profile", help="Named Athena config profile")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Propose plan only; do not execute backtests",
    )
    parser.add_argument(
        "--propose",
        action="store_true",
        help="Alias for --dry-run",
    )
    parser.add_argument("--output", type=Path, help="Write JSON result to path")
    parser.add_argument(
        "--no-openai",
        action="store_true",
        help="Force rule-based intent parser even if OPENAI_API_KEY is set",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    configure_logging(level=10 if args.verbose else 20)
    log = get_logger("athena_ai.cli")

    if not args.query:
        parser.print_help()
        return 0

    dry_run = args.dry_run or args.propose
    assistant = ResearchAssistant(
        config_path=args.ai_config,
        athena_config_path=args.config,
        profile=args.profile,
    )
    result = assistant.research(
        args.query,
        dry_run=dry_run,
        use_openai=False if args.no_openai else None,
    )
    payload = assistant.to_dict(result)
    text = json.dumps(payload, indent=2)
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text)

    log.info(
        "research.complete",
        session_id=result.session_id,
        dry_run=dry_run,
        recommendations=len(result.recommendations),
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
