from pathlib import Path

from steadlore_house.cli import _resolve_output_path, _write_markdown, build_parser


def test_output_path_directory_uses_default_filename(tmp_path: Path) -> None:
    assert _resolve_output_path(tmp_path, default_filename="network-snapshot.md") == tmp_path / "network-snapshot.md"


def test_output_path_file_is_used_as_given(tmp_path: Path) -> None:
    output = tmp_path / "custom.md"

    assert _resolve_output_path(output, default_filename="network-snapshot.md") == output


def test_write_markdown_accepts_existing_directory(tmp_path: Path) -> None:
    output = _write_markdown(tmp_path, "# Example\n", default_filename="network-snapshot.md", parser=build_parser())

    assert output == tmp_path / "network-snapshot.md"
    assert output.read_text(encoding="utf-8") == "# Example\n"
