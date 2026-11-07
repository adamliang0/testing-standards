"""Translate low-level errors and report failures at a single boundary."""

from pathlib import Path


class SettingsError(Exception):
    """Base exception for configuration failures."""


class InvalidRetryCount(SettingsError):
    """Configuration contains an invalid retry count."""


class SettingsReadError(SettingsError):
    """The configuration source could not be read."""


def parse_retry_count(raw: str) -> int:
    try:
        retries = int(raw)
    except ValueError as exc:
        raise InvalidRetryCount(f"not an integer: {raw!r}") from exc

    if not 0 <= retries <= 5:
        raise InvalidRetryCount("retries must be between 0 and 5")
    return retries


def load_retry_count(path: Path) -> int:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise SettingsReadError(f"cannot read settings from {path}") from exc

    # Already a domain error: let it propagate without catching and rethrowing.
    return parse_retry_count(text.strip())


def configuration_status(path: Path) -> tuple[int, str]:
    """Translate expected domain errors at the application boundary."""
    try:
        retries = load_retry_count(path)
    except SettingsError as exc:
        return 2, f"configuration error: {exc}"

    return 0, f"retries: {retries}"
