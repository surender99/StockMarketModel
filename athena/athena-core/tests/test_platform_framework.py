"""DevOps platform framework tests — ATH-REL-018."""

from __future__ import annotations

from athena_core.application.platform_manager import PlatformManager
from athena_core.domain.platform import PipelineStatus


def test_req_ops_cicd_001_pipeline() -> None:
    """REQ-OPS-CICD-001 — CI/CD."""
    mgr = PlatformManager()
    run = mgr.cicd.trigger()
    assert run.status == PipelineStatus.SUCCESS


def test_req_ops_artifact_001_repository() -> None:
    """REQ-OPS-ARTIFACT-001 — artifact repository."""
    mgr = PlatformManager()
    mgr.artifacts.publish("v0.1", "/build/v0.1.tar")
    assert mgr.artifacts.resolve("v0.1") == "/build/v0.1.tar"


def test_req_ops_deploy_001_deployment() -> None:
    """REQ-OPS-DEPLOY-001 — deployment pipelines."""
    mgr = PlatformManager()
    result = mgr.release("0.1.0", "staging")
    assert result["status"] == "deployed"
    assert len(mgr.deploy.list_deployments()) == 1
