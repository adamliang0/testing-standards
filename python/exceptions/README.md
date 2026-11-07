# Exception handling: reference patterns

[`examples/settings.py`](examples/settings.py) is the preferred coding model; [its tests](tests/test_settings.py) check failure types and chained causes.

1. Define a small domain exception hierarchy when callers need a stable error contract.
2. Catch only errors the current layer can translate or recover from. Keep each `try` block small; avoid routine `except Exception`.
3. Translate low-level exceptions with `raise DomainError("context") from exc`. Leave `__cause__` and the original traceback intact.
4. Reject invalid values explicitly rather than returning ambiguous `None` or silently using defaults.
5. Convert expected domain failures into an HTTP response, CLI exit status, or job result **once**, at the owning boundary. Do not log and re-raise at every layer.
6. Do not catch an exception just to rethrow it. If a catch is required, use bare `raise` to preserve its traceback.

**Escalate:** Use targeted retries only for transient, idempotent operations; use `ExceptionGroup` / `except*` for independently failing concurrent tasks.

From `python/`: `uv run pytest exceptions/tests`.
