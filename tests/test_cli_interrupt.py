import pytest

from steadlore_house import cli


def test_cli_handles_keyboard_interrupt_cleanly(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr(cli, "_main", lambda parser, argv=None: (_ for _ in ()).throw(KeyboardInterrupt()))

    with pytest.raises(SystemExit) as raised:
        cli.main(["--help"])

    assert raised.value.code == 130
    assert "Cancelled." in capsys.readouterr().err
