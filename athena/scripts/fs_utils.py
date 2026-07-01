"""Filesystem helpers for integration scripts (Windows-safe tree removal)."""
from __future__ import annotations

import os
import shutil
import stat
import time
from pathlib import Path


def safe_rmtree(path: Path, *, retries: int = 5) -> None:
    """Remove a directory tree, retrying on Windows file-lock errors."""
    if not path.exists():
        return

    def _onerror(func, p, _exc_info) -> None:
        os.chmod(p, stat.S_IWRITE)
        func(p)

    last_err: BaseException | None = None
    for attempt in range(retries):
        try:
            shutil.rmtree(path, onerror=_onerror)
            return
        except (PermissionError, OSError) as exc:
            last_err = exc
            time.sleep(0.15 * (attempt + 1))
    if last_err is not None:
        raise last_err
