"""Intelligence suite traceability — suite domains + domain archives."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
ATHENA = REPO / "athena"
SPEC = ATHENA / "athena-spec"
SUITE_ROOT = SPEC / "ATHENA" / "Intelligence-Suite"
SCRIPTS = ATHENA / "scripts"
PY = sys.executable

EXPECTED_SUITE_DOMAINS = 5
EXPECTED_AI_MODULES = 10
EXPECTED_MARKET_MODULES = 10
EXPECTED_PATTERN_MODULES = 7
EXPECTED_TRADE_MODULES = 10

SUITE_DOMAINS = [
    "01-Indicator-Intelligence",
    "02-Pattern-Intelligence",
    "03-Market-Intelligence",
    "04-Trade-Intelligence",
    "05-AI-Intelligence",
]

AI_MODULES = [
    "AI-001-Reasoning-Engine",
    "AI-002-Natural-Language",
    "AI-003-AI-Trade-Coach",
    "AI-004-Personalization",
    "AI-005-Knowledge-Engine",
    "AI-006-Agent-Framework",
    "AI-007-Recommendation-Engine",
    "AI-008-Learning-Engine",
    "AI-009-Evaluation",
    "AI-010-Roadmap",
]

MARKET_MODULES = [
    "MI-001-Market-Data-Universe",
    "MI-002-Market-Context",
    "MI-003-Liquidity-Intelligence",
    "MI-004-Stop-Loss-Intelligence",
    "MI-005-Participant-Intelligence",
    "MI-006-Market-Memory",
    "MI-007-Opportunity-Scoring",
    "MI-008-Research-Validation",
    "MI-009-AI-Reasoning",
    "MI-010-Roadmap",
]

PATTERN_MODULES = [
    "01-Pattern-Universe",
    "02-Research-Framework",
    "03-Competitor-Study",
    "04-Validation",
    "05-AI-Reasoning",
    "06-ATH-IP",
    "07-Research-Backlog",
]

TRADE_MODULES = [
    "TI-001-Trade-DNA",
    "TI-002-Entry-Intelligence",
    "TI-003-StopLoss-Intelligence",
    "TI-004-Target-Intelligence",
    "TI-005-Trade-Management",
    "TI-006-Outcome-Analytics",
    "TI-007-Behavioral-Intelligence",
    "TI-008-AI-Trade-Coach",
    "TI-009-Learning-Engine",
    "TI-010-Roadmap",
]


def _run_integration_script() -> None:
    result = subprocess.run(
        [PY, str(SCRIPTS / "integrate_intelligence_suite_references.py")],
        cwd=ATHENA,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr or result.stdout


def test_intelligence_suite_index_exists() -> None:
    index = SPEC / "INTELLIGENCE-SUITE-INDEX.md"
    complete = SPEC / "INTELLIGENCE-SUITE-COMPLETE.md"
    assert index.is_file()
    assert complete.is_file()
    text = index.read_text(encoding="utf-8")
    assert "ATH-INTELLIGENCE-SUITE(1).zip" in text
    assert "AI-Intelligence" in text
    assert "Trade-Intelligence" in text


@pytest.mark.parametrize("domain", SUITE_DOMAINS, ids=SUITE_DOMAINS)
def test_suite_domain_integrated(domain: str) -> None:
    path = SUITE_ROOT / "Suite" / domain
    assert path.is_dir(), f"suite domain missing: {domain}"
    readme = path / "README.md"
    assert readme.is_file()


@pytest.mark.parametrize("module", AI_MODULES, ids=AI_MODULES)
def test_ai_intelligence_module(module: str) -> None:
    path = SUITE_ROOT / "AI-Intelligence" / module
    assert path.is_dir(), f"AI module missing: {module}"
    assert (path / "Overview.md").is_file()


@pytest.mark.parametrize("module", MARKET_MODULES, ids=MARKET_MODULES)
def test_market_intelligence_module(module: str) -> None:
    path = SUITE_ROOT / "Market-Intelligence" / module
    assert path.is_dir(), f"market module missing: {module}"
    assert (path / "Overview.md").is_file()


@pytest.mark.parametrize("module", PATTERN_MODULES, ids=PATTERN_MODULES)
def test_pattern_intelligence_module(module: str) -> None:
    path = SUITE_ROOT / "Pattern-Intelligence" / module
    assert path.is_dir(), f"pattern module missing: {module}"
    assert (path / "Overview.md").is_file()


@pytest.mark.parametrize("module", TRADE_MODULES, ids=TRADE_MODULES)
def test_trade_intelligence_module(module: str) -> None:
    path = SUITE_ROOT / "Trade-Intelligence" / module
    assert path.is_dir(), f"trade module missing: {module}"
    assert (path / "Overview.md").is_file()


def test_suite_domain_count() -> None:
    domains = [p for p in (SUITE_ROOT / "Suite").iterdir() if p.is_dir()]
    assert len(domains) == EXPECTED_SUITE_DOMAINS


def test_domain_module_counts() -> None:
    assert len(list((SUITE_ROOT / "AI-Intelligence").iterdir())) >= EXPECTED_AI_MODULES
    assert len(list((SUITE_ROOT / "Market-Intelligence").iterdir())) >= EXPECTED_MARKET_MODULES
    assert len(list((SUITE_ROOT / "Pattern-Intelligence").iterdir())) >= EXPECTED_PATTERN_MODULES
    assert len(list((SUITE_ROOT / "Trade-Intelligence").iterdir())) >= EXPECTED_TRADE_MODULES


def test_intelligence_suite_readme_present() -> None:
    readme = SUITE_ROOT / "README.md"
    assert readme.is_file()
    assert "Intelligence Suite" in readme.read_text(encoding="utf-8")


def test_integration_script_idempotent() -> None:
    _run_integration_script()
    test_suite_domain_count()
