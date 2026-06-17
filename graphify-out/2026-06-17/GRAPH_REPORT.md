# Graph Report - NeuroForge  (2026-06-17)

## Corpus Check
- 67 files · ~16,464 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 740 nodes · 1277 edges · 62 communities (49 shown, 13 thin omitted)
- Extraction: 77% EXTRACTED · 23% INFERRED · 0% AMBIGUOUS · INFERRED: 290 edges (avg confidence: 0.59)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `b8aad3cd`
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
- [[_COMMUNITY_Community 55|Community 55]]
- [[_COMMUNITY_Community 56|Community 56]]
- [[_COMMUNITY_Community 57|Community 57]]
- [[_COMMUNITY_Community 58|Community 58]]
- [[_COMMUNITY_Community 59|Community 59]]
- [[_COMMUNITY_Community 60|Community 60]]
- [[_COMMUNITY_Community 61|Community 61]]

## God Nodes (most connected - your core abstractions)
1. `Graph` - 80 edges
2. `Edge` - 48 edges
3. `Node` - 46 edges
4. `GraphSerializer` - 40 edges
5. `GraphValidator` - 38 edges
6. `NodeRegistry` - 28 edges
7. `Port` - 26 edges
8. `make_node()` - 22 edges
9. `Graph` - 22 edges
10. `GraphScene` - 20 edges

## Surprising Connections (you probably didn't know these)
- `Edge` --uses--> `ValidationError`  [INFERRED]
  tests/unit/test_graph_validator.py → src/neuroforge/graph/validator.py
- `Node` --uses--> `ValidationError`  [INFERRED]
  tests/unit/test_graph_validator.py → src/neuroforge/graph/validator.py
- `Port` --uses--> `ValidationError`  [INFERRED]
  tests/unit/test_graph_validator.py → src/neuroforge/graph/validator.py
- `PortDirection` --uses--> `ValidationError`  [INFERRED]
  tests/unit/test_graph_validator.py → src/neuroforge/graph/validator.py
- `Edge` --uses--> `GraphValidator`  [INFERRED]
  tests/unit/test_graph_validator.py → src/neuroforge/graph/validator.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **NeuroForge Python Package Modules** — claude_md_core_module, claude_md_graph_module, claude_md_training_module, claude_md_datasets_module, claude_md_tracking_module, claude_md_storage_module, claude_md_visualization_module, claude_md_ui_module [EXTRACTED 1.00]
- **C++ Performance Modules (storage + metrics via pybind11)** — cmakelists_cpp_storage_subdir, cmakelists_cpp_metrics_subdir, cmakelists_pybind11_dep [EXTRACTED 1.00]
- **Phase 0 Toolchain Setup (Python + C++ + tests + linting)** — dev_phase0_python_tooling, dev_phase0_cpp_setup, dev_phase0_test_pipeline, dev_phase0_linting_typing [EXTRACTED 1.00]
- **Immutable Object Hierarchy in Content-Addressable Store** — dev_phase3_versioning_objectstore, dev_phase3_versioning_neuroforgeobject, dev_phase3_versioning_graphobject, dev_phase3_versioning_architectureobject, dev_phase3_versioning_checkpointobject, dev_phase3_versioning_runobject, dev_phase3_versioning_experimentobject, dev_phase3_versioning_snapshot [EXTRACTED 1.00]
- **Training IPC Pipeline (Worker → Queue → Controller → UI)** — dev_phase2_pytorch_training_trainingworker, dev_phase2_pytorch_training_metricsemitter, dev_phase2_pytorch_training_trainingmessage, dev_phase2_pytorch_training_trainingcontroller, dev_phase4_live_monitoring_hookmanager, dev_phase4_live_monitoring_ringbuffer, dev_phase4_live_monitoring_live_graph_update [INFERRED 0.85]
- **Graph Editor MVC Architecture** — dev_phase1_project_graph_graph, dev_phase1_project_graph_graphscene, dev_phase1_project_graph_graphview, dev_phase1_project_graph_nodeitem, dev_phase1_project_graph_edgeitem, dev_phase1_project_graph_command_pattern [EXTRACTED 1.00]

## Communities (62 total, 13 thin omitted)

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
Cohesion: 0.10
Nodes (9): ABC, AddEdgeCommand, AddNodeCommand, Command, GroupNodesCommand, MacroCommand, RemoveEdgeCommand, UpdateParamCommand (+1 more)

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
Cohesion: 0.17
Nodes (19): Edge, Edge, Node, Port, A typed connection point on a node.      Attributes:         id: Unique identifi, A single operation in the computation graph.      Attributes:         id: UUID s, A directed connection between two ports.      Attributes:         id: UUID strin, Node (+11 more)

### Community 38 - "Community 38"
Cohesion: 0.08
Nodes (35): Project, ProjectConfig, Return the directory where graph JSON files are stored., Return the directory where component JSON files are stored., Immutable metadata for a NeuroForge project.      Attributes:         name: Huma, A NeuroForge project, backed by a directory on disk.      The project directory, Create a new in-memory project (does not write to disk).          Args:, Load a project from an existing directory.          Args:             root: Path (+27 more)

