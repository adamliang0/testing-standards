# Typing examples

These examples are checked **statically** by ty and show runtime behavior.

From `python/`:

```sh
uv sync
uv run ty check
uv run python typing/examples/narrowing.py
uv run python typing/examples/models.py
```

| Example | Concepts |
| --- | --- |
| [narrowing.py](narrowing.py) | `None`, `isinstance`, `TypeIs`, `TypeGuard`, `assert_type` |
| [models.py](models.py) | `TypedDict`, `Protocol`, `Literal`, `assert_never` |

These modules use `typing.assert_type` for static assertions; it does not assert a runtime type. For executable behavioral tests, see [pytest tests](../../testing/tests/test_validation.py).
