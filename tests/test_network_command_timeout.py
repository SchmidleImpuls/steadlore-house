import subprocess

import pytest

from steadlore_house.network_discovery import _run


def test_run_returns_completed_process_on_timeout(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_run(*args, **kwargs):
        raise subprocess.TimeoutExpired(cmd=args[0], timeout=3, output="partial")

    monkeypatch.setattr(subprocess, "run", fake_run)

    result = _run(["example"], timeout=3)

    assert result.returncode == 124
    assert result.stdout == "partial"
    assert "timed out" in result.stderr
