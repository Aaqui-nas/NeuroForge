# Phase 3 — Système de versioning

> Inspiré de Git, mais adapté aux objets ML. Implémenté en C++ pour le core storage.

---

## 3.1 — Object Store C++ (content-addressable)

### Objectif
Stocker des objets immuables identifiés par le SHA256 de leur contenu.

### Principe fondamental
```
hash = SHA256(content)
path = objects/{hash[0:2]}/{hash[2:]}
```
Identique au modèle objet de Git.

### Interface C++ (à exposer via pybind11)
```cpp
class ObjectStore {
public:
    explicit ObjectStore(std::filesystem::path root);

    // Stocker un objet, retourner son hash
    std::string put(const std::vector<uint8_t>& data);

    // Récupérer un objet par hash
    std::vector<uint8_t> get(const std::string& hash) const;

    // Vérifier l'existence
    bool exists(const std::string& hash) const;

    // Vérifier l'intégrité (hash du contenu == hash du nom de fichier)
    bool verify(const std::string& hash) const;
};
```

### Algorithme de `put`
1. Calculer SHA256 du contenu (bibliothèque OpenSSL ou implémentation pure C++)
2. Construire le path : `root/objects/{hash[:2]}/{hash[2:]}`
3. Si le fichier existe déjà → retourner le hash (déduplication automatique)
4. Créer le répertoire si besoin
5. Écrire le contenu
6. Marquer le fichier en lecture seule (`chmod 444`) — immuabilité garantie

### Bibliothèque SHA256
- Option A : OpenSSL (`#include <openssl/sha.h>`) — déjà présente sur la plupart des systèmes
- Option B : implémentation single-header (ex: `picosha2`) — zéro dépendance externe

### Points d'attention
- Opération atomique : écrire dans un fichier temporaire, puis rename (évite les fichiers corrompus)
- Thread-safe : les écritures sont atomiques par design (fichiers immuables), lectures concurrentes OK
- La déduplication est **gratuite** : deux objets identiques ne sont stockés qu'une fois

---

## 3.2 — Modèles d'objets immuables

### Hiérarchie
```
NeuroForgeObject (ABC):
  object_type: str
  serialize() → bytes
  deserialize(data: bytes) → Self  [classmethod]

GraphObject(NeuroForgeObject):
  graph: Graph

ArchitectureObject(NeuroForgeObject):
  graph_hash: str
  component_hashes: dict[str, str]

HyperparameterObject(NeuroForgeObject):
  training_config: TrainingConfig

DatasetObject(NeuroForgeObject):
  dataset_config: DatasetConfig
  split_hash: str  # hash de la liste d'indices train/val/test

CheckpointObject(NeuroForgeObject):
  weights_hash: str  # hash du fichier .pt
  epoch: int
  step: int

MetricsObject(NeuroForgeObject):
  metrics: dict[str, list[float]]

RunObject(NeuroForgeObject):
  architecture_hash: str
  hyperparameter_hash: str
  dataset_hash: str
  checkpoint_hash: str | None
  metrics_hash: str

ExperimentObject(NeuroForgeObject):
  name: str
  run_hashes: list[str]  # liste ordonnée de runs
```

### Sérialisation
Format : **MessagePack** (binaire, compact) ou JSON (debuggable).
Recommandation : JSON encodé en UTF-8, stocké tel quel dans l'object store.

---

## 3.3 — Layout de stockage

```
<project_dir>/
  .neuroforge/
    objects/
      ab/
        cdef1234...    # fichier = contenu brut
      ff/
        ...
    refs/
      main             # fichier contenant un hash d'ExperimentObject
      branches/
        cnn_experiments
        transformer_v2
    HEAD               # nom de la branche courante
    metadata/
      config.json      # config du repo (nom, créateur, version)
```

### Refs
Un ref est un fichier texte contenant un hash SHA256.
Analogie Git : `refs/heads/main` pointe sur un commit → ici pointe sur un `ExperimentObject`.

---

## 3.4 — Snapshots

### Définition
Un snapshot capture l'état complet d'une expérience à un instant T.

```
Snapshot:
  architecture_hash: str
  hyperparameter_hash: str
  dataset_hash: str
  checkpoint_hash: str | None
  metrics_hash: str
  parent_hash: str | None   # snapshot précédent (chaîne d'historique)
  timestamp: str
  message: str              # message utilisateur (comme un commit message)
```

### Algorithme de création
1. Sérialiser les objets composants, les stocker dans l'object store → obtenir leurs hashes
2. Créer le `Snapshot` avec ces hashes
3. Sérialiser le snapshot, le stocker → obtenir le hash du snapshot
4. Mettre à jour la branche courante : écrire le hash du snapshot dans `refs/<branch>`

### Chaîne d'historique
`snapshot_N.parent_hash = hash(snapshot_{N-1})`
Permet de remonter l'historique (comme `git log`).

---

## 3.5 — Branches et refs

### Opérations
```
BranchManager:
  create_branch(name: str, from_hash: str | None) → None
  switch_branch(name: str) → None
  delete_branch(name: str) → None
  list_branches() → list[BranchInfo]
  current_branch() → str
  resolve_ref(name: str) → str  # nom → hash
```

### Fichier HEAD
```
ref: branches/main
```
Ou en mode "detached HEAD" (fork) :
```
hash: abc123...
```

---

## 3.6 — Forking

### Objectif
Reprendre l'entraînement depuis un checkpoint antérieur, sur une nouvelle branche.

### Algorithme
1. L'utilisateur sélectionne un `CheckpointObject` d'un run passé
2. Créer une nouvelle branche depuis le snapshot contenant ce checkpoint
3. Créer un nouveau `RunObject` avec `parent_run_hash` et `resume_from_epoch`
4. Le `TrainingWorker` (phase 2.5) charge le checkpoint via `torch.load` et reprend

### Points d'attention
- Le checkpoint doit inclure l'état de l'optimizer (pas seulement les poids du modèle)
- `torch.save({'model': model.state_dict(), 'optimizer': opt.state_dict(), 'epoch': epoch})`
- Valider que l'architecture du fork est compatible avec le checkpoint (même shape de poids)
