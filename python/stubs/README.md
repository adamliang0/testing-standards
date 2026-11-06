# Consumer-driven Python stubs

Store local `.pyi` files here, with paths matching the **imported module names**. ty searches this directory through `[tool.ty.environment] extra-paths = ["./stubs"]` in `../pyproject.toml`.

## Example layout

For code that statically imports `vendor_api.client`, create:

```text
stubs/
  vendor_api/
    __init__.pyi
    client.pyi
```

The `client.pyi` file can declare only the APIs your application needs:

```python
def execute(query: str) -> list[str]: ...
```

A real stub should be verified against the dependency's actual runtime behavior. A partial stub may hide other attributes of a package instead of merging them with its existing annotations.

## Dynamic imports

For `importlib.import_module(variable)`, a stub by itself does not establish which module has been loaded. Use a typed adapter / `Protocol`, perform runtime checks at the loading boundary, and limit any `cast()` to that boundary.

Do not assume `callable(value)` checks argument or return types. For untrusted plugins, validate outputs on invocation or use a versioned plugin contract with integration tests.

## Checks

From `python/`:

```sh
uv sync
uv run ty check
uv run pytest
```

References: [ty module resolution](https://docs.astral.sh/ty/modules/), [ty configuration](https://docs.astral.sh/ty/reference/configuration/), [Python typing specification](https://typing.python.org/en/latest/spec/).
