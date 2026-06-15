# NeuroForge

A desktop application for visually designing, training, analyzing and versioning PyTorch neural networks.

Think Unreal Engine Blueprint — but for deep learning.

---

## Features

- **Visual graph editor** — build neural networks by connecting nodes, no code required
- **PyTorch native** — every node maps directly to a PyTorch module; training runs real PyTorch
- **Live graph monitoring** — nodes change color during training based on gradient magnitudes and activation norms
- **Experiment versioning** — content-addressable object store (inspired by Git) for architectures, checkpoints and datasets
- **Reusable components** — group any subgraph into a reusable block, nest them arbitrarily
- **Offline first** — no cloud dependency, everything runs locally

## Stack

| Layer | Technology |
|-------|-----------|
| UI | PySide6 (Qt6) |
| Deep learning | PyTorch 2.x |
| Performance modules | C++17 + pybind11 |
| Build | uv + CMake + scikit-build-core |

## Quick Start

```bash
# Install dependencies
uv sync

# Build C++ extensions
cmake -B build -S . -DCMAKE_BUILD_TYPE=Release
cmake --build build

# Run
uv run python -m neuroforge
```

## Development

```bash
# Install with dev extras
uv sync --extra dev

# Run tests
uv run pytest

# Lint
uv run ruff check src/ tests/

# Type check
uv run mypy src/
```

## Documentation

```bash
uv run mkdocs serve
```

Then open [http://localhost:8000](http://localhost:8000).

## Project Status

Early development — Phase 0 (project initialization) in progress.

See the [roadmap](docs/dev/roadmap.md) for the full plan.

## License

MIT
