from datetime import UTC, datetime

from steadlore_house.staleness import age_in_days, is_stale


def test_stale_when_older_than_freshness_window() -> None:
    now = datetime(2026, 5, 1, tzinfo=UTC)

    assert is_stale("2026-03-01T00:00:00Z", 30, now=now)


def test_current_when_inside_freshness_window() -> None:
    now = datetime(2026, 5, 1, tzinfo=UTC)

    assert not is_stale("2026-04-20T00:00:00Z", 30, now=now)


def test_age_in_days() -> None:
    now = datetime(2026, 5, 1, 12, tzinfo=UTC)

    assert age_in_days("2026-04-20T12:00:00Z", now=now) == 11