### Community 39 - "Community 39"
Cohesion: 0.50
Nodes (3): main(), MainWindow, QMainWindow

### Community 42 - "Community 42"
Cohesion: 0.25
Nodes (7): commands, components, model, neuroforge.graph, registry, serializer, validator

### Community 47 - "Community 47"
Cohesion: 0.40
Nodes (4): graph_editor.items, graph_editor.scene, graph_editor.view, neuroforge.ui

### Community 50 - "Community 50"
Cohesion: 0.09
Nodes (9): GraphScene, GraphView, GraphScene, QGraphicsScene, QGraphicsView, QMouseEvent, QWheelEvent, Graph (+1 more)

### Community 52 - "Community 52"
Cohesion: 0.08
Nodes (45): EdgeId, Graph, Add a node to the graph. Silently ignored if the id already exists.          Arg, Remove a node and all edges that reference it.          Args:             node_i, Add an edge to the graph. Silently ignored if the id already exists.          Ar, Remove an edge. No-op if the edge does not exist.          Args:             edg, Return the node for the given id, or None if not found.          Args:, Return the edge for the given id, or None if not found.          Args: (+37 more)

### Community 53 - "Community 53"
Cohesion: 0.11
Nodes (47): GraphValidator, Detect cycles using Kahn's algorithm (via `Graph.topological_order`)., A single validation rule violation.      Attributes:         code: Machine-reada, Verify that connected ports carry compatible data types.          `DataType.ANY`, Verify that every required INPUT port has at least one incoming edge., Verify that no INPUT port receives more than one incoming edge., Outcome of a full graph validation pass.      Attributes:         is_valid: True, Return True if a value of *src* type can flow into a *dst* port. (+39 more)

### Community 54 - "Community 54"
Cohesion: 0.09
Nodes (47): Any, GraphSerializer, Upgrade ``data`` from an older schema version to `SCHEMA_VERSION`.          Add, Recursively convert Enum → int and tuple → list for JSON compatibility., Serializes and deserializes a `Graph` to/from JSON.      The JSON file format in, Convert a `Graph` to a JSON-serializable dict.          Enum values are stored a, Reconstruct a `Graph` from a deserialized dict.          Calls `_migrate` automa, Write the graph to a JSON file.          Creates parent directories automaticall (+39 more)

### Community 56 - "Community 56"
Cohesion: 0.06
Nodes (28): Enum, DataType, PortDirection, Direction of a port on a node., Data type flowing through a port connection., build_default_registry(), NodeDefinition, NodeRegistry (+20 more)

### Community 57 - "Community 57"
Cohesion: 0.18
Nodes (5): NodeItem, PortItem, PortId, QGraphicsEllipseItem, QGraphicsSceneMouseEvent

### Community 58 - "Community 58"
Cohesion: 0.14
Nodes (7): MoveNodeCommand, RemoveNodeCommand, Any, Edge, Graph, Node, NodeId

### Community 59 - "Community 59"
Cohesion: 0.19
Nodes (5): EdgeDraftItem, EdgeItem, QGraphicsPathItem, QPointF, Edge

### Community 60 - "Community 60"
Cohesion: 0.31
Nodes (4): ComponentDefinition, ComponentLibrary, Graph, NodeId

## Knowledge Gaps
- **203 isolated node(s):** `DataType`, `Port`, `Node`, `Edge`, `Feat` (+198 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **13 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Graph` connect `Community 52` to `Training Config & Experiment Objects`, `Community 37`, `Community 50`, `Community 53`, `Community 54`, `Community 56`, `Community 58`, `Community 60`, `Community 61`?**
  _High betweenness centrality (0.116) - this node is a cross-community bridge._
- **Why does `GraphSerializer` connect `Community 54` to `Community 56`, `Community 52`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **Why does `PortDirection` connect `Community 56` to `Community 53`, `Community 52`, `Community 37`, `Community 54`?**
  _High betweenness centrality (0.039) - this node is a cross-community bridge._
- **Are the 65 inferred relationships involving `Graph` (e.g. with `Edge` and `AddEdgeCommand`) actually correct?**
  _`Graph` has 65 INFERRED edges - model-reasoned connections that need verification._
- **Are the 41 inferred relationships involving `Edge` (e.g. with `Edge` and `AddEdgeCommand`) actually correct?**
  _`Edge` has 41 INFERRED edges - model-reasoned connections that need verification._
- **Are the 41 inferred relationships involving `Node` (e.g. with `Edge` and `AddEdgeCommand`) actually correct?**
  _`Node` has 41 INFERRED edges - model-reasoned connections that need verification._
- **Are the 30 inferred relationships involving `GraphSerializer` (e.g. with `Graph` and `PortDirection`) actually correct?**
  _`GraphSerializer` has 30 INFERRED edges - model-reasoned connections that need verification._