"""Product phase requirements traceability — PR-01 … PR-10."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
ATHENA = REPO / "athena"
SPEC = ATHENA / "athena-spec"
PHASE_ROOT = SPEC / "ATHENA" / "Phase-Requirements"
SCRIPTS = ATHENA / "scripts"
PY = sys.executable

EXPECTED_PHASES = 10
SECTIONS = ("requirements", "deliverables", "acceptance", "roadmap", "risks")


def _run_integration_script() -> None:
    result = subprocess.run(
        [PY, str(SCRIPTS / "integrate_phase_requirements_references.py")],
        cwd=ATHENA,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr or result.stdout


def test_phase_requirements_index_exists() -> None:
    index = SPEC / "PHASE-REQUIREMENTS-INDEX.md"
    complete = SPEC / "PHASE-REQUIREMENTS-COMPLETE.md"
    assert index.is_file()
    assert complete.is_file()
    text = index.read_text(encoding="utf-8")
    assert "ATH-PHASE-REQUIREMENTS.zip" in text
    assert "PR-01" in text
    assert "PR-10" in text


@pytest.mark.parametrize(
    "phase_num",
    list(range(1, 11)),
    ids=[f"PR-{n:02d}" for n in range(1, 11)],
)
def test_phase_spec_integrated(phase_num: int) -> None:
    matches = list(PHASE_ROOT.glob(f"PHASE-{phase_num:02d}-*"))
    assert matches, f"phase spec missing for PR-{phase_num:02d}"
    overview = matches[0] / "00-Overview.md"
    assert overview.is_file()


@pytest.mark.parametrize("section", SECTIONS)
def test_phase_sections_present(section: str) -> None:
    phase_dirs = [p for p in PHASE_ROOT.iterdir() if p.is_dir() and p.name.startswith("PHASE-")]
    assert len(phase_dirs) == EXPECTED_PHASES
    for phase_dir in phase_dirs:
        section_dir = phase_dir / section
        assert section_dir.is_dir(), f"{phase_dir.name} missing {section}/"
        assert any(section_dir.glob("*.md"))


def test_phase_count() -> None:
    phases = [p for p in PHASE_ROOT.iterdir() if p.is_dir() and p.name.startswith("PHASE-")]
    assert len(phases) == EXPECTED_PHASES


def test_integration_script_idempotent() -> None:
    _run_integration_script()
    test_phase_count()
