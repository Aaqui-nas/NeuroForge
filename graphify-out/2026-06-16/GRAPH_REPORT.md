# Graph Report - .  (2026-06-15)

## Corpus Check
- Corpus is ~8,053 words - fits in a single context window. You may not need a graph.

## Summary
- 144 nodes · 155 edges · 34 communities (29 shown, 5 thin omitted)
- Extraction: 75% EXTRACTED · 25% INFERRED · 0% AMBIGUOUS · INFERRED: 39 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

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

## God Nodes (most connected - your core abstractions)
1. `NeuroForge — CLAUDE.md` - 12 edges
2. `Graph (DAG model)` - 10 edges
3. `API Reference index` - 8 edges
4. `ObjectStore C++ (Content-Addressable)` - 8 edges
5. `NeuroForge README` - 6 edges
6. `GraphScene (QGraphicsScene)` - 6 edges
7. `PyTorch Code Generator (Graph → nn.Module)` - 6 edges
8. `NeuroForgeObject (ABC)` - 6 edges
9. `RunObject` - 6 edges
10. `C++ lock-free ring buffer metrics module` - 5 edges

## Surprising Connections (you probably didn't know these)
- `NeuroForge Vision & Core Principles` --conceptually_related_to--> `ObjectStore C++ (Content-Addressable)`  [INFERRED]
  idea.md → docs/dev/phase3_versioning.md
- `Experiment Versioning (content-addressable object store, Git-inspired)` --conceptually_related_to--> `Python storage module (C++ storage wrapper)`  [INFERRED]
  README.md → CLAUDE.md
- `src/cpp/metrics CMake subdirectory` --conceptually_related_to--> `C++ lock-free ring buffer metrics module`  [INFERRED]
  CMakeLists.txt → CLAUDE.md
- `NeuroForge Vision & Core Principles` --conceptually_related_to--> `GraphScene (QGraphicsScene)`  [INFERRED]
  idea.md → docs/dev/phase1_project_graph.md
- `Google Test v1.14.0 (FetchContent dependency)` --conceptually_related_to--> `C++ Stack (C++17, pybind11, CMake, Google Test)`  [INFERRED]
  CMakeLists.txt → CLAUDE.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **NeuroForge Python Package Modules** — claude_md_core_module, claude_md_graph_module, claude_md_training_module, claude_md_datasets_module, claude_md_tracking_module, claude_md_storage_module, claude_md_visualization_module, claude_md_ui_module [EXTRACTED 1.00]
- **C++ Performance Modules (storage + metrics via pybind11)** — cmakelists_cpp_storage_subdir, cmakelists_cpp_metrics_subdir, cmakelists_pybind11_dep [EXTRACTED 1.00]
- **Phase 0 Toolchain Setup (Python + C++ + tests + linting)** — dev_phase0_python_tooling, dev_phase0_cpp_setup, dev_phase0_test_pipeline, dev_phase0_linting_typing [EXTRACTED 1.00]
- **Immutable Object Hierarchy in Content-Addressable Store** — dev_phase3_versioning_objectstore, dev_phase3_versioning_neuroforgeobject, dev_phase3_versioning_graphobject, dev_phase3_versioning_architectureobject, dev_phase3_versioning_checkpointobject, dev_phase3_versioning_runobject, dev_phase3_versioning_experimentobject, dev_phase3_versioning_snapshot [EXTRACTED 1.00]
- **Training IPC Pipeline (Worker → Queue → Controller → UI)** — dev_phase2_pytorch_training_trainingworker, dev_phase2_pytorch_training_metricsemitter, dev_phase2_pytorch_training_trainingmessage, dev_phase2_pytorch_training_trainingcontroller, dev_phase4_live_monitoring_hookmanager, dev_phase4_live_monitoring_ringbuffer, dev_phase4_live_monitoring_live_graph_update [INFERRED 0.85]
- **Graph Editor MVC Architecture** — dev_phase1_project_graph_graph, dev_phase1_project_graph_graphscene, dev_phase1_project_graph_graphview, dev_phase1_project_graph_nodeitem, dev_phase1_project_graph_edgeitem, dev_phase1_project_graph_command_pattern [EXTRACTED 1.00]

## Communities (34 total, 5 thin omitted)

