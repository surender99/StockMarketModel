"""Delivery hierarchy IP MVP probes — ATH-IP-000001 … 000033."""

from __future__ import annotations

import importlib
from pathlib import Path

import pytest

from athena_common.delivery_ips import DELIVERY_IPS, DeliveryIP

REPO = Path(__file__).resolve().parents[3]
ATHENA = REPO / "athena"
SCRIPTS = ATHENA / "scripts"


def _resolve_import(target: str) -> object:
    module_path, _, symbol = target.partition(":")
    if not symbol:
        msg = f"import target must be module:symbol, got {target!r}"
        raise ValueError(msg)
    module = importlib.import_module(module_path)
    return getattr(module, symbol)


def _resolve_script(target: str) -> Path:
    path = ATHENA / target if target.startswith("codegen/") else SCRIPTS / target
    if not path.is_file():
        msg = f"script not found: {path}"
        raise FileNotFoundError(msg)
    return path


@pytest.mark.parametrize("ip", DELIVERY_IPS, ids=[ip.ip_id for ip in DELIVERY_IPS])
def test_delivery_ip_mvp_probe(ip: DeliveryIP) -> None:
    if ip.probe_kind == "import":
        obj = _resolve_import(ip.target)
        assert obj is not None
        return

    assert _resolve_script(ip.target).is_file()


def test_delivery_ip_registry_count() -> None:
    assert len(DELIVERY_IPS) == 33
