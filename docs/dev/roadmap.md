# NeuroForge — Roadmap

## Vue d'ensemble

| Phase | Titre | Statut |
|-------|-------|--------|
| 0 | Initialisation du projet | En cours |
| 1 | Projet & Éditeur de graphe | À faire |
| 2 | Génération PyTorch & Entraînement | À faire |
| 3 | Système de versioning | À faire |
| 4 | Monitoring live du graphe | À faire |
| 5 | Exécution distante | À faire |

---

## Phase 0 — Initialisation du projet
> Objectif : environnement de développement opérationnel, structure en place, CI locale fonctionnelle.

Voir : [phase0_init.md](phase0_init.md)

- [ ] 0.1 — Structure du projet et tooling Python
- [ ] 0.2 — Setup C++ (CMake + pybind11)
- [ ] 0.3 — Pipeline de tests (pytest + Google Test)
- [ ] 0.4 — Linting et typage (ruff + mypy)

---

## Phase 1 — Projet & Éditeur de graphe
> Objectif : créer, sauvegarder et charger un graphe de noeuds dans l'UI.

Voir : [phase1_project_graph.md](phase1_project_graph.md)

- [ ] 1.1 — Modèle de projet (Project, ProjectConfig)
- [ ] 1.2 — Modèle de graphe (Node, Port, Edge, Graph)
- [ ] 1.3 — Sérialisation/désérialisation du graphe (JSON)
- [ ] 1.4 — Validation du graphe (cycles, types de ports)
- [ ] 1.5 — Éditeur de graphe UI (QGraphicsScene)
- [ ] 1.6 — Bibliothèque de noeuds de base (Linear, Conv, ReLU…)
- [ ] 1.7 — Undo/Redo (pattern Command)
- [ ] 1.8 — Subgraphs & composants réutilisables

---

## Phase 2 — Génération PyTorch & Entraînement
> Objectif : générer du code PyTorch valide depuis le graphe et lancer un entraînement.

Voir : [phase2_pytorch_training.md](phase2_pytorch_training.md)

- [ ] 2.1 — Inférence de shapes (propagation de tenseurs dans le graphe)
- [ ] 2.2 — Générateur de code PyTorch (Graph → nn.Module)
- [ ] 2.3 — Gestionnaire de datasets (CSV, images, dossiers)
- [ ] 2.4 — Configuration d'entraînement (loss, optimizer, scheduler)
- [ ] 2.5 — Moteur d'entraînement (subprocess + IPC)
- [ ] 2.6 — Suivi d'expériences (runs, métriques, hyperparamètres)

---

## Phase 3 — Système de versioning
> Objectif : versionner architectures, datasets, checkpoints et expériences.

Voir : [phase3_versioning.md](phase3_versioning.md)

- [ ] 3.1 — Object store C++ (SHA256, content-addressable)
- [ ] 3.2 — Modèles d'objets immuables (GraphObject, CheckpointObject…)
- [ ] 3.3 — Layout de stockage (.neuroforge/)
- [ ] 3.4 — Snapshots
- [ ] 3.5 — Branches et refs
- [ ] 3.6 — Forking depuis un checkpoint

---

## Phase 4 — Monitoring live du graphe
> Objectif : le graphe s'anime pendant l'entraînement (couleurs, épaisseurs, inspecteur).

Voir : [phase4_live_monitoring.md](phase4_live_monitoring.md)

- [ ] 4.1 — Hooks PyTorch (forward/backward)
- [ ] 4.2 — Ring buffer C++ pour streaming de métriques
- [ ] 4.3 — Mise à jour live du graphe Qt
- [ ] 4.4 — Inspecteur de noeuds (poids, gradients, histogrammes)
- [ ] 4.5 — Panneaux de visualisation (courbes, distributions)

---

## Phase 5 — Exécution distante
> Objectif : lancer l'entraînement sur des machines distantes.

Voir : [phase5_remote_execution.md](phase5_remote_execution.md)

- [ ] 5.1 — Gestion de connexions SSH
- [ ] 5.2 — Synchronisation de fichiers distante
- [ ] 5.3 — Lancement d'entraînement distant et rapatriement de métriques
- [ ] 5.4 — Transfert de checkpoints
- [ ] 5.5 — Profiling avancé (PyTorch profiler, GPU utilization)
