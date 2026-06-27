"""Athena SDK — programmatic access to scan, backtest, optimize, experiments — REQ-SDK-001.

Public API: import only ``AthenaClient`` from this package.
Application code must not import ``athena_core`` directly; see README.md.
"""

from athena_sdk.client import AthenaClient

__all__ = ["AthenaClient"]
__version__ = "0.1.0"
