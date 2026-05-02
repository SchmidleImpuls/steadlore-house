from datetime import UTC, datetime
from pathlib import Path

import pytest

from steadlore_house import cli
from steadlore_house.network_discovery import NetworkSnapshot


def test_discover_network_requires_nmap_when_active_scan_is_requested(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setattr(cli.shutil, "which", lambda name: None)

    with pytest.raises(SystemExit) as raised:
        cli.main(["discover-network", "--active-scan", "--subnet", "192.0.2.0/24", "--output", str(tmp_path)])

    assert raised.value.code == 2


def test_discover_network_reports_active_scan_failures(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setattr(cli.shutil, "which", lambda name: "nmap")
    monkeypatch.setattr(
        cli,
        "discover_network",
        lambda **kwargs: (_ for _ in ()).throw(cli.NetworkDiscoveryError("nmap ping scan failed for 192.0.2.0/24: example failure")),
    )

    with pytest.raises(SystemExit) as raised:
        cli.main(["discover-network", "--active-scan", "--subnet", "192.0.2.0/24", "--output", str(tmp_path)])

    assert raised.value.code == 2


def test_discover_network_prints_minimal_feedback(monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    snapshot = NetworkSnapshot(observed_at=datetime(2026, 5, 1, tzinfo=UTC), method="passive local OS snapshot")
    monkeypatch.setattr(cli, "discover_network", lambda **kwargs: snapshot)

    result = cli.main(["discover-network", "--output", str(tmp_path)])

    assert result == 0
    output = capsys.readouterr().out
    assert "Discovering network (passive local snapshot)" in output
    assert "Wrote Network Discovery Snapshot" in output
    assert (tmp_path / "network-snapshot.md").is_file()


def test_discover_network_can_write_inventory_draft(monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    snapshot = NetworkSnapshot(
        observed_at=datetime(2026, 5, 1, tzinfo=UTC),
        method="passive local OS snapshot",
    )
    monkeypatch.setattr(cli, "discover_network", lambda **kwargs: snapshot)

    result = cli.main(["discover-network", "--output", str(tmp_path / "snapshot.md"), "--inventory-draft", str(tmp_path)])

    assert result == 0
    output = capsys.readouterr().out
    assert "Wrote review-required Manual Inventory draft" in output
    assert (tmp_path / "inventory-draft.yaml").is_file()
