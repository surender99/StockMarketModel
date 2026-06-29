"""SDK and public API framework tests — ATH-REL-020."""

from __future__ import annotations

from athena_sdk import API_VERSION, AthenaClient, RestAPIFacade, WebSocketFacade
from athena_sdk.api import RateLimitState


def test_req_sdk_python_001_client_health() -> None:
    """REQ-SDK-PYTHON-001 — Python SDK."""
    client = AthenaClient()
    health = client.health()
    assert health["status"] == "ok"
    assert health["sdk_version"]


def test_req_sdk_rest_001_api_spec() -> None:
    """REQ-SDK-REST-001 — REST API."""
    client = AthenaClient()
    spec = client.api_spec()
    assert spec["openapi"] == "3.0.0"
    assert "/health" in spec["paths"]


def test_req_sdk_ws_001_websocket() -> None:
    """REQ-SDK-WS-001 — WebSocket API."""
    ws = WebSocketFacade()
    ws.subscribe("scans")
    ws.publish("scans", {"symbol": "AAPL"})
    msgs = ws.drain("scans")
    assert msgs[0]["symbol"] == "AAPL"


def test_req_sdk_cli_001_rate_limiting() -> None:
    """API rate limiting stub."""
    api = RestAPIFacade(RateLimitState(max_requests=2, window_seconds=60))
    api.register("/ping", lambda: "pong")
    assert api.call("/ping")["data"] == "pong"
    api.call("/ping")
    limited = api.call("/ping")
    assert limited.get("error") == "rate_limit_exceeded"
    assert limited["version"] == API_VERSION
