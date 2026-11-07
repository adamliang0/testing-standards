# Mutability and object semantics: reference patterns

[`examples/models.py`](examples/models.py) is the preferred coding model. Its [tests](tests/test_models.py) verify the ownership contract.

| Failure mode | Preferred implementation |
| --- | --- |
| Shared mutable default | `field(default_factory=list)` or an immutable default; never `def f(items=[])` |
| Unintended mutation of domain values | `@dataclass(frozen=True, slots=True)` with immutable fields |
| Mutation through alias | Copy the caller's mapping before change; return immutable snapshots of internal lists |
| Late-binding closure in a loop | Use a named function factory that captures each loop value |
| Optional collection argument | Use `None` as the default, then construct a new collection inside the function |

A frozen dataclass is **shallowly** frozen; a nested list can still change. Convert nested data to immutable representations when immutability is part of the public contract.

**Escalate** from copying to shared mutable state only if ownership, synchronization, and performance needs are explicit and documented. Execute from `python/`: `uv run pytest mutability/tests`.
