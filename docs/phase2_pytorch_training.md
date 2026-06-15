# Phase 2 — Génération PyTorch & Entraînement

---

## 2.1 — Inférence de shapes

### Objectif
Propager les formes de tenseurs à travers le graphe pour valider la cohérence avant génération de code.

### Algorithme
1. **Tri topologique** du graphe (algorithme de Kahn, voir phase 1.4)
2. Pour chaque noeud dans l'ordre topologique :
   - Récupérer les shapes en entrée (depuis les ports connectés)
   - Calculer les shapes en sortie selon le type de noeud
   - Stocker les shapes sur les ports de sortie

### Shape propagators
Chaque type de noeud a une fonction `propagate_shape(input_shapes, params) → output_shapes`.

Exemples :
- `Linear(in_features, out_features)` : `(B, in_features) → (B, out_features)`
- `Conv2d(in_ch, out_ch, kernel_size, stride, padding)` : `(B, C, H, W) → (B, out_ch, H', W')`  
  formule H' = floor((H + 2*padding - kernel_size) / stride + 1)
- `Flatten()` : `(B, C, H, W) → (B, C*H*W)`

### Points d'attention
- Les shapes peuvent être **partiellement connues** (batch size = None)
- Utiliser `Optional[int]` pour les dimensions inconnues
- Arrêter la propagation et remonter une erreur si les shapes sont incompatibles

---

## 2.2 — Générateur de code PyTorch

### Objectif
Convertir un `Graph` en un `nn.Module` PyTorch valide (code Python).

### Approche : génération de texte (string-based)
Générer du code Python lisible plutôt qu'un AST.  
Avantage : debuggable par l'utilisateur.

### Algorithme
1. Tri topologique → ordre d'exécution
2. Générer la classe `__init__` : instancier chaque noeud à état (Linear, Conv2d…)
3. Générer la méthode `forward` : appeler les noeuds dans l'ordre, propager les tenseurs

### Template de sortie
```python
class GeneratedModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear_0 = nn.Linear(128, 64)
        self.relu_1 = nn.ReLU()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        out_0 = self.linear_0(x)
        out_1 = self.relu_1(out_0)
        return out_1
```

### Gestion des composants réutilisables
Résoudre récursivement chaque `ComponentNode` → générer une sous-classe `nn.Module` séparée.

### Points d'attention
- Nommer les variables `out_{node_id_court}` pour éviter les collisions
- Gérer les noeuds à **multiples sorties** (ex: Split)
- Gérer les **connexions résiduelles** (Add) : plusieurs entrées → combiner
- La génération doit être **déterministe** (même graphe → même code)

---

## 2.3 — Gestionnaire de datasets

### Objectif
Enregistrer, prévisualiser et configurer des datasets pour l'entraînement.

### Datasets supportés (MVP)
- **CSV** : via `pandas` + `torch.utils.data.Dataset` custom
- **Images** : dossier `<class>/<images>` → `torchvision.datasets.ImageFolder`
- **Torch** : datasets torchvision (MNIST, CIFAR10…)

### Modèle
```
DatasetConfig:
  id: str
  name: str
  type: DatasetType  # CSV | IMAGE_FOLDER | TORCH_BUILTIN
  path: Path | None
  torch_name: str | None
  split_ratios: tuple[float, float, float]  # train/val/test
  transform_config: dict
```

### DataLoader configuration
- batch_size, num_workers, shuffle, pin_memory
- Généré dynamiquement depuis `DatasetConfig`

---

## 2.4 — Configuration d'entraînement

### Modèle
```
TrainingConfig:
  optimizer: OptimizerConfig
  loss: LossConfig
  scheduler: SchedulerConfig | None
  epochs: int
  device: str  # "cpu", "cuda", "mps"
  mixed_precision: bool

OptimizerConfig:
  type: str  # "adam", "sgd", "adamw"
  lr: float
  params: dict

LossConfig:
  type: str  # "cross_entropy", "mse", "bce"
  params: dict
```

### Points d'attention
- Les configs sont sérialisables (versioning en phase 3)
- Valider la cohérence : loss BCE + sortie non-sigmoid → warning

---

## 2.5 — Moteur d'entraînement

### Objectif
Exécuter l'entraînement dans un process séparé, l'UI reste réactive.

### Architecture IPC
```
UI Process          Training Process
    │                      │
    │  ─── start ──────►   │
    │                      │  (training loop)
    │  ◄── metrics ───     │  multiprocessing.Queue
    │  ◄── checkpoint ──   │
    │                      │
    │  ─── stop ───────►   │  Event
```

### Composants
- `TrainingWorker` : tourne dans un subprocess, exécute la boucle d'entraînement
- `MetricsEmitter` : envoie les métriques dans la Queue à chaque step/epoch
- `TrainingController` : côté UI, lance le worker, lit la Queue, émet des signaux Qt

### Queue messages
```
TrainingMessage:
  type: MessageType  # METRICS | CHECKPOINT | LOG | ERROR | DONE
  payload: dict
  timestamp: float
```

### Points d'attention
- **La Queue doit être drainée côté UI** sans bloquer : utiliser un `QTimer` qui lit la queue toutes les 100ms
- Les checkpoints sont sauvegardés par le worker (`torch.save`), l'UI est juste notifiée
- Gérer les crashs du subprocess : surveiller le process avec `.is_alive()`

---

## 2.6 — Suivi d'expériences

### Modèle
```
Run:
  id: str
  experiment_name: str
  graph_id: str
  dataset_id: str
  training_config: TrainingConfig
  hardware_info: HardwareInfo
  start_time: datetime
  end_time: datetime | None
  status: RunStatus  # RUNNING | COMPLETED | FAILED | STOPPED
  metrics: dict[str, list[float]]  # "train_loss": [0.9, 0.7, ...]
  checkpoints: list[CheckpointRef]

HardwareInfo:
  gpu: str | None
  gpu_memory_gb: float | None
  cpu: str
  ram_gb: float
```

### Stockage
SQLite via `sqlite3` standard (pas d'ORM pour rester léger) dans `<project_dir>/runs.db`.

### Points d'attention
- Garder les métriques en mémoire pendant le run, flush en DB par batch
- Index sur `experiment_name` et `start_time` pour les queries de comparaison
