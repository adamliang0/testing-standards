"""Validate expected errors, cause chains, and boundary results."""

from pathlib import Path

import pytest

from exceptions.examples.settings import (
    InvalidRetryCount,
    SettingsReadError,
    configuration_status,
    load_retry_count,
    parse_retry_count,
)


@pytest.mark.parametrize("raw", ["0", "3", "5"])
def test_valid_retry_count(raw: str) -> None:
    assert parse_retry_count(raw) == int(raw)


@pytest.mark.parametrize("raw", ["-1", "6", "100"])
def test_reject_out_of_range_retry_count(raw: str) -> None:
    with pytest.raises(InvalidRetryCount, match="between 0 and 5"):
        parse_retry_count(raw)


def test_invalid_integer_preserves_original_cause() -> None:
    with pytest.raises(InvalidRetryCount) as error:
        parse_retry_count("three")
    assert isinstance(error.value.__cause__, ValueError)
    assert "three" in str(error.value)


def test_file_error_preserves_os_cause(tmp_path: Path) -> None:
    missing = tmp_path / "missing.conf"
    with pytest.raises(SettingsReadError) as error:
        load_retry_count(missing)
    assert isinstance(error.value.__cause__, OSError)
    assert str(missing) in str(error.value)


def test_invalid_file_content_is_a_domain_error(tmp_path: Path) -> None:
    config = tmp_path / "retries.conf"
    config.write_text("garbage", encoding="utf-8")
    with pytest.raises(InvalidRetryCount):
        load_retry_count(config)


def test_boundary_reports_success(tmp_path: Path) -> None:
    config = tmp_path / "retries.conf"
    config.write_text("2\n", encoding="utf-8")
    assert configuration_status(config) == (0, "retries: 2")


def test_boundary_reports_expected_failure(tmp_path: Path) -> None:
    status, message = configuration_status(tmp_path / "missing.conf")
    assert status == 2
    assert message.startswith("configuration error: cannot read settings")
