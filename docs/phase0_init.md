# Phase 0 — Initialisation du projet

## 0.1 — Structure Python & tooling

### À faire
1. Créer `pyproject.toml` avec uv
2. Configurer ruff (linting + formatting)
3. Configurer mypy strict
4. Créer les `__init__.py` vides dans chaque sous-module
5. Vérifier que `python -m neuroforge` fonctionne

### Outils à installer
```
uv add pyside6 torch pytest pytest-qt
uv add --dev ruff mypy
```

### Points d'attention
- Utiliser `uv` (pas pip direct) pour la reproductibilité
- `src/` layout (src-layout) : le package `neuroforge` est dans `src/neuroforge/`, pas à la racine
- Cela évite les conflits d'import pendant les tests

---

## 0.2 — Setup C++ (CMake + pybind11)

### À faire
1. Créer `CMakeLists.txt` racine
2. Créer `CMakeLists.txt` pour `src/cpp/storage/` et `src/cpp/metrics/`
3. Intégrer pybind11 via FetchContent ou vcpkg
4. Configurer scikit-build-core pour packager les extensions C++ avec Python

### Concepts clés à maîtriser
- **FetchContent** : télécharge pybind11 au build time via CMake
- **scikit-build-core** : remplace setup.py pour les projets CMake/Python, s'intègre dans pyproject.toml
- **PYBIND11_MODULE** : macro pybind11 pour déclarer un module Python en C++

### Structure d'un binding minimal
```cpp
// src/cpp/storage/bindings.cpp
#include <pybind11/pybind11.h>
namespace py = pybind11;

PYBIND11_MODULE(_storage, m) {
    m.doc() = "NeuroForge storage C++ extension";
    // déclarations ici
}
```

### Commande de build
```bash
pip install scikit-build-core pybind11
cmake -B build -S . -DCMAKE_BUILD_TYPE=Release
cmake --build build
```

---

## 0.3 — Pipeline de tests

### Python — pytest
```
tests/unit/           # Tests unitaires par module
tests/integration/    # Tests d'intégration multi-modules
conftest.py           # Fixtures partagées
```

Lancer les tests :
```bash
pytest tests/ -v
```

### C++ — Google Test
- Intégrer GTest via CMake FetchContent
- Un binaire de test par module C++
- Les tests C++ tournent via `ctest` ou directement

### Intégration dans pyproject.toml
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
```

---

## 0.4 — Linting et typage

### ruff
```toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "SIM"]
```

### mypy
```toml
[tool.mypy]
python_version = "3.11"
strict = true
ignore_missing_imports = true
```

### Lancer les checks
```bash
ruff check src/ tests/
mypy src/
```
