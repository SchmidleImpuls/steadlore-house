import pytest

from steadlore_house.cli import main


@pytest.mark.parametrize(
    ("argv", "expected"),
    [
        (["--help"], "Local-first household continuity tooling"),
        (["generate-manual", "--help"], "Generate a deterministic Markdown Continuity Manual"),
        (["generate-ai-packet", "--help"], "must not authorize privileged actions"),
        (["discover-network", "--help"], "Does not perform port scans"),
        (["discover-network", "--help"], "offline MAC vendor enrichment"),
        (["discover-network", "--help"], "review-required Manual Inventory"),
    ],
)
def test_cli_help_documents_commands(argv: list[str], expected: str, capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as raised:
        main(argv)

    assert raised.value.code == 0
    assert expected in capsys.readouterr().out
