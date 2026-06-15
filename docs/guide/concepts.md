# Core Concepts

## Graph and Nodes

The central abstraction in NeuroForge is the **graph** — a directed acyclic graph (DAG) of nodes connected by edges.

Each **node** represents a PyTorch operation:

- Layers: `Linear`, `Conv2d`, `MultiheadAttention`…
- Activations: `ReLU`, `GELU`, `Softmax`…
- Normalization: `BatchNorm2d`, `LayerNorm`…
- Utility: `Flatten`, `Reshape`, `Add` (residual)…

**Ports** are the connection points on nodes. An output port carries a tensor; an input port receives one. The graph is valid when all required input ports are connected and there are no cycles.

---

## PyTorch Generation

When you launch training, NeuroForge performs a **topological sort** of the graph and generates a `nn.Module` subclass. The generated code is plain, readable PyTorch — you can inspect it at any time.

**Shape inference** runs before code generation to catch incompatible connections early (e.g. a `Linear(128, 64)` connected to a `Linear(32, 10)` will raise an error before training starts).

---

## Reusable Components

Any selection of nodes can be **grouped** into a reusable component. The component exposes only the external connections as ports. Components can be nested.

This is analogous to functions in code, or custom nodes in Blender / Unreal Blueprint.

---

## Versioning

NeuroForge implements its own **content-addressable object store**, inspired by Git internals.

Every object — graph, architecture, hyperparameters, dataset split, checkpoint, metrics — is serialized and stored under `SHA256(content)`. Objects are **immutable**.

A **snapshot** ties all these objects together at a point in time (like a Git commit). Snapshots form a chain via `parent_hash`.

**Branches** are named pointers to snapshots (like Git refs).

**Forking** means creating a new branch from an existing checkpoint and resuming training from there.

---

## Live Monitoring

During training, PyTorch **hooks** (forward and backward) collect statistics from each layer and send them to the UI via an IPC channel. The graph responds visually:

| Signal | Visual encoding |
|--------|----------------|
| Gradient magnitude | Node color (blue → red) |
| Activation norm | Edge thickness |
| Activation magnitude | Edge color |

Clicking a node opens the **inspector**: weight histograms, gradient distributions, activation maps, parameter values.

---

## Experiment Tracking

Every training run is recorded as a `Run` object containing:

- Architecture hash
- Hyperparameter hash
- Dataset hash
- Metrics per epoch/step
- Hardware info (GPU, RAM)
- Status and timing

Runs are stored locally in SQLite. No external service required.
