# Python typing standards

## Table of contents
1. [Toolchain](#toolchain)
2. [Required annotation rules](#required-annotation-rules)
3. [Narrowing rules](#narrowing-rules)
4. [Exhaustiveness](#exhaustiveness)
5. [Runtime validation versus static typing](#runtime-validation-versus-static-typing)
6. [Examples and checks](#examples-and-checks)

## Toolchain

Use **Pyright strict** as the type checker and **uv** for dependency management. The shared `python/pyproject.toml` configures both. Python baseline: **3.13+**.

```sh
cd python
uv sync
uv run pyright
uv run pytest
```

## Required annotation rules

- Annotate every public and private function parameter and return type, including `-> None`.
- Prefer built-in generics (`list[str]`, `dict[str, int]`) and `X | None` unions.
- Model shape with `TypedDict`, behavior with `Protocol`, and finite alternatives with `Literal`.
- Do not use `Any` by default. Use `object` for unknown input and narrow before use.
- Keep `cast()` and `# type: ignore` rare, localized, and explained; never use them to mask runtime defects.

## Narrowing rules

1. Use `is None` / `is not None` for optional values.
2. Use `isinstance(value, T)` for ordinary runtime type checks.
3. Use discriminant fields and `Literal` for tagged unions.
4. Use `TypeIs[T]` (PEP 742) for reusable **sound** narrowing; it narrows both true and false branches. The predicate must identify *all and only* values of `T` within the declared input domain.
5. Use `TypeGuard[T]` (PEP 647) only when `TypeIs` cannot express the relationship, such as narrowing invariant `list[object]` to `list[int]`. It narrows only the true branch; do not assume mutation-safe guarantees.
6. Prefer a checked constructor or explicit validation at trust boundaries (JSON, environment, network).

```python
from typing import TypeIs, assert_type

def is_text(value: str | int) -> TypeIs[str]:
    return isinstance(value, str)

def handle(value: str | int) -> None:
    if is_text(value):
        assert_type(value, str)
    else:
        assert_type(value, int)
```

**Caution:** A predicate that returns `False` for some valid members of `T` is *not* suitable for `TypeIs[T]`. For example, `is_positive_int` is not a sound `TypeIs[int]`.

## Exhaustiveness

Use `assert_never()` in the final branch of finite unions, usually with `match` or `if/elif`.

```python
from typing import Literal, assert_never

def label(status: Literal["open", "closed"]) -> str:
    match status:
        case "open":
            return "Open"
        case "closed":
            return "Closed"
        case _:
            assert_never(status)
```

Adding a new status requires updating this handler; Pyright can detect missing cases.

## Runtime validation versus static typing

Annotations do **not** validate values at runtime. Use explicit validation for external data. `typing.assert_type` verifies inferred types in static checking and is not a runtime assertion about an object's type. Run pytest to verify actual behavior.

## Examples and checks

- [Narrowing examples](../examples/narrowing.py): `None`, `isinstance`, `TypeIs`, `TypeGuard`, `assert_type`.
- [Structural and exhaustive typing](../examples/models.py): `TypedDict`, `Protocol`, `Literal`, `assert_never`.
- [Runtime tests](../../testing/tests/test_validation.py).

References: [Python Typing Specification](https://typing.python.org/en/latest/spec/), [Type narrowing](https://typing.python.org/en/latest/spec/narrowing.html), [Pyright configuration](https://github.com/microsoft/pyright/blob/main/docs/configuration.md), [uv docs](https://docs.astral.sh/uv/).
