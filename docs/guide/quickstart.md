# Quick Start

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- CMake 3.21+
- A C++17 compiler (GCC 11+, Clang 14+, MSVC 2022+)

## Installation

### 1. Clone the repository

```bash
git clone <repo-url>
cd NeuroForge
```

### 2. Install Python dependencies

```bash
uv sync
```

### 3. Build C++ extensions

```bash
cmake -B build -S . -DCMAKE_BUILD_TYPE=Release
cmake --build build
```

The two C++ extensions (`_storage`, `_metrics`) will be compiled and placed automatically inside the Python package.

### 4. Run

```bash
uv run python -m neuroforge
```

## Development setup

```bash
uv sync --extra dev
```

This adds pytest, ruff, mypy and mkdocs to your environment.

### Run the test suite

```bash
uv run pytest
```

### Run C++ tests

```bash
cmake --build build --target test
# or
cd build && ctest --output-on-failure
```

### Serve the documentation locally

```bash
uv run mkdocs serve
```
