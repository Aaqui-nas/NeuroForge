# Phase 5 — Exécution distante

---

## 5.1 — Gestion des connexions SSH

### Bibliothèque
`paramiko` : client SSH pure Python, bien maintenu.

### Modèle de connexion
```
RemoteHost:
  id: str
  name: str
  hostname: str
  port: int
  username: str
  auth: SSHAuthConfig  # clé privée ou password

SSHAuthConfig:
  type: AuthType  # KEY | PASSWORD | AGENT
  key_path: Path | None
  passphrase: str | None
```

### RemoteConnectionManager
```
RemoteConnectionManager:
  connect(host: RemoteHost) → SSHClient
  disconnect(host_id: str) → None
  is_connected(host_id: str) → bool
  test_connection(host: RemoteHost) → ConnectionTestResult
```

### Points d'attention
- Stocker les mots de passe/passphrase dans le keyring système (`keyring` library)
- Timeout de connexion configurable (défaut : 10s)
- Reconnexion automatique si la session expire

---

## 5.2 — Synchronisation de fichiers distante

### Objectif
Envoyer le code généré, les datasets et les configs sur la machine distante.

### Approche
`rsync` via subprocess (si disponible) ou `paramiko SFTP` en fallback.

### Ce qui est synchronisé
1. Le code PyTorch généré (fichier `.py` unique)
2. La `TrainingConfig` sérialisée (JSON)
3. Les datasets (si pas déjà présents, vérifier par hash)
4. Le checkpoint de reprise (si fork)

### Algorithme de sync intelligente
1. Pour chaque fichier à synchroniser : calculer son hash SHA256 local
2. Vérifier si le fichier existe à distance avec ce hash
3. Ne transférer que les fichiers manquants ou modifiés

### RemoteEnvironmentSetup
- Vérifier que Python, PyTorch et les dépendances sont installés
- Créer un venv distant si nécessaire
- Installer les dépendances manquantes (`pip install -r requirements.txt`)

---

## 5.3 — Lancement d'entraînement distant et rapatriement de métriques

### Architecture
```
UI Process (local)          Remote Machine
    │                           │
    │  ── SSH exec ──────────►  │  python train.py
    │                           │  (training loop)
    │  ◄── SSH tunnel ────────  │  stdout: JSON metrics
    │  (streaming stdout)       │
```

### Streaming des métriques
Le script d'entraînement sur la machine distante écrit les métriques sur stdout en JSON :
```json
{"type": "metrics", "epoch": 1, "step": 100, "loss": 0.54, "acc": 0.87}
{"type": "checkpoint", "path": "/tmp/checkpoint_epoch1.pt"}
{"type": "done", "status": "completed"}
```

Côté local : lire le stdout du channel SSH ligne par ligne dans un thread, parser le JSON, mettre à jour l'UI.

### RemoteTrainingController
```
RemoteTrainingController:
  start(config: RemoteTrainingConfig) → None
  stop() → None
  on_metrics_received: Signal[dict]
  on_checkpoint_available: Signal[str]
  on_training_done: Signal[RunStatus]
```

---

## 5.4 — Transfert de checkpoints

### Stratégie
- Checkpoints sauvegardés sur la machine distante dans un répertoire temporaire
- Rapatriation automatique après chaque epoch (configurable : toutes les N epochs)
- Stocker dans l'object store local (phase 3)

### Compression
- Les checkpoints PyTorch peuvent être volumineux (GB pour les grands modèles)
- Proposer une option de compression (`gzip`) avant transfert
- Pour les modèles très grands : ne transférer que les deltas (sparse diff des poids) — avancé

---

## 5.5 — Profiling avancé

### PyTorch Profiler
```python
with torch.profiler.profile(
    activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA],
    schedule=torch.profiler.schedule(wait=1, warmup=1, active=3),
    on_trace_ready=torch.profiler.tensorboard_trace_handler('./log'),
    record_shapes=True,
    with_stack=True
) as prof:
    # training step
    pass
```

### Métriques de profiling
- Temps par opération (CPU + GPU)
- Utilisation GPU (via `nvidia-smi` ou `pynvml`)
- Utilisation mémoire GPU
- Throughput (samples/sec)

### Affichage dans NeuroForge
- Timeline des opérations (Gantt chart simplifié)
- Tableau des top N opérations les plus coûteuses
- Courbe d'utilisation GPU en temps réel

### pynvml
```python
import pynvml
pynvml.nvmlInit()
handle = pynvml.nvmlDeviceGetHandleByIndex(0)
info = pynvml.nvmlDeviceGetMemoryInfo(handle)
util = pynvml.nvmlDeviceGetUtilizationRates(handle)
```

### Points d'attention
- Le profiling ralentit l'entraînement : proposer un mode "profiling" séparé
- Les traces de profiling peuvent être énormes : limiter la durée de capture
- Sur machine distante : exécuter le profiler, rapatrier la trace, la visualiser localement
