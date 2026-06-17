# Graph Report - NeuroForge  (2026-06-16)

## Corpus Check
- 49 files · ~9,933 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 311 nodes · 267 edges · 52 communities (39 shown, 13 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS · INFERRED: 1 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ce24c970`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Project Docs & API Reference|Project Docs & API Reference]]
- [[_COMMUNITY_C++ Stack & Storage Layer|C++ Stack & Storage Layer]]
- [[_COMMUNITY_Graph Data Model|Graph Data Model]]
- [[_COMMUNITY_Training Engine & Metrics IPC|Training Engine & Metrics IPC]]
- [[_COMMUNITY_Training Config & Experiment Objects|Training Config & Experiment Objects]]
- [[_COMMUNITY_Content-Addressable Object Store|Content-Addressable Object Store]]
- [[_COMMUNITY_Graph Editor UI & Live Monitoring|Graph Editor UI & Live Monitoring]]
- [[_COMMUNITY_C++ Metrics Bindings|C++ Metrics Bindings]]
- [[_COMMUNITY_Test Infrastructure|Test Infrastructure]]
- [[_COMMUNITY_C++ Storage Bindings|C++ Storage Bindings]]
- [[_COMMUNITY_Node Registry|Node Registry]]
- [[_COMMUNITY_Project Model|Project Model]]
- [[_COMMUNITY_Command Pattern|Command Pattern]]
- [[_COMMUNITY_Remote Profiling|Remote Profiling]]
- [[_COMMUNITY_Roadmap Phase 0|Roadmap Phase 0]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 35|Community 35]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 39|Community 39]]
- [[_COMMUNITY_Community 40|Community 40]]
- [[_COMMUNITY_Community 41|Community 41]]
- [[_COMMUNITY_Community 42|Community 42]]
- [[_COMMUNITY_Community 43|Community 43]]
- [[_COMMUNITY_Community 44|Community 44]]
- [[_COMMUNITY_Community 45|Community 45]]
- [[_COMMUNITY_Community 46|Community 46]]
- [[_COMMUNITY_Community 47|Community 47]]
- [[_COMMUNITY_Community 48|Community 48]]
- [[_COMMUNITY_Community 49|Community 49]]
- [[_COMMUNITY_Community 50|Community 50]]
- [[_COMMUNITY_Community 51|Community 51]]

## God Nodes (most connected - your core abstractions)
1. `NeuroForge — CLAUDE.md` - 9 edges
2. `Phase 1 — Projet & Éditeur de graphe` - 9 edges
3. `NeuroForge` - 8 edges
4. `NeuroForge — Roadmap` - 8 edges
5. `Phase 2 — Génération PyTorch & Entraînement` - 7 edges
6. `2.2 — Générateur de code PyTorch` - 7 edges
7. `Phase 3 — Système de versioning` - 7 edges
8. `3.1 — Object Store C++ (content-addressable)` - 7 edges
9. `4.2 — Ring Buffer C++ pour streaming de métriques` - 7 edges
10. `Core Concepts` - 7 edges

## Surprising Connections (you probably didn't know these)
- `tmp_project_dir()` --references--> `Path`  [EXTRACTED]
  tests/conftest.py → scripts/theme_reports.py
- `C++ Tests CMake (placeholder)` --references--> `_storage pybind11 CMake Target`  [EXTRACTED]
  tests/cpp/CMakeLists.txt → src/cpp/storage/CMakeLists.txt
- `NeuroForge` --references--> `Installation`  [EXTRACTED]
  docs/index.md → docs/guide/quickstart.md
- `Live Monitoring` --references--> `HookManager`  [EXTRACTED]
  docs/guide/concepts.md → docs/dev/phase4_live_monitoring.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **NeuroForge Python Package Modules** — claude_md_core_module, claude_md_graph_module, claude_md_training_module, claude_md_datasets_module, claude_md_tracking_module, claude_md_storage_module, claude_md_visualization_module, claude_md_ui_module [EXTRACTED 1.00]
- **C++ Performance Modules (storage + metrics via pybind11)** — cmakelists_cpp_storage_subdir, cmakelists_cpp_metrics_subdir, cmakelists_pybind11_dep [EXTRACTED 1.00]
- **Phase 0 Toolchain Setup (Python + C++ + tests + linting)** — dev_phase0_python_tooling, dev_phase0_cpp_setup, dev_phase0_test_pipeline, dev_phase0_linting_typing [EXTRACTED 1.00]
- **Immutable Object Hierarchy in Content-Addressable Store** — dev_phase3_versioning_objectstore, dev_phase3_versioning_neuroforgeobject, dev_phase3_versioning_graphobject, dev_phase3_versioning_architectureobject, dev_phase3_versioning_checkpointobject, dev_phase3_versioning_runobject, dev_phase3_versioning_experimentobject, dev_phase3_versioning_snapshot [EXTRACTED 1.00]
- **Training IPC Pipeline (Worker → Queue → Controller → UI)** — dev_phase2_pytorch_training_trainingworker, dev_phase2_pytorch_training_metricsemitter, dev_phase2_pytorch_training_trainingmessage, dev_phase2_pytorch_training_trainingcontroller, dev_phase4_live_monitoring_hookmanager, dev_phase4_live_monitoring_ringbuffer, dev_phase4_live_monitoring_live_graph_update [INFERRED 0.85]
- **Graph Editor MVC Architecture** — dev_phase1_project_graph_graph, dev_phase1_project_graph_graphscene, dev_phase1_project_graph_graphview, dev_phase1_project_graph_nodeitem, dev_phase1_project_graph_edgeitem, dev_phase1_project_graph_command_pattern [EXTRACTED 1.00]

## Communities (52 total, 13 thin omitted)

### Community 0 - "Project Docs & API Reference"
Cohesion: 0.22
Nodes (8): Development, Documentation, Features, License, NeuroForge, Project Status, Quick Start, Stack

### Community 1 - "C++ Stack & Storage Layer"
Cohesion: 0.33
Nodes (6): src/cpp/metrics CMake subdirectory, src/cpp/storage CMake subdirectory, Google Test v1.14.0 (FetchContent dependency), CMakeLists.txt — neuroforge_cpp project, pybind11 v2.12.0 (FetchContent dependency), tests/cpp CMake subdirectory

### Community 2 - "Graph Data Model"
Cohesion: 0.12
Nodes (15): CI Reports, Navigation, NeuroForge, What is NeuroForge?, 1. Clone the repository, 2. Install Python dependencies, 3. Build C++ extensions, 4. Run (+7 more)

### Community 3 - "Training Engine & Metrics IPC"
Cohesion: 0.08
Nodes (25): 5.1 — Gestion des connexions SSH, 5.2 — Synchronisation de fichiers distante, 5.3 — Lancement d'entraînement distant et rapatriement de métriques, 5.4 — Transfert de checkpoints, 5.5 — Profiling avancé, Affichage dans NeuroForge, Algorithme de sync intelligente, Approche (+17 more)

### Community 4 - "Training Config & Experiment Objects"
Cohesion: 0.14
Nodes (13): 4.1 — Hooks PyTorch, HookManager, Métriques collectées par noeud, Objectif, Points d'attention, Types de hooks PyTorch, Core Concepts, Experiment Tracking (+5 more)

### Community 7 - "C++ Metrics Bindings"
Cohesion: 0.50
Nodes (3): _metrics, PYBIND11_MODULE(), m

### Community 8 - "Test Infrastructure"
Cohesion: 0.32
Nodes (6): Path, inject(), Inject the NeuroForge theme into generated HTML reports (htmlcov, graphify)., theme_directory(), Temporary directory simulating a NeuroForge project root., tmp_project_dir()

### Community 9 - "C++ Storage Bindings"
Cohesion: 0.50
Nodes (3): m, _storage, PYBIND11_MODULE()

### Community 10 - "Node Registry"
Cohesion: 0.08
Nodes (24): 2.1 — Inférence de shapes, 2.3 — Gestionnaire de datasets, 2.4 — Configuration d'entraînement, 2.5 — Moteur d'entraînement, 2.6 — Suivi d'expériences, Algorithme, Architecture IPC, Composants (+16 more)

### Community 11 - "Project Model"
Cohesion: 0.07
Nodes (29): 1.2 — Modèle de graphe, 1.3 — Sérialisation du graphe, 1.4 — Validation du graphe, 1.5 — Éditeur de graphe UI, 1.6 — Bibliothèque de noeuds, 1.7 — Undo/Redo, Algorithme clé : détection de cycle, Algorithme : courbe de Bézier pour les arêtes (+21 more)

### Community 12 - "Command Pattern"
Cohesion: 0.08
Nodes (24): 3.1 — Object Store C++ (content-addressable), 3.2 — Modèles d'objets immuables, 3.3 — Layout de stockage, 3.4 — Snapshots, 3.5 — Branches et refs, 3.6 — Forking, Algorithme, Algorithme de création (+16 more)

### Community 13 - "Remote Profiling"
Cohesion: 0.08
Nodes (24): 4.2 — Ring Buffer C++ pour streaming de métriques, 4.3 — Mise à jour live du graphe Qt, 4.4 — Inspecteur de noeuds, 4.5 — Panneaux de visualisation, Activation maps (Conv2d), Architecture de mise à jour, Binding pybind11, Concepts clés à maîtriser (+16 more)

### Community 14 - "Roadmap Phase 0"
Cohesion: 0.11
Nodes (18): 0.1 — Structure Python & tooling, 0.2 — Setup C++ (CMake + pybind11), 0.3 — Pipeline de tests, 0.4 — Linting et typage, C++ — Google Test, Commande de build, Concepts clés à maîtriser, Intégration dans pyproject.toml (+10 more)

### Community 34 - "Community 34"
Cohesion: 0.13
Nodes (14): C++, C++ (modules critiques), Documentation, graphify, NeuroForge — CLAUDE.md, Pourquoi C++ ici ?, Python, Python (+6 more)

### Community 35 - "Community 35"
Cohesion: 0.22
Nodes (8): NeuroForge — Roadmap, Phase 0 — Initialisation du projet, Phase 1 — Projet & Éditeur de graphe, Phase 2 — Génération PyTorch & Entraînement, Phase 3 — Système de versioning, Phase 4 — Monitoring live du graphe, Phase 5 — Exécution distante, Vue d'ensemble

### Community 36 - "Community 36"
Cohesion: 0.25
Nodes (7): C++, Code standards, Commit convention, Contributing, Python, Running checks, Workflow

### Community 37 - "Community 37"
Cohesion: 0.29
Nodes (7): 2.2 — Générateur de code PyTorch, Algorithme, Approche : génération de texte (string-based), Gestion des composants réutilisables, Objectif, Points d'attention, Template de sortie

### Community 38 - "Community 38"
Cohesion: 0.40
Nodes (5): 1.1 — Modèle de projet, Concepts, Objectif, Points d'attention, Sérialisation

### Community 39 - "Community 39"
Cohesion: 0.50
Nodes (3): main(), MainWindow, QMainWindow

### Community 50 - "Community 50"
Cohesion: 0.40
Nodes (5): 1.8 — Subgraphs & composants réutilisables, Algorithme de création d'un subgraph, Objectif, Points d'attention, Structure

## Knowledge Gaps
- **191 isolated node(s):** `What is NeuroForge?`, `Navigation`, `CI Reports`, `Rôle de Claude dans ce projet`, `Workflow TDD` (+186 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **13 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Phase 1 — Projet & Éditeur de graphe` connect `Project Model` to `Community 50`, `Community 38`?**
  _High betweenness centrality (0.014) - this node is a cross-community bridge._
- **Why does `Phase 4 — Monitoring live du graphe` connect `Remote Profiling` to `Training Config & Experiment Objects`?**
  _High betweenness centrality (0.012) - this node is a cross-community bridge._
- **Why does `Phase 2 — Génération PyTorch & Entraînement` connect `Node Registry` to `Community 37`?**
  _High betweenness centrality (0.008) - this node is a cross-community bridge._
- **What connects `Inject the NeuroForge theme into generated HTML reports (htmlcov, graphify).`, `What is NeuroForge?`, `Navigation` to the rest of the system?**
  _195 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Graph Data Model` be split into smaller, more focused modules?**
  _Cohesion score 0.11764705882352941 - nodes in this community are weakly interconnected._
- **Should `Training Engine & Metrics IPC` be split into smaller, more focused modules?**
  _Cohesion score 0.08 - nodes in this community are weakly interconnected._
- **Should `Training Config & Experiment Objects` be split into smaller, more focused modules?**
  _Cohesion score 0.14285714285714285 - nodes in this community are weakly interconnected._