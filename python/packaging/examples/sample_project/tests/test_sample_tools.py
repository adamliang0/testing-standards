"""Verify package imports and console-entry behavior."""

import pytest

from sample_tools import normalize_label
from sample_tools.cli import main


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("Hello World", "hello-world"),
        ("  Python   Standards ", "python-standards"),
        ("MiXeD", "mixed"),
    ],
)
def test_normalize_label(raw: str, expected: str) -> None:
    assert normalize_label(raw) == expected


def test_reject_blank_label() -> None:
    with pytest.raises(ValueError, match="cannot be blank"):
        normalize_label(" \t ")


def test_cli_prints_result(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["  Hello   World  "]) == 0
    assert capsys.readouterr().out == "hello-world\n"


def test_cli_reports_invalid_label(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as error:
        main(["  "])

    assert error.value.code == 2
    assert "label cannot be blank" in capsys.readouterr().err
