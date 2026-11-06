# Advanced Python testing standard: risk-based escalation

**Scope:** Python services, libraries, CLIs, plugins, and reference implementations.
**Toolchain:** `pytest` as the sole test runner; `uv` for dependency management; `ty` for static checking; `stubs/` for local type stubs.
**Status:** Normative guidance. "MUST" is mandatory, "SHOULD" is the default with documented exceptions, and "MAY" is optional.

This standard extends [the baseline pytest guide](README.md). It defines **five required areas of test design** and **when to escalate** to expensive or advanced methods. Escalation is driven by failure impact and defects that simpler tests cannot detect—not by a desire to use every tool.

## 1. Baseline: required for every behavior change

Before considering an advanced technique, the change MUST have:

1. `pytest` tests that assert public/observable behavior: normal, boundary, invalid-input, and failure paths as applicable. Use `pytest.mark.parametrize` instead of duplicated tests.
2. Independent, deterministic tests with function-scoped fixtures by default. Control time, randomness, environment, files, and external effects; use `tmp_path`, `monkeypatch`, injected dependencies, and `unittest.mock` as needed.
3. No uncontrolled live network, shared mutable state, real production credentials, or production data.
4. An explicit check for untested branches and meaningful assertions. Coverage is evidence of execution, **not evidence of correctness**.
5. `uv run ty check` and `uv run pytest` passing. Test functions and reusable fixtures SHOULD have useful type annotations.

**Do not escalate automatically.** A small deterministic transformation with a few well-understood input classes generally needs only parametrized example tests. Every escalation MUST cover an identified risk or provide a detection capability the baseline lacks.

## 2. Decision procedure

For each change, ask these questions in order:

1. **What can fail?** Identify invariants, boundary values, state transitions, external contracts, and observable side effects.
2. **How costly would a failure be?** Classify as routine, elevated (repeated regressions or complex behavior), or critical (security, authorization, financial correctness, irreversible writes, integrity, availability).
3. **Can example-based tests detect the plausible defect?** If yes and the impact is routine, stop at the baseline.
4. **Which risk is still untested?** Select the **smallest** advanced technique that exercises it. Multiple techniques may be necessary; they are not a required sequence.
5. **What is the exit evidence?** Record the property, mutant, contract, fault, or reproducible interleaving the new test detects. If the method finds no actionable signal, simplify it rather than retaining expensive test infrastructure by default.

### Escalation matrix

| Signal / risk | Escalate to | Required evidence |
| --- | --- | --- |
| Large input space, parser/codec, complex normalization, many edge cases | Hypothesis property-based or metamorphic testing | An invariant holds across generated inputs; failing cases are reproducible and shrinkable |
| A sequence of operations changes later outcomes (create/update/delete, cache, workflow) | Hypothesis stateful testing with a reference model | Invariants hold after generated operation sequences |
| Two implementations or formats should agree | Differential testing | Equivalent observable results across implementations |
| High-impact business rules, repeat escaped bugs, or tests execute lines without detecting wrong behavior | Targeted mutation testing (e.g., `mutmut`) | Meaningful mutants are killed or each survivor is reviewed |
| Database transactions, migrations, queues, caches, wire protocols, or service-specific semantics | Real integration tests; Testcontainers when containerized services are available | Behavior is verified against a supported real dependency version |
| Versioned HTTP/API contract with a machine-readable schema | Schemathesis and explicit consumer contract tests as needed | Generated invalid/valid requests and response constraints are checked |
| Ordering, clock, random seed, concurrency, retries, cancellation, or cleanup can change outcomes | Fault injection, controlled clock/scheduler, order perturbation, repeated or concurrent runs | A recorded seed/schedule/fault reliably reproduces the check |
| A suite is too slow to run fully on each pull request | Separate fast PR and scheduled/release suites; consider `pytest-xdist` after isolation checks | Fast feedback remains reliable; advanced suite still runs on a defined cadence |

**Critical changes MUST receive a documented risk review.** Use at least one targeted technique beyond baseline where a meaningful risk remains (for example, database transaction integration tests for irreversible writes). Risk classification does not require using all techniques.

## 3. Five testing requirements

### 3.1 Test behavior and invariants

**Baseline MUST:** Test public behavior with meaningful expected outcomes; cover rejected values, boundaries, and exception semantics. Do not assert incidental implementation details or mock the function under test.

**Escalate when:** Input combinations are unbounded; invariants are clearer than example outputs; serialization, parsing, validation, algorithms, or business rules have many edge cases; or behavior depends on prior operations.

