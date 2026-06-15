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

## Références

- [Roadmap complète](docs/roadmap.md)
- [Phase 0 — Initialisation du projet](docs/phase0_init.md)
- [Phase 1 — Projet & Éditeur de graphe](docs/phase1_project_graph.md)
- [Phase 2 — Génération PyTorch & Entraînement](docs/phase2_pytorch_training.md)
- [Phase 3 — Système de versioning](docs/phase3_versioning.md)
- [Phase 4 — Monitoring live du graphe](docs/phase4_live_monitoring.md)
- [Phase 5 — Exécution distante](docs/phase5_remote_execution.md)
