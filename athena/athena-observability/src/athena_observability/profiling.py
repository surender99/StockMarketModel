"""Profiling stub."""

from __future__ import annotations

import time
from contextlib import contextmanager
from typing import Iterator


@contextmanager
def profile_block(name: str) -> Iterator[None]:
    start = time.perf_counter()
    yield
    _ = time.perf_counter() - start
    _ = name


__all__ = ["profile_block"]
