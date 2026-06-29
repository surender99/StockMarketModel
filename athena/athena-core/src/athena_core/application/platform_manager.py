"""Platform manager — ATH-REL-018."""

from __future__ import annotations

from athena_core.domain.platform import (
    ArtifactRepository,
    CICDPipeline,
    DeploymentPipeline,
    DeploymentTarget,
    PipelineStatus,
)


class PlatformManager:
    """Orchestrate DevOps and platform engineering workflows."""

    def __init__(self) -> None:
        self.cicd = CICDPipeline("athena-main")
        self.artifacts = ArtifactRepository()
        self.deploy = DeploymentPipeline(self.artifacts)

    def release(self, version: str, target_env: str = "staging") -> dict:
        run = self.cicd.trigger()
        if run.status != PipelineStatus.SUCCESS:
            return {"status": "failed"}
        artifact = run.artifacts[0]
        self.artifacts.publish(version, artifact)
        return self.deploy.deploy(DeploymentTarget(version, target_env, image=f"athena:{version}"))
