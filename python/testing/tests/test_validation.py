"""Behavioral pytest examples for validation boundaries."""

import pytest

from testing.examples.validation import parse_positive_int


@pytest.mark.parametrize(
    ("text", "expected"),
    [("1", 1), ("42", 42), ("0002", 2)],
)
def test_parse_positive_int(text: str, expected: int) -> None:
    assert parse_positive_int(text) == expected


@pytest.mark.parametrize("text", ["0", "-3", "abc"])
def test_reject_invalid_int(text: str) -> None:
    with pytest.raises(ValueError):
        parse_positive_int(text)
