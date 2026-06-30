from athena_research import ResearchWorkspace


def test_workspace() -> None:
    ws = ResearchWorkspace()
    assert ws.catalog is not None
