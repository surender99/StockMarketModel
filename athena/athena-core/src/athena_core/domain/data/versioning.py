"""Dataset versioning and immutability — REQ-DATA-VERSION-001, ATH-REL-002 §08."""

from __future__ import annotations

import hashlib


def compute_content_version(checksum_sha256: str, data_version: str) -> str:
    """Derive a reproducible content version from checksum and logical data version."""
    payload = f"{data_version}:{checksum_sha256}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:16]


def build_snapshot_id(symbol: str, content_version: str) -> str:
    """Build an immutable snapshot identifier for registry entries."""
    safe = symbol.replace("/", "_")
    return f"{safe}@{content_version}"
