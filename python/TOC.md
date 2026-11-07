# Python standards — table of contents

## Testing
- [Testing standards](testing/docs/README.md)
- [Advanced testing and escalation policy](testing/docs/ADVANCED_TESTING.md)
- [Validation example](testing/examples/validation.py)
- [pytest parametrization and errors](testing/tests/test_validation.py)

## Typing
- [Typing standards](typing/docs/README.md)
- [Narrowing: None, isinstance, TypeIs, TypeGuard](typing/examples/narrowing.py)
- [Structural typing and exhaustiveness](typing/examples/models.py)
- [Consumer-driven stub conventions](stubs/README.md)
- [Example instructions](typing/examples/README.md)

## Code examples
- [Packaging and environments](packaging/README.md)
- [Installable uv project](packaging/examples/sample_project/README.md)
- [Mutability and object semantics](mutability/README.md)
- [Immutable values, state isolation, and closures](mutability/examples/models.py)
- [Exception handling](exceptions/README.md)
- [Typed errors, exception chaining, and boundaries](exceptions/examples/settings.py)

## Toolchain
- [uv project and ty/pytest configuration](pyproject.toml)

Run commands from `python/`: `uv sync`, `uv run ty check`, `uv run pytest`.