### Community 0 - "Project Docs & API Reference"
Cohesion: 0.11
Nodes (28): neuroforge.core API doc, neuroforge.datasets API doc, neuroforge.graph API doc (nodes, ports, edges, validation), API Reference index, neuroforge.tracking API doc (experiment tracking, runs, metrics), neuroforge.training API doc (PyTorch codegen, engine, IPC), neuroforge.ui API doc (Qt widgets, graph editor, panels), neuroforge.visualization API doc (+20 more)

### Community 1 - "C++ Stack & Storage Layer"
Cohesion: 0.13
Nodes (18): neuroforge.storage API doc (C++ backend), C++ Performance Rationale (storage: intensive hashing; metrics: real-time IPC), C++ Stack (C++17, pybind11, CMake, Google Test), Python storage module (C++ storage wrapper), src/cpp/storage CMake subdirectory, Google Test v1.14.0 (FetchContent dependency), CMakeLists.txt — neuroforge_cpp project, pybind11 v2.12.0 (FetchContent dependency) (+10 more)

### Community 2 - "Graph Data Model"
Cohesion: 0.14
Nodes (18): ComponentDefinition (Subgraph), DFS Colored Cycle Detection, Edge, Graph (DAG model), Graph Serialization (JSON), Graph Validator, Node, Port (+10 more)

### Community 3 - "Training Engine & Metrics IPC"
Cohesion: 0.14
Nodes (15): _metrics pybind11 CMake Target, MetricsEmitter, TrainingController, TrainingMessage (IPC Queue), TrainingWorker (subprocess), Forking (Resume from Checkpoint), HookManager (PyTorch Hooks), RingBuffer C++ (Lock-Free SPSC) (+7 more)

### Community 4 - "Training Config & Experiment Objects"
Cohesion: 0.29
Nodes (11): DatasetConfig, Run (Experiment Tracking), TrainingConfig, ArchitectureObject, CheckpointObject, ExperimentObject, GraphObject, NeuroForgeObject (ABC) (+3 more)

### Community 5 - "Content-Addressable Object Store"
Cohesion: 0.25
Nodes (9): _storage pybind11 CMake Target, C++ Tests CMake (placeholder), BranchManager, ObjectStore C++ (Content-Addressable), Snapshot, Storage Layout (.neuroforge/), Remote Checkpoint Transfer, Phase 3 — Versioning System (+1 more)

### Community 6 - "Graph Editor UI & Live Monitoring"
Cohesion: 0.33
Nodes (7): EdgeItem (Bezier curve), GraphScene (QGraphicsScene), GraphView (QGraphicsView), NodeItem (QGraphicsItem), Live Graph Qt Update, NodeInspector (QDockWidget), NeuroForge Vision & Core Principles

### Community 7 - "C++ Metrics Bindings"
Cohesion: 0.50
Nodes (3): _metrics, PYBIND11_MODULE(), m

### Community 8 - "Test Infrastructure"
Cohesion: 0.50
Nodes (3): Path, Temporary directory simulating a NeuroForge project root., tmp_project_dir()

### Community 9 - "C++ Storage Bindings"
Cohesion: 0.50
Nodes (3): m, _storage, PYBIND11_MODULE()

## Knowledge Gaps
- **37 isolated node(s):** `_metrics`, `m`, `_storage`, `m`, `Path` (+32 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Graph (DAG model)` connect `Graph Data Model` to `Training Config & Experiment Objects`, `Graph Editor UI & Live Monitoring`?**
  _High betweenness centrality (0.075) - this node is a cross-community bridge._
- **Why does `NeuroForge — CLAUDE.md` connect `Project Docs & API Reference` to `C++ Stack & Storage Layer`?**
  _High betweenness centrality (0.055) - this node is a cross-community bridge._
- **Why does `ObjectStore C++ (Content-Addressable)` connect `Content-Addressable Object Store` to `Training Engine & Metrics IPC`, `Training Config & Experiment Objects`, `Graph Editor UI & Live Monitoring`?**
  _High betweenness centrality (0.052) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `ObjectStore C++ (Content-Addressable)` (e.g. with `NeuroForgeObject (ABC)` and `NeuroForge Vision & Core Principles`) actually correct?**
  _`ObjectStore C++ (Content-Addressable)` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `_metrics`, `m`, `_storage` to the rest of the system?**
  _42 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Project Docs & API Reference` be split into smaller, more focused modules?**
  _Cohesion score 0.10846560846560846 - nodes in this community are weakly interconnected._
- **Should `C++ Stack & Storage Layer` be split into smaller, more focused modules?**
  _Cohesion score 0.13071895424836602 - nodes in this community are weakly interconnected._
