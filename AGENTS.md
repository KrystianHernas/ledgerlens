# AGENTS.md — ledgerlens

## Commands
- **Build**: `uv build` (via pyproject.toml build-system)
- **Test**: `uv run pytest` (testpaths: `tests`, pythonpath: `src`)
- **Lint**: `uv run ruff check .` && `uv run mypy .` (strict=true)
- **Run**: `uv run ledgerlens` (entrypoint: `ledgerlens:main`)

## Structure
```
src/ledgerlens/     # package source
tests/              # pytest tests
.venv/              # virtualenv (uv)
```

## Conventions
- Python ≥3.12, type hints required (mypy strict)
- Ruff for formatting/linting (line-length default)
- Tests in `tests/`, import via `src/` layout

## Env
- Virtualenv: `.venv/` (managed by uv)
- No external services required