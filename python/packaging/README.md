# Packaging and environments: example-first conventions

Start with the [installable sample project](examples/sample_project/README.md). It defines the preferred `src/` layout, `pyproject.toml` configuration, command-line entry point, and typed public API.

- **MUST:** Use `uv` for dependencies. Define direct runtime dependencies in `[project]` and development tools in `[dependency-groups]`.
- **SHOULD:** Use `src/` and `[build-system]` for shared code or an application with an executable command. Keep the CLI as a thin wrapper around importable logic.
- **MUST:** Do not modify `sys.path` in production code to make package imports work.
- **MUST:** Keep executable application `uv.lock` files in version control; use `uv sync --locked` in CI. Libraries MAY also commit a lockfile for development reproducibility, but a consumer resolves its own dependencies.
- **MUST NOT:** Commit `.venv/`, cache directories, or build output.
- **MAY:** Use `uv run file.py` without packaging for a truly standalone script.

See [uv project layouts](https://docs.astral.sh/uv/concepts/projects/init/) and [uv build backend](https://docs.astral.sh/uv/concepts/build-backend/).
