# Graph Report - NeuroForge  (2026-06-17)

## Corpus Check
- 61 files · ~11,904 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 540 nodes · 815 edges · 55 communities (42 shown, 13 thin omitted)
- Extraction: 75% EXTRACTED · 25% INFERRED · 0% AMBIGUOUS · INFERRED: 201 edges (avg confidence: 0.51)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `16158abb`
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
- [[_COMMUNITY_Community 52|Community 52]]
- [[_COMMUNITY_Community 53|Community 53]]
- [[_COMMUNITY_Community 54|Community 54]]

## God Nodes (most connected - your core abstractions)
1. `Graph` - 48 edges
2. `Edge` - 44 edges
3. `Node` - 42 edges
4. `NodeId` - 35 edges
5. `EdgeId` - 29 edges
6. `Port` - 22 edges
7. `GraphScene` - 22 edges
8. `Command` - 19 edges
9. `NodeItem` - 18 edges
10. `GraphView` - 14 edges

## Surprising Connections (you probably didn't know these)
- `Path` --uses--> `ProjectConfig`  [INFERRED]
  tests/unit/test_project.py → src/neuroforge/core/project.py
- `test_project_config_default_format_version()` --calls--> `ProjectConfig`  [INFERRED]
  tests/unit/test_project.py → src/neuroforge/core/project.py
- `test_project_config_is_frozen()` --calls--> `ProjectConfig`  [INFERRED]
  tests/unit/test_project.py → src/neuroforge/core/project.py
- `Path` --uses--> `Project`  [INFERRED]
  tests/unit/test_project.py → src/neuroforge/core/project.py
- `ComponentDefinition` --uses--> `Graph`  [INFERRED]
  src/neuroforge/graph/components.py → src/neuroforge/graph/model.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **NeuroForge Python Package Modules** — claude_md_core_module, claude_md_graph_module, claude_md_training_module, claude_md_datasets_module, claude_md_tracking_module, claude_md_storage_module, claude_md_visualization_module, claude_md_ui_module [EXTRACTED 1.00]
- **C++ Performance Modules (storage + metrics via pybind11)** — cmakelists_cpp_storage_subdir, cmakelists_cpp_metrics_subdir, cmakelists_pybind11_dep [EXTRACTED 1.00]
- **Phase 0 Toolchain Setup (Python + C++ + tests + linting)** — dev_phase0_python_tooling, dev_phase0_cpp_setup, dev_phase0_test_pipeline, dev_phase0_linting_typing [EXTRACTED 1.00]
- **Immutable Object Hierarchy in Content-Addressable Store** — dev_phase3_versioning_objectstore, dev_phase3_versioning_neuroforgeobject, dev_phase3_versioning_graphobject, dev_phase3_versioning_architectureobject, dev_phase3_versioning_checkpointobject, dev_phase3_versioning_runobject, dev_phase3_versioning_experimentobject, dev_phase3_versioning_snapshot [EXTRACTED 1.00]
- **Training IPC Pipeline (Worker → Queue → Controller → UI)** — dev_phase2_pytorch_training_trainingworker, dev_phase2_pytorch_training_metricsemitter, dev_phase2_pytorch_training_trainingmessage, dev_phase2_pytorch_training_trainingcontroller, dev_phase4_live_monitoring_hookmanager, dev_phase4_live_monitoring_ringbuffer, dev_phase4_live_monitoring_live_graph_update [INFERRED 0.85]
- **Graph Editor MVC Architecture** — dev_phase1_project_graph_graph, dev_phase1_project_graph_graphscene, dev_phase1_project_graph_graphview, dev_phase1_project_graph_nodeitem, dev_phase1_project_graph_edgeitem, dev_phase1_project_graph_command_pattern [EXTRACTED 1.00]

## Communities (55 total, 13 thin omitted)

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
Cohesion: 0.08
Nodes (26): ABC, AddEdgeCommand, AddNodeCommand, Command, CommandHistory, GroupNodesCommand, MacroCommand, MoveNodeCommand (+18 more)

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
Cohesion: 0.06
Nodes (31): 2.1 — Inférence de shapes, 2.2 — Générateur de code PyTorch, 2.3 — Gestionnaire de datasets, 2.4 — Configuration d'entraînement, 2.5 — Moteur d'entraînement, 2.6 — Suivi d'expériences, Algorithme, Algorithme (+23 more)

