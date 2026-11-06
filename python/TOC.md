# Python standards — table of contents

## Testing
- [Testing standards](testing/docs/README.md)
- [Validation example](testing/examples/validation.py)
- [pytest parametrization and errors](testing/tests/test_validation.py)

## Typing
- [Typing standards](typing/docs/README.md)
- [Narrowing: None, isinstance, TypeIs, TypeGuard](typing/examples/narrowing.py)
- [Structural typing and exhaustiveness](typing/examples/models.py)
- [Consumer-driven stub conventions](stubs/README.md)
- [Example instructions](typing/examples/README.md)

## Toolchain
- [uv project and ty/pytest configuration](pyproject.toml)

Run commands from `python/`: `uv sync`, `uv run ty check`, `uv run pytest`.
