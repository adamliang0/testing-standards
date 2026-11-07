"""Keep business logic importable and free of command-line side effects."""


def normalize_label(value: str) -> str:
    """Normalize whitespace and Unicode case in a human-readable label."""
    words = value.split()
    if not words:
        raise ValueError("label cannot be blank")
    return "-".join(words).casefold()
