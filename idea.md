# CLAUDE.md

## Project Name

NeuroForge

## Vision

NeuroForge is a desktop application for visually designing, training, analyzing and versioning PyTorch neural networks.

The goal is to provide a complete desktop environment for machine learning experimentation without relying on web technologies.

Users should be able to:

* Build neural networks through a node-based visual editor.
* Create reusable sub-networks.
* Configure datasets, losses, optimizers and schedulers visually.
* Launch training locally or on remote machines.
* Monitor training in real time.
* Visualize weights, gradients and activations directly on the graph.
* Compare experiments.
* Version architectures, datasets, checkpoints and experiments using a custom object-based versioning system inspired by Git.

The application should feel closer to Unreal Engine Blueprint, Blender Geometry Nodes or LabVIEW than to a web dashboard.

---

# Core Principles

## Desktop First

This is a desktop application.

Do not use web technologies such as:

* React
* Electron
* Next.js
* Vue
* Angular

Preferred stack:

* Python
* PySide6
* Qt
* PyTorch

The application must run natively on:

* Linux
* Windows
* macOS

---

## Visual First

The graph editor is the center of the application.

Users should not need to write code for common tasks.

Everything should be configurable through the interface.

Generated PyTorch code is an implementation detail.

---

## PyTorch Native

PyTorch is the only backend framework.

The graph should generate valid PyTorch modules.

Every visual node must map cleanly to PyTorch concepts.

Examples:

* Linear
* Conv1D
* Conv2D
* Conv3D
* ReLU
* GELU
* BatchNorm
* LayerNorm
* Dropout
* Attention
* Transformer Blocks
* Residual Connections
* Custom Modules

---

## Reusable Components

Users can convert any graph into a reusable component.

Example:

Encoder
├── Conv
├── Conv
└── Pool

becomes

EncoderBlock

which can then be reused elsewhere.

Nested components must be supported.

---

# Main Modules

## Graph Editor

Responsibilities:

* Node creation
* Node deletion
* Connections
* Node grouping
* Subgraphs
* Copy/paste
* Undo/redo
* Validation

Preferred implementation:

* NodeGraphQt
* Custom Qt Graphics Scene if needed

---

## Training Engine

Responsibilities:

* Generate PyTorch code
* Build runtime graph
* Execute training
* Save checkpoints
* Emit live metrics

Training must run in separate processes.

UI must never block.

---

## Dataset Manager

Responsibilities:

* Dataset registration
* Dataset versioning
* Preview samples
* Split configuration

Supported initially:

* CSV
* Images
* Folder datasets
* Torch datasets

Future:

* HuggingFace datasets

---

## Experiment Tracker

Responsibilities:

* Track runs
* Metrics
* Hyperparameters
* Checkpoints
* Hardware information

Must work offline.

No cloud dependency.

---

## Visualization Engine

Responsibilities:

* Loss curves
* Accuracy curves
* Weight distributions
* Gradient distributions
* Activation maps

All visualizations must update live during training.

---

# Advanced Visual Monitoring

The graph itself should become alive during training.

Examples:

Node color:

* Gradient magnitude

Connection thickness:

* Signal strength

Connection color:

* Activation magnitude

Node overlay:

* Current statistics

Users should be able to click a node and inspect:

* Parameters
* Weights
* Gradients
* Histograms
* Activations

This is a major differentiating feature.

---

# Versioning System

NeuroForge must implement its own object storage system.

Do not use Git internally.

The architecture should be inspired by Git concepts.

---

## Object Model

Everything is immutable.

Objects:

* DatasetObject
* GraphObject
* ArchitectureObject
* HyperparameterObject
* CheckpointObject
* MetricsObject
* ExperimentObject
* RunObject

Each object receives:

SHA256(content)

as unique identifier.

---

## Storage Layout

project/

objects/
refs/
metadata/

Example:

project/
├── objects/
├── refs/
├── metadata/
└── cache/

---

## Branches

Users can create branches.

Examples:

main

cnn_experiments

transformer_experiments

research_v2

Branches point to experiment snapshots.

---

## Snapshots

Snapshots capture:

* Architecture
* Hyperparameters
* Dataset
* Checkpoint
* Metrics

A snapshot is immutable.

---

## Forking

Users can fork from any checkpoint.

Example:

Run 10
Epoch 50

Fork

Run 11

Training resumes from Epoch 50.

This is a first-class feature.

---

# Code Quality

Requirements:

* Type hints everywhere
* Dataclasses where appropriate
* Modular architecture
* No giant files
* No global state
* Extensive documentation

Maximum file size target:

1000 lines

Preferred:

300-500 lines

---

# Folder Structure

src/

core/
graph/
training/
datasets/
tracking/
storage/
visualization/
ui/

tests/

assets/

docs/

---

# MVP Roadmap

Phase 1

* Project system
* Node editor
* Basic nodes
* Save/load projects

Phase 2

* PyTorch generation
* Local training
* Metrics tracking

Phase 3

* Versioning system
* Branches
* Snapshots

Phase 4

* Live graph monitoring
* Weight visualization
* Gradient visualization

Phase 5

* Remote execution
* Cluster execution
* Advanced profiling

---

# Long-Term Goal

Become the equivalent of Unreal Blueprint for deep learning.

A researcher should be able to:

* Design architectures visually
* Train models
* Analyze internals
* Version experiments
* Compare runs

without leaving the application.
