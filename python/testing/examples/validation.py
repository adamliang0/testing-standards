"""Small subject under test: input validation stays a runtime obligation."""


def parse_positive_int(text: str) -> int:
    try:
        value = int(text)
    except ValueError as exc:
        raise ValueError("not an integer") from exc
    if value <= 0:
        raise ValueError("must be positive")
    return value
