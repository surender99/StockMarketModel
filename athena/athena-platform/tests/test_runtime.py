"""Platform assembly smoke tests."""

from athena_platform.features import PlatformFeatures
from athena_platform.runtime import assemble_runtime


def test_assemble_runtime() -> None:
    runtime = assemble_runtime(features=PlatformFeatures())
    assert runtime.event_bus is not None
    assert runtime.wiring.container.has("athena_runtime")


def test_feature_toggles() -> None:
    features = PlatformFeatures(ai=True)
    assert "ai" in features.enabled_modules()