### Community 11 - "Project Model"
Cohesion: 0.05
Nodes (39): 1.1 — Modèle de projet, 1.2 — Modèle de graphe, 1.3 — Sérialisation du graphe, 1.4 — Validation du graphe, 1.5 — Éditeur de graphe UI, 1.6 — Bibliothèque de noeuds, 1.7 — Undo/Redo, 1.8 — Subgraphs & composants réutilisables (+31 more)

### Community 12 - "Command Pattern"
Cohesion: 0.08
Nodes (24): 3.1 — Object Store C++ (content-addressable), 3.2 — Modèles d'objets immuables, 3.3 — Layout de stockage, 3.4 — Snapshots, 3.5 — Branches et refs, 3.6 — Forking, Algorithme, Algorithme de création (+16 more)

### Community 13 - "Remote Profiling"
Cohesion: 0.05
Nodes (37): 4.1 — Hooks PyTorch, 4.2 — Ring Buffer C++ pour streaming de métriques, 4.3 — Mise à jour live du graphe Qt, 4.4 — Inspecteur de noeuds, 4.5 — Panneaux de visualisation, Activation maps (Conv2d), Architecture de mise à jour, Binding pybind11 (+29 more)

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
Cohesion: 0.07
Nodes (23): ComponentDefinition, ComponentLibrary, EdgeDraftItem, EdgeItem, NodeItem, PortItem, Port, Port (+15 more)

### Community 38 - "Community 38"
Cohesion: 0.08
Nodes (35): Project, ProjectConfig, Return the directory where graph JSON files are stored., Return the directory where component JSON files are stored., Immutable metadata for a NeuroForge project.      Attributes:         name: Huma, A NeuroForge project, backed by a directory on disk.      The project directory, Create a new in-memory project (does not write to disk).          Args:, Load a project from an existing directory.          Args:             root: Path (+27 more)

### Community 39 - "Community 39"
Cohesion: 0.50
Nodes (3): main(), MainWindow, QMainWindow

### Community 50 - "Community 50"
Cohesion: 0.09
Nodes (8): GraphScene, GraphView, GraphScene, QGraphicsScene, QGraphicsView, QMouseEvent, QWheelEvent, NodeId

### Community 52 - "Community 52"
Cohesion: 0.31
Nodes (7): Enum, DataType, PortDirection, build_default_registry(), NodeDefinition, NodeRegistry, PortDefinition

### Community 53 - "Community 53"
Cohesion: 0.38
Nodes (4): GraphValidator, ValidationError, ValidationResult, Graph

### Community 54 - "Community 54"
Cohesion: 0.33
Nodes (4): GraphSerializer, Any, Graph, Path

## Knowledge Gaps
- **191 isolated node(s):** `What is NeuroForge?`, `Navigation`, `CI Reports`, `Rôle de Claude dans ce projet`, `Workflow TDD` (+186 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **13 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Graph` connect `Training Config & Experiment Objects` to `Community 37`, `Community 50`, `Community 52`, `Community 53`, `Community 54`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **Why does `GraphScene` connect `Community 50` to `Training Config & Experiment Objects`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Why does `Edge` connect `Training Config & Experiment Objects` to `Community 50`, `Community 52`, `Community 37`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Are the 34 inferred relationships involving `Graph` (e.g. with `AddEdgeCommand` and `AddNodeCommand`) actually correct?**
  _`Graph` has 34 INFERRED edges - model-reasoned connections that need verification._
- **Are the 38 inferred relationships involving `Edge` (e.g. with `AddEdgeCommand` and `AddNodeCommand`) actually correct?**
  _`Edge` has 38 INFERRED edges - model-reasoned connections that need verification._
- **Are the 38 inferred relationships involving `Node` (e.g. with `AddEdgeCommand` and `AddNodeCommand`) actually correct?**
  _`Node` has 38 INFERRED edges - model-reasoned connections that need verification._
- **Are the 30 inferred relationships involving `NodeId` (e.g. with `AddEdgeCommand` and `AddNodeCommand`) actually correct?**
  _`NodeId` has 30 INFERRED edges - model-reasoned connections that need verification._