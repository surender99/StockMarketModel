"""YAML instrument master — REQ-DATA-INSTR-001, ATH-REL-002 §03."""

from __future__ import annotations

from pathlib import Path

import yaml

from athena_core.domain.entities.symbol import Symbol
from athena_core.domain.ports.instrument_registry import InstrumentRegistryPort

_DEFAULT_INSTRUMENTS = Path(__file__).resolve().parents[3] / "config" / "instruments.yaml"


class YamlInstrumentMaster(InstrumentRegistryPort):
    """Static YAML-backed instrument registry."""

    def __init__(self, instruments_file: Path | str | None = None) -> None:
        path = Path(instruments_file) if instruments_file else _DEFAULT_INSTRUMENTS
        self._symbols = self._load(path)

    @staticmethod
    def _load(path: Path) -> dict[str, Symbol]:
        if not path.is_file():
            return {}
        with path.open(encoding="utf-8") as fh:
            raw = yaml.safe_load(fh)
        entries = raw.get("instruments", []) if isinstance(raw, dict) else raw or []
        symbols: dict[str, Symbol] = {}
        for item in entries:
            if not isinstance(item, dict):
                continue
            code = str(item.get("code", "")).strip()
            if not code:
                continue
            symbols[code.upper()] = Symbol(
                code=code,
                exchange=str(item.get("exchange", "NSE")),
                yfinance_suffix=str(item.get("yfinance_suffix", ".NS")),
            )
        return symbols

    def resolve(self, code: str) -> Symbol | None:
        return self._symbols.get(code.upper())

    def list_symbols(self) -> list[Symbol]:
        return sorted(self._symbols.values(), key=lambda s: s.code)