**Advanced methods:**
- **Property-based:** Use `hypothesis.given` and strategies to explore many valid or invalid inputs; write a precise invariant, not `assert result is not None`.
- **Metamorphic:** Assert relations when no single reference answer is easy to compute, e.g. `decode(encode(x)) == x` or sorting twice equals sorting once.
- **Differential:** Compare a new implementation against an independent reference; avoid sharing the same flawed logic in both sides.
- **Stateful:** Use `RuleBasedStateMachine` for transitions and a simple independent model; exercise actions, preconditions, and invariants after each transition.

Example, run from `python/`:

```python
from hypothesis import given, strategies as st

from testing.examples.validation import parse_positive_int


@given(st.integers(min_value=1, max_value=1_000_000))
def test_positive_decimal_round_trip(value: int) -> None:
    assert parse_positive_int(str(value)) == value
```

**Stop condition:** If a bounded set of examples completely represents the behavior, do not add generated tests merely for volume. Generated tests MUST report a minimal reproducible counterexample and SHOULD avoid non-deterministic external services.

### 3.2 Measure test effectiveness

**Baseline MUST:** Inspect branch and exception-path coverage on modified code. Coverage increases do not justify weak assertions.

**Escalate when:** An authorization/financial/integrity rule changes; the same behavior has regressed more than once; line/branch coverage is high but assertions are shallow; or reviewers cannot show that tests reject a plausible incorrect implementation.

**Advanced method:** Run targeted `mutmut` against production logic, not tests, dependencies, generated code, or unrelated modules. Review **surviving** and **no-coverage** mutants. Write a test for a realistic surviving defect; document genuinely equivalent mutants rather than forcing arbitrary tests.

Mutation metrics SHOULD show killed, survived, equivalent/excluded, not-covered, and not-run counts separately. A mutation percentage MUST NOT be used as a release gate until scope, exclusions, and a reliable baseline are established. Never claim that 100% mutation score proves correctness.

**Operational constraint:** Current `mutmut` requires POSIX fork support; use Linux/macOS or WSL on Windows. When forks interact poorly with threads, event loops, or database handles, use supported process-isolation options and inspect results.

### 3.3 Control dependencies and test contracts

**Baseline MUST:** Prefer dependency injection, local fakes, `tmp_path`, and `monkeypatch`. Mock an external boundary, not the behavior being asserted. Avoid sleeping and reaching live services.

**Escalate when:** Correctness depends on real SQL semantics, transaction boundaries, database migrations, message delivery, cache expiry, HTTP serialization, or API schema validation. Mocks cannot prove those properties.

**Advanced methods:**
- **Testcontainers:** Run a disposable real service version (such as PostgreSQL) under pytest fixtures. Isolate database/schema per test or transaction and clean all persistent state. Docker is a documented prerequisite.
- **Schemathesis:** Generate API cases from OpenAPI/GraphQL schemas. Add semantic assertions and authentication/authorization tests because schema compliance alone cannot establish business correctness.
- **Consumer-driven contracts:** Verify compatibility across independently deployed clients/providers when a schema alone does not describe the behavior.
- **Dynamic imports and `stubs/`:** `ty` and partial `.pyi` stubs verify the declared consumer-facing shape statically; a separate runtime contract/integration test MUST confirm that dynamically loaded modules actually provide that shape.

**Stop condition:** Do not start containers for pure functions or mock real database behavior in an integration test. Reserve slow/external tests for the contracts they alone can verify.

### 3.4 Test failure modes and nondeterminism

**Baseline MUST:** Cover expected exception paths and cleanup. Tests MUST control clocks, random seeds, timeouts, and mutable global state when relevant; each test must be independent of execution order.

**Escalate when:** Code retries, cancels, runs async tasks/threads, persists multi-step changes, or must recover from external faults; failures appear only under certain orders or schedules; or previous bugs involved partial progress.

**Advanced methods:**
- **Fault injection:** Inject timeouts, connection drops, duplicate messages, malformed responses, failed writes, and mid-operation cancellation. Assert retry bounds, idempotency, rollback/compensation, cleanup, and the final observable state.
- **Order perturbation:** Use `pytest-randomly` to expose shared-state coupling. Log and reproduce the seed (`--randomly-seed`).
- **Concurrency/stateful stress:** Exercise conflicting operations and race-prone paths with explicit barriers or controlled scheduling; use repeated or randomized schedules when the hazard is timing-dependent.
- **Parallel execution:** Enable `pytest-xdist` only after tests are safe to run in separate workers and temporary services/ports/databases do not collide. Parallel runs are not a substitute for concurrency correctness tests.

