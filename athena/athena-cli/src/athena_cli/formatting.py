"""CLI output formatting helpers — REQ-CLI-001."""

from __future__ import annotations

import json
from typing import Any


def emit_output(
    payload: str,
    *,
    output_path: str | None = None,
) -> None:
    if output_path:
        with open(output_path, "w", encoding="utf-8") as fh:
            fh.write(payload)
    else:
        print(payload)


def render_payload(
    data: dict[str, Any] | list[Any],
    *,
    output_format: str,
) -> str:
    if output_format == "json":
        return json.dumps(data, indent=2)
    if output_format == "table" and isinstance(data, dict) and "experiments" in data:
        from athena_core.application.runtime import format_comparison_table

        return format_comparison_table(data)
    return json.dumps(data, indent=2)
