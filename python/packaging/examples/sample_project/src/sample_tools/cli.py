"""Parse CLI arguments at the boundary; delegate logic to a pure function."""

import argparse
from collections.abc import Sequence

from .formatting import normalize_label


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Normalize a label.")
    parser.add_argument("label", help="Text to normalize")
    args = parser.parse_args(argv)

    try:
        label = normalize_label(args.label)
    except ValueError as exc:
        parser.error(str(exc))

    print(label)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