**Stop condition:** Do not make unpredictable stress tests mandatory in the fast PR suite unless they are reliable. Every failure MUST preserve a seed, fault configuration, schedule, or minimal case. Reruns may diagnose a flake, but MUST NOT silently turn an unstable test into a pass.

### 3.5 Establish proportional CI gates

Use separate execution tiers; **not every advanced test is a PR gate**.

| Tier | When | Required checks |
| --- | --- | --- |
| Fast PR (all changes) | Every pull request | `ty check`, pytest behavior tests, coverage report including branches, no flaky failures |
| Targeted PR (triggered) | Changes matching the escalation matrix | Relevant property/stateful, contract/integration, or failure-injection tests |
| Scheduled / nightly | Slow fuzz/stateful, broad mutation, multiple random seeds, full integration matrix | Trend reports, reproducible failures, assigned ownership |
| Release / critical change | Before high-impact release or after a severe defect | Re-run relevant targeted checks and review remaining untested risks |

From `python/`, the existing project supports:

```sh
uv sync
uv run ty check
uv run pytest --cov --cov-branch --cov-report=term-missing
```

**After `python/uv.lock` is generated and committed**, CI SHOULD use the locked equivalents:

```sh
uv sync --locked
uv run --locked ty check
uv run --locked pytest --cov --cov-branch --cov-report=term-missing
```

The lockfile is **not yet present** in this reference repository. Do not claim these locked commands are currently an enforced gate. Add optional testing libraries with `uv add --dev <package>` or a dedicated `uv add --group testing-advanced <package>` and commit the updated lockfile before enabling corresponding jobs.

**CI policy:**
- A failed deterministic test or static check MUST block a merge. PR gates MUST be reproducible from the published dependency set.
- Branch coverage is a diagnostic; only set `--cov-fail-under` after a measured baseline and a team-approved threshold. Review missing critical branches regardless of percentage.
- Mutation score and randomized/stress results SHOULD initially be advisory. Promote a check to required only when execution is stable, runtime cost is acceptable, and a remediation owner exists.
- Failed scheduled or release checks MUST produce an actionable issue; do not ignore them because the PR suite passed.
- If a test is quarantined, record owner, reason, issue, and expiry/review date. Do not use `xfail` or automatic reruns to hide persistent defects.

## 4. Examples of choosing the correct level

| Change | Appropriate tests | Usually unnecessary |
| --- | --- | --- |
| Small helper with three defined cases | Parametrized behavior, boundary, and error tests | Containers, mutation campaign, state machine |
| Parser/serializer with many possible strings | Examples + Hypothesis round-trip/invalid-input properties | Real database integration |
| Authorization decision or billing formula | Examples + adversarial properties + targeted mutation tests | General-purpose concurrency stress unless shared state exists |
| Database migration or transaction | Real database integration, rollback and failure injection | Mock-only assertions |
| Async retry worker handling duplicate events | Injected clock/faults, idempotency checks; stateful model if operations interact | Mutation testing as the first response |
| API schema version upgrade | Schemathesis contract cases + compatibility and security assertions | Mutation testing on unrelated modules |

## 5. Test review and exception record

A PR reviewer SHOULD be able to answer:

1. What behavior and invariant does each test defend?
2. Which meaningful failure modes were considered?
3. Which escalation trigger applies, or why is baseline sufficient?
4. Are tests isolated, deterministic, typed, and reproducible?
5. What CI tier will execute the chosen tests, and what failure will block release?

For waived advanced testing on a critical change, record: **risk**, **reason the method is not proportionate**, **alternative evidence**, **owner**, and **revisit condition/date**. Avoid untracked permanent exceptions.

## 6. References

- [pytest documentation](https://docs.pytest.org/en/stable/) and [flaky-test guidance](https://docs.pytest.org/en/stable/explanation/flaky.html)
- [Hypothesis property-based and stateful testing](https://hypothesis.readthedocs.io/en/latest/stateful.html)
- [mutmut documentation](https://mutmut.readthedocs.io/en/latest/)
- [coverage.py branch measurement](https://coverage.readthedocs.io/en/latest/branch.html)
- [Testcontainers for Python](https://docs.docker.com/guides/testcontainers-python-getting-started/)
- [Schemathesis pytest integration](https://schemathesis.readthedocs.io/en/latest/explanations/pytest/)
- [pytest-randomly](https://github.com/pytest-dev/pytest-randomly) and [pytest-xdist](https://pytest-xdist.readthedocs.io/en/stable/)
- [uv dependency groups](https://docs.astral.sh/uv/concepts/projects/dependencies/) and [locked syncing](https://docs.astral.sh/uv/concepts/projects/sync/)
