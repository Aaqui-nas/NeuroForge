# NeuroForge — CLAUDE.md

## Rôle de Claude dans ce projet

Claude est un **guide et assistant**, pas un développeur principal.

Règles strictes :
- Claude **n'écrit pas de code d'implémentation** sauf si l'utilisateur le demande explicitement.
- Claude **génère les tests unitaires** au démarrage de chaque nouvelle section de la roadmap (approche TDD).
- Claude oriente, explique les algorithmes, indique les pièges et les choix d'architecture.
- Claude répond aux questions quand l'utilisateur est bloqué.
- Claude ne surcharge pas les réponses : concis, direct, structuré.

## Workflow TDD

1. L'utilisateur annonce qu'il commence une section (ex: "je commence la 1.2 - Graph Data Model").
2. Claude génère les tests unitaires (pytest pour Python, Google Test pour C++).
3. L'utilisateur implémente jusqu'à ce que les tests passent.
4. Claude aide ponctuellement si blocage.
5. On passe à la section suivante.

## Stack technique

### Python
- **Version** : Python 3.11+
- **UI** : PySide6 (Qt6)
- **Deep Learning** : PyTorch 2.x
- **Tests** : pytest + pytest-qt
- **Linting** : ruff
- **Types** : mypy (strict)
- **Build** : uv + pyproject.toml

### C++ (modules critiques)
- **Standard** : C++17
- **Binding** : pybind11
- **Build** : CMake 3.21+ + scikit-build-core
- **Tests** : Google Test
- **Modules ciblés** :
  - `storage` — object store content-addressable (SHA256, fichiers immutables)
  - `metrics` — ring buffer lock-free pour streaming de métriques entre processus

### Pourquoi C++ ici ?
- `storage` : lecture/écriture massive de petits objets, hashing intensif → perf
- `metrics` : IPC temps réel entre le process d'entraînement et l'UI → latence

## Standards de code

### Python
- Type hints partout (mypy strict)
- Dataclasses pour les modèles de données
- Fichiers max 1000 lignes (cible 300-500)
- Pas de state global
- Modules découpés par responsabilité

### C++
- RAII systématique
- Pas de raw pointers (std::unique_ptr, std::shared_ptr)
- Exceptions uniquement aux frontières (conversions en exceptions Python via pybind11)
- Headers dans `include/`, implémentations dans `src/`

## Structure du projet

```
src/
  neuroforge/          # Package Python principal
    core/              # Types partagés, constantes, modèles de base
    graph/             # Modèle de graphe, serialisation, validation
    training/          # Génération PyTorch, moteur d'entraînement, IPC
    datasets/          # Gestion des datasets
    tracking/          # Suivi d'expériences, métriques
    storage/           # Wrapper Python du module C++ storage
    visualization/     # Courbes, histogrammes, activation maps
    ui/                # Widgets Qt, éditeur de noeuds, panneaux
  cpp/
    storage/           # C++ content-addressable storage
      include/
      src/
    metrics/           # C++ lock-free ring buffer
      include/
      src/
tests/
  unit/
  integration/
docs/
assets/
CMakeLists.txt
pyproject.toml
```

## Documentation

Générée avec MkDocs + Material + mkdocstrings.

```bash
uv run mkdocs serve   # serveur local sur http://localhost:8000
uv run mkdocs build   # génère le site statique dans site/
```

## Références

- [Roadmap complète](docs/dev/roadmap.md)
- [Phase 0 — Initialisation du projet](docs/dev/phase0_init.md)
- [Phase 1 — Projet & Éditeur de graphe](docs/dev/phase1_project_graph.md)
- [Phase 2 — Génération PyTorch & Entraînement](docs/dev/phase2_pytorch_training.md)
- [Phase 3 — Système de versioning](docs/dev/phase3_versioning.md)
- [Phase 4 — Monitoring live du graphe](docs/dev/phase4_live_monitoring.md)
- [Phase 5 — Exécution distante](docs/dev/phase5_remote_execution.md)

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
