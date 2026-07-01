"""Milestone traceability smoke tests — REQ MS-01 … MS-17."""

from __future__ import annotations

import importlib
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
ATHENA = REPO / "athena"
SCRIPTS = ATHENA / "scripts"
SPEC_MILESTONES = ATHENA / "athena-spec" / "ATHENA" / "Milestones"
PY = sys.executable


def _run_script(name: str) -> None:
    result = subprocess.run([PY, str(SCRIPTS / name)], cwd=ATHENA, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr or result.stdout


def _import_optional(module: str):
    try:
        return importlib.import_module(module)
    except ImportError:
        return None


@pytest.mark.parametrize(
    "ms_num",
    list(range(1, 18)),
    ids=[f"M{n}" for n in range(1, 18)],
)
def test_milestone_spec_integrated(ms_num: int) -> None:
    matches = list(SPEC_MILESTONES.glob(f"Milestone-{ms_num:02d}-*"))
    assert matches, f"milestone spec missing for M{ms_num:02d}"
    assert any(matches[0].glob("ATH-*"))


def test_milestone_1_engineering_platform() -> None:
    """M1: inspector, validators, dependency checker."""
    _run_script("check_dependencies.py")
    _run_script("validate_architecture.py")
    _run_script("validate_events.py")
    _run_script("validate_interfaces.py")
    result = subprocess.run(
        [PY, str(SCRIPTS / "athena_inspector.py")],
        cwd=ATHENA,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "Total modules:" in result.stdout


def test_milestone_2_athena_os() -> None:
    """M2: AthenaOS infrastructure modules."""
    mod = _import_optional("athena_os.event_bus")
    if mod is None:
        pytest.skip("athena-os not installed")
    importlib.import_module("athena_os.plugins")
    importlib.import_module("athena_os.configuration")


def test_milestone_3_data_platform() -> None:
    from athena_core.domain.data.quality import check_ohlcv_quality

    assert callable(check_ohlcv_quality)


def test_milestone_4_indicator_platform() -> None:
    from athena_core.domain.indicators.engine import IndicatorEngine

    assert IndicatorEngine is not None


def test_milestone_5_pattern_recognition() -> None:
    from athena_core.domain.patterns.pipeline import PatternPipeline

    assert PatternPipeline is not None


def test_milestone_6_strategy_platform() -> None:
    from athena_core.domain.strategy.engine import StrategyEngine

    assert StrategyEngine is not None


def test_milestone_7_backtesting_simulation() -> None:
    from athena_core.application.backtest_engine import BacktestEngine

    assert BacktestEngine is not None


def test_milestone_8_portfolio_risk() -> None:
    from athena_core.domain.portfolio.models import PortfolioState
    from athena_core.domain.analytics.risk import analyze_risk

    assert PortfolioState is not None
    assert callable(analyze_risk)


def test_milestone_9_oms_paper_trading() -> None:
    from athena_core.application.paper_trading_engine import PaperTradingEngine
    from athena_core.domain.paper.orders import OrderSide

    engine = PaperTradingEngine()
    order = engine.place_order("AAPL", OrderSide.BUY, 10, 150.0)
    assert order.symbol == "AAPL"


def test_milestone_10_live_trading() -> None:
    from athena_core.application.production_manager import ProductionManager

    mgr = ProductionManager()
    assert mgr.gateway is not None


def test_milestone_11_ai_research() -> None:
    orchestrator = _import_optional("athena_ai.application.orchestrator")
    if orchestrator is not None:
        assert orchestrator.ResearchOrchestrator is not None
        return
    from athena_core.domain.research.catalog import QREP_CATALOG

    assert QREP_CATALOG


def test_milestone_12_dashboard() -> None:
    if _import_optional("athena_dashboard") is None:
        assert (ATHENA / "athena-dashboard" / "src").is_dir()
        pytest.skip("athena-dashboard not installed")
    import athena_dashboard

    assert athena_dashboard is not None


def test_milestone_13_devops() -> None:
    assert (REPO / ".github" / "workflows").exists() or (ATHENA / "Makefile").exists()
    assert (SCRIPTS / "install.ps1").is_file()


def test_milestone_14_security() -> None:
    security = _import_optional("athena_os.security")
    if security is not None:
        auth = security.Authenticator()
        user = auth.register("alice", "secret", security.Role.RESEARCHER)
        assert auth.authenticate("alice", "secret") == user
        return
    from athena_core.domain.security import Authenticator, Role

    auth = Authenticator()
    user = auth.register("alice", "secret", Role.RESEARCHER)
    assert auth.authenticate("alice", "secret") == user


def test_milestone_15_enterprise_governance() -> None:
    metrics = _import_optional("athena_os.metrics")
    if metrics is not None:
        collector = metrics.MetricsCollector()
        collector.increment("test.counter")
        assert collector.snapshot()["counters"]["test.counter"] >= 1
        return
    from athena_core.domain.observability import MetricsCollector

    collector = MetricsCollector()
    collector.record("test.counter", 1.0)
    assert collector.query("test.counter")


def test_milestone_16_ecosystem() -> None:
    sdk = _import_optional("athena_sdk")
    if sdk is None:
        assert (ATHENA / "athena-sdk" / "src").is_dir()
        pytest.skip("athena-sdk not installed")
    from athena_sdk.client import AthenaClient

    assert AthenaClient is not None


def test_milestone_17_enterprise_productization() -> None:
    platform = _import_optional("athena_platform.runtime")
    if platform is None:
        assert (ATHENA / "athena-platform" / "src").is_dir()
        pytest.skip("athena-platform not installed")
    from athena_platform.features import PlatformFeatures

    runtime = platform.assemble_runtime(features=PlatformFeatures())
    assert runtime.event_bus is not None
