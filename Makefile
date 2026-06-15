.PHONY: install test lint type-check fmt docs build clean

install:
	uv sync --group dev
	uv run pre-commit install --hook-type pre-commit --hook-type commit-msg

test:
	uv run pytest --tb=short -q

cov:
	uv run pytest --cov --cov-report=term-missing --cov-report=html:htmlcov -q
	@echo "Coverage report: htmlcov/index.html"

lint:
	uv run ruff check src/ tests/
	uv run ruff format --check src/ tests/

fmt:
	uv run ruff check --fix src/ tests/
	uv run ruff format src/ tests/

type-check:
	uv run mypy src/

check: lint type-check test

build-cpp:
	cmake -B build -S . -DCMAKE_BUILD_TYPE=Release
	cmake --build build --parallel

docs:
	uv run mkdocs serve

docs-build:
	uv run mkdocs build

bump:
	uv run cz bump

changelog:
	uv run cz changelog

clean:
	rm -rf build/ site/ reports/ htmlcov/ .pytest_cache/ .mypy_cache/ .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
