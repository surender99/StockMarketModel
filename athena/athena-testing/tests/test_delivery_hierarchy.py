"""Delivery hierarchy traceability smoke tests — Epics, Features, IPs, Stories, Tasks."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
ATHENA = REPO / "athena"
SPEC = ATHENA / "athena-spec"
SCRIPTS = ATHENA / "scripts"
PY = sys.executable

EXPECTED = {
    "epics": 15,
    "features": 75,
    "ips": 33,
    "stories": 32,
    "tasks": 32,
}


def _run_integration_script() -> None:
    result = subprocess.run(
        [PY, str(SCRIPTS / "integrate_delivery_master_references.py")],
        cwd=ATHENA,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr or result.stdout


def test_delivery_hierarchy_index_exists() -> None:
    index = SPEC / "DELIVERY-HIERARCHY-INDEX.md"
    complete = SPEC / "DELIVERY-HIERARCHY-COMPLETE.md"
    assert index.is_file()
    assert complete.is_file()
    text = index.read_text(encoding="utf-8")
    assert "ATH-EPIC-MASTER.zip" in text
    assert "ATH-TASK-MASTER.zip" in text


@pytest.mark.parametrize(
    "epic_num",
    list(range(1, 16)),
    ids=[f"E{n:03d}" for n in range(1, 16)],
)
def test_epic_spec_integrated(epic_num: int) -> None:
    epics = SPEC / "ATHENA" / "Epics"
    matches = list(epics.glob(f"EPIC-{epic_num:03d}-*"))
    assert matches, f"epic spec missing for EPIC-{epic_num:03d}"


def test_epic_master_roadmap() -> None:
    roadmap = SPEC / "ATHENA" / "Epics" / "MASTER-ROADMAP.md"
    assert roadmap.is_file()
    assert "EPIC-001" in roadmap.read_text(encoding="utf-8")


def test_feature_packages_extracted() -> None:
    features = SPEC / "ATHENA" / "Features"
    dirs = [p for p in features.rglob("FEATURE-*") if p.is_dir()]
    assert len(dirs) == EXPECTED["features"]


def test_implementation_packages_extracted() -> None:
    ip_root = SPEC / "implementation-packages"
    starter = ip_root / "ATH-IP-Starter-Pack"
    ips = [p for p in ip_root.rglob("ATH-IP-*") if p.is_dir() and p != starter]
    assert starter.is_dir()
    assert len(ips) == EXPECTED["ips"]


@pytest.mark.parametrize("domain", ["Engineering", "AthenaOS", "Data", "Indicators"])
def test_story_domain_packages(domain: str) -> None:
    stories = SPEC / "ATHENA" / "Stories" / domain
    assert stories.is_dir()
    assert any(stories.glob("STORY-*"))


@pytest.mark.parametrize("domain", ["Engineering", "AthenaOS", "Data", "Indicators"])
def test_task_domain_packages(domain: str) -> None:
    tasks = SPEC / "ATHENA" / "Tasks" / domain
    assert tasks.is_dir()
    assert any(tasks.glob("TASK-*"))


def test_story_and_task_counts() -> None:
    stories = [p for p in (SPEC / "ATHENA" / "Stories").rglob("STORY-*") if p.is_dir()]
    tasks = [p for p in (SPEC / "ATHENA" / "Tasks").rglob("TASK-*") if p.is_dir()]
    assert len(stories) == EXPECTED["stories"]
    assert len(tasks) == EXPECTED["tasks"]


def test_epic_count() -> None:
    epics = [p for p in (SPEC / "ATHENA" / "Epics").iterdir() if p.is_dir() and p.name.startswith("EPIC-")]
    assert len(epics) == EXPECTED["epics"]


def test_integration_script_idempotent() -> None:
    _run_integration_script()
    test_feature_packages_extracted()
    test_implementation_packages_extracted()
