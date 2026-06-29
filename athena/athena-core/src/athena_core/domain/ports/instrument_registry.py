"""Instrument master port — REQ-DATA-INSTR-001, ATH-REL-002 §03."""

from __future__ import annotations

from abc import ABC, abstractmethod

from athena_core.domain.entities.symbol import Symbol


class InstrumentRegistryPort(ABC):
    """Symbol metadata and yfinance ticker resolution."""

    @abstractmethod
    def resolve(self, code: str) -> Symbol | None:
        """Return instrument metadata for *code*, or None if unknown."""

    @abstractmethod
    def list_symbols(self) -> list[Symbol]:
        """Return all registered instruments."""
