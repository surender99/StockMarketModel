"""Research master roadmap traceability — WS-01 … WS-08."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
ATHENA = REPO / "athena"
SPEC = ATHENA / "athena-spec"
ROADMAP_ROOT = SPEC / "ATHENA" / "Research-Master-Roadmap"
SCRIPTS = ATHENA / "scripts"
PY = sys.executable

EXPECTED_WORKSTREAMS = 8
ARTIFACTS = ("01-Tasks.md", "02-Research-Template.md", "03-Sources.md", "04-Outputs.md")


def _run_integration_script() -> None:
    result = subprocess.run(
        [PY, str(SCRIPTS / "integrate_research_master_roadmap_references.py")],
        cwd=ATHENA,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr or result.stdout


def test_research_master_roadmap_index_exists() -> None:
    index = SPEC / "RESEARCH-MASTER-ROADMAP-INDEX.md"
    complete = SPEC / "RESEARCH-MASTER-ROADMAP-COMPLETE.md"
    assert index.is_file()
    assert complete.is_file()
    text = index.read_text(encoding="utf-8")
    assert "ATH-RESEARCH-MASTER-ROADMAP.zip" in text
    assert "WS-01" in text
    assert "WS-08" in text


@pytest.mark.parametrize(
    "ws_num",
    list(range(1, 9)),
    ids=[f"WS-{n:02d}" for n in range(1, 9)],
)
def test_workstream_spec_integrated(ws_num: int) -> None:
    matches = list(ROADMAP_ROOT.glob(f"WS-{ws_num:02d}-*"))
    assert matches, f"workstream spec missing for WS-{ws_num:02d}"
    tasks = matches[0] / "01-Tasks.md"
    assert tasks.is_file()


@pytest.mark.parametrize("artifact", ARTIFACTS)
def test_workstream_artifacts_present(artifact: str) -> None:
    ws_dirs = [p for p in ROADMAP_ROOT.iterdir() if p.is_dir() and p.name.startswith("WS-")]
    assert len(ws_dirs) == EXPECTED_WORKSTREAMS
    for ws_dir in ws_dirs:
        md = ws_dir / artifact
        assert md.is_file(), f"{ws_dir.name} missing {artifact}"


def test_workstream_count() -> None:
    workstreams = [p for p in ROADMAP_ROOT.iterdir() if p.is_dir() and p.name.startswith("WS-")]
    assert len(workstreams) == EXPECTED_WORKSTREAMS


def test_roadmap_readme_present() -> None:
    readme = ROADMAP_ROOT / "README.md"
    assert readme.is_file()
    assert "Research" in readme.read_text(encoding="utf-8")


def test_integration_script_idempotent() -> None:
    _run_integration_script()
    test_workstream_count()
