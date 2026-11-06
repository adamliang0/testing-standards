# Testing standards: pytest

## Table of contents
1. [Setup and execution](#setup-and-execution)
2. [Test design](#test-design)
3. [Fixtures and isolation](#fixtures-and-isolation)
4. [Mocking](#mocking)
5. [Coverage and CI](#coverage-and-ci)
6. [Review checklist](#review-checklist)

## Setup and execution

Run all commands from `python/`. Use **uv**, not `pip install` for project dependencies.

```sh
uv sync
uv run pytest
uv run pytest --cov=testing --cov-report=term-missing
```

Use **pytest** as the only test runner. Do not use `unittest.TestCase`, `TestSuite`, or `unittest` test discovery. `unittest.mock` is allowed for isolation.

## Test design
- Name files `test_*.py`, functions `test_*`; use Arrange–Act–Assert.
- Test observable behavior rather than private implementation.
- Use plain `assert`, `pytest.raises`, and `@pytest.mark.parametrize`.
- Add boundary cases: empty inputs, `None`, invalid types, exception paths, and limits.
- Keep tests deterministic and independent of ordering or external services.

```python
import pytest

@pytest.mark.parametrize(
    ("value", "expected"),
    [(0, 0), (1, 1), (-1, 1)],
)
def test_absolute_value(value: int, expected: int) -> None:
    assert abs(value) == expected

def test_invalid_integer() -> None:
    with pytest.raises(ValueError):
        int("not-an-integer")
```

## Fixtures and isolation
- Prefer function-scoped fixtures; widen scope only for expensive immutable resources.
- Use `tmp_path` for files and `monkeypatch` for environment changes.
- Use `yield` fixtures when cleanup is necessary.
- Do not share mutable global state between tests.

## Mocking
- Prefer dependency injection and lightweight fakes.
- Use `unittest.mock.Mock`, `create_autospec`, `patch`, or `AsyncMock` when replacing a boundary.
- Patch the name **where it is looked up**, not where it was originally defined.
- Avoid mocks of the exact behavior being tested.

## Coverage and CI
- Treat coverage as a diagnostic signal, not proof of quality.
- Cover high-risk branches and exceptions. Review missing lines rather than maximizing a number.
- Run `uv sync --locked`, `uv run ty check`, and `uv run pytest --cov` in CI once `uv.lock` is committed.
- CI should fail on test failures and static type errors.

## Review checklist
- [ ] Tests are deterministic, isolated, and named for behavior.
- [ ] Success, failure, and boundary cases are covered.
- [ ] No network, clock, or filesystem dependencies without explicit isolation.
- [ ] Parametrization replaces needless repeated tests.
- [ ] Types of test functions and fixtures are explicit.
- [ ] `uv run pytest` and `uv run ty check` pass.

See [runnable example](../tests/test_validation.py).
