"""Dashboard import smoke tests — REQ-DASH-001."""

from __future__ import annotations

import athena_dashboard


def test_dashboard_import() -> None:
    assert athena_dashboard.__version__ == "0.1.0"
