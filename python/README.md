# Python standards

This directory contains two independent standards:

- [Testing](testing/docs/README.md): pytest, test isolation, parametrization, mocks, coverage, and CI.
- [Typing](typing/docs/README.md): strict Pyright, annotations, narrowing, and exhaustiveness.

Package manager: **uv**. Python baseline: **3.13+** (so `typing.TypeIs` is available).

From `python/`:

```sh
uv sync
uv run pyright
uv run pytest
```

See [typing examples](typing/examples/) and [testing examples](testing/examples/).
