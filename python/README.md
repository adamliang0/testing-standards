# Python standards

This directory contains testing and typing standards, plus executable coding examples:

- [Testing](testing/docs/README.md): pytest, test isolation, parametrization, mocks, coverage, and CI.
- [Typing](typing/docs/README.md): ty, annotations, narrowing, consumer-driven stubs, and exhaustiveness.
- [Packaging](packaging/README.md): installable uv project and typed CLI.
- [Mutability](mutability/README.md): value semantics, independent state, and closures.
- [Exceptions](exceptions/README.md): domain errors, chaining, and boundary translation.

Package manager: **uv**. Python baseline: **3.13+** (so `typing.TypeIs` is available).

From `python/`:

```sh
uv sync
uv run ty check
uv run pytest
```

The packaging example is an independent project: run its commands from `packaging/examples/sample_project/`.

Local type stubs belong in [stubs/](stubs/README.md).
See [typing examples](typing/examples/), [testing examples](testing/examples/), and [the table of contents](TOC.md).
