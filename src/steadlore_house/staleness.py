from __future__ import annotations

from datetime import UTC, datetime, timedelta


def parse_utc(value: str) -> datetime:
    """Parse an ISO-8601 timestamp as an aware UTC datetime."""
    normalized = value.replace("Z", "+00:00")
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


def is_stale(last_verified: str, freshness_days: int, *, now: datetime | None = None) -> bool:
    """Return whether a fact is older than its freshness window."""
    checked_at = parse_utc(last_verified)
    current = now or datetime.now(UTC)
    if current.tzinfo is None:
        current = current.replace(tzinfo=UTC)
    return current.astimezone(UTC) - checked_at > timedelta(days=freshness_days)


def age_in_days(last_verified: str, *, now: datetime | None = None) -> int:
    """Return the non-negative age of a verification timestamp in whole days."""
    checked_at = parse_utc(last_verified)
    current = now or datetime.now(UTC)
    if current.tzinfo is None:
        current = current.replace(tzinfo=UTC)
    age = current.astimezone(UTC) - checked_at
    return max(age.days, 0)
