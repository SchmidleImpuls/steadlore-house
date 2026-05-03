from pathlib import Path

import pytest

from steadlore_house import cli


def test_review_inventory_draft_cli_refuses_to_overwrite(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    output = tmp_path / "household.yaml"
    output.write_text("existing\n", encoding="utf-8")

    with pytest.raises(SystemExit) as raised:
        cli.main(["review-inventory-draft", "--draft", "dist/inventory-draft.yaml", "--output", str(output)])

    assert raised.value.code == 2


def test_review_inventory_draft_cli_reports_validation_errors_without_traceback(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    draft = tmp_path / "inventory-draft.yaml"
    draft.write_text(
        """
household_name: Example
people: []
devices:
  - id: gateway
    name: Gateway
    device_type: Gateway
    core: true
    location: Utility cabinet
    household_impact: Provides network connectivity.
services: []
secret_references: []
""".strip()
        + "\n",
        encoding="utf-8",
    )

    with pytest.raises(SystemExit) as raised:
        cli.main(["review-inventory-draft", "--draft", str(draft), "--output", str(tmp_path), "--force"])

    assert raised.value.code == 2
    captured = capsys.readouterr()
    assert "Validation failed" in captured.err
    assert "use core_infrastructure" in captured.err
    assert "Traceback" not in captured.err



def test_review_inventory_draft_cli_writes_output_with_force(monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    answers = iter(
        [
            "Example Household",
            "n",
            "y",
            "main-gateway",
            "Main Gateway",
            "Gateway",
            "y",
            "Utility cabinet",
            "Provides internet access and local routing for the household.",
            "n",
        ]
    )
    monkeypatch.setattr(cli.builtins, "input", lambda text: next(answers))
    output = tmp_path / "household.yaml"

    result = cli.main(["review-inventory-draft", "--draft", "dist/inventory-draft.yaml", "--output", str(output), "--force"])

    assert result == 0
    assert "Wrote reviewed Manual Inventory" in capsys.readouterr().out
    assert "_review" not in output.read_text(encoding="utf-8")
