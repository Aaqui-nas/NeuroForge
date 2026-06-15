# Contributing

## Workflow

This project uses **TDD (Test-Driven Development)**.

1. Before implementing any feature, tests are written first.
2. Implementation continues until all tests pass.
3. Refactor if needed, keeping tests green.

## Commit convention

```
feat: add node serialization
fix: correct edge direction validation
chore: update CMakeLists for storage module
docs: document Graph.validate()
test: add shape inference tests for Conv2d
```

## Code standards

### Python

- Type hints on every function signature
- Docstrings on every public class and method (Google style)
- `ruff check` must pass with zero warnings
- `mypy --strict` must pass

### C++

- Every public function documented with Doxygen comments
- RAII for all resources
- No raw owning pointers
- `clang-format` applied before commit

## Running checks

```bash
# Python
uv run ruff check src/ tests/
uv run mypy src/
uv run pytest

# C++
cd build && ctest --output-on-failure
```
