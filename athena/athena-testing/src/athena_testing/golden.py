"""Golden dataset path resolution."""

from __future__ import annotations

from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[2]
GOLDEN_DATASETS_DIR = PACKAGE_ROOT / "golden-datasets"
SPEC_GOLDEN_DIR = PACKAGE_ROOT.parent / "athena-spec" / "ATHENA" / "Golden-Datasets"


def resolve_golden_dataset(name: str) -> Path:
    """Resolve a golden dataset by filename from local or spec directory."""
    local = GOLDEN_DATASETS_DIR / name
    if local.exists():
        return local
    spec = SPEC_GOLDEN_DIR / name
    if spec.exists():
        return spec
    msg = f"golden dataset not found: {name}"
    raise FileNotFoundError(msg)
