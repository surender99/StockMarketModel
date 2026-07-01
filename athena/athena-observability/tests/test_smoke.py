from athena_observability import check_health


def test_health_smoke() -> None:
    status = check_health("athena-testing")
    assert status.healthy
