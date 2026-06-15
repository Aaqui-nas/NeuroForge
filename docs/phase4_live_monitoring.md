# Phase 4 — Monitoring live du graphe

> Le graphe s'anime pendant l'entraînement. C'est le feature différenciateur de NeuroForge.

---

## 4.1 — Hooks PyTorch

### Objectif
Collecter les activations, poids et gradients de chaque couche pendant l'entraînement.

### Types de hooks PyTorch

**Forward hook** : déclenché après le `forward()` d'un module.
```python
def forward_hook(module, input, output):
    # input : tuple de tenseurs (entrées du module)
    # output : tenseur ou tuple (sorties)
    pass

handle = module.register_forward_hook(forward_hook)
```

**Backward hook** : déclenché après le backward, reçoit les gradients.
```python
def backward_hook(module, grad_input, grad_output):
    # grad_output : gradient w.r.t. la sortie du module
    pass

handle = module.register_full_backward_hook(backward_hook)
```

### HookManager
```
HookManager:
  _handles: list[RemovableHandle]
  _metrics_queue: Queue  # vers le process UI

  attach(model: nn.Module) → None
  detach() → None
  _on_forward(module, input, output, node_id) → None
  _on_backward(module, grad_input, grad_output, node_id) → None
```

### Métriques collectées par noeud
- Norme L2 de l'activation (sortie du forward)
- Norme L2 du gradient (grad_output du backward)
- Statistiques des poids : mean, std, min, max, norme

### Points d'attention
- Les hooks tournent **dans le process d'entraînement**
- N'envoyer que des statistiques scalaires dans la queue (pas les tenseurs entiers)
- Sous-échantillonner : collecter toutes les N steps pour ne pas ralentir l'entraînement
- Détacher les hooks proprement (`handle.remove()`) en fin d'entraînement

---

## 4.2 — Ring Buffer C++ pour streaming de métriques

### Objectif
Buffer lock-free entre le process d'entraînement et l'UI pour les métriques en temps réel.

### Pourquoi C++ ?
`multiprocessing.Queue` de Python a de la latence et de l'overhead de sérialisation.  
Un ring buffer en mémoire partagée est beaucoup plus rapide pour du streaming de scalaires.

### Design
```cpp
template<typename T, size_t N>
class RingBuffer {
public:
    bool try_push(const T& item);    // retourne false si plein
    bool try_pop(T& item);           // retourne false si vide
    size_t size() const;
    bool empty() const;
    bool full() const;
private:
    std::array<T, N> buffer_;
    std::atomic<size_t> head_{0};
    std::atomic<size_t> tail_{0};
};
```

### Implémentation lock-free (Single Producer, Single Consumer)
```cpp
bool try_push(const T& item) {
    size_t tail = tail_.load(std::memory_order_relaxed);
    size_t next = (tail + 1) % N;
    if (next == head_.load(std::memory_order_acquire))
        return false;  // plein
    buffer_[tail] = item;
    tail_.store(next, std::memory_order_release);
    return true;
}

bool try_pop(T& item) {
    size_t head = head_.load(std::memory_order_relaxed);
    if (head == tail_.load(std::memory_order_acquire))
        return false;  // vide
    item = buffer_[head];
    head_.store((head + 1) % N, std::memory_order_release);
    return true;
}
```

### Concepts clés à maîtriser
- `std::atomic` : opérations atomiques sans mutex
- `memory_order_relaxed / acquire / release` : barrières mémoire
- **SPSC** (Single Producer Single Consumer) : un seul thread écrit, un seul thread lit → lock-free trivial

### Binding pybind11
```cpp
PYBIND11_MODULE(_metrics, m) {
    py::class_<RingBuffer<MetricsSample, 1024>>(m, "MetricsRingBuffer")
        .def("try_push", &RingBuffer<MetricsSample, 1024>::try_push)
        .def("try_pop", ...)
        .def("empty", ...);
}
```

---

## 4.3 — Mise à jour live du graphe Qt

### Objectif
Actualiser les couleurs, épaisseurs et overlays des noeuds/arêtes en temps réel.

### Encodage visuel

| Métrique | Encodage |
|----------|----------|
| Norme du gradient | Couleur du noeud (bleu→rouge) |
| Norme de l'activation | Épaisseur de l'arête |
| Magnitude de l'activation | Couleur de l'arête |
| Statistiques courantes | Overlay texte sur le noeud |

### Mapping couleur (gradient magnitude)
```python
def gradient_to_color(norm: float, max_norm: float) -> QColor:
    t = min(norm / max_norm, 1.0)
    # interpolation HSV : bleu (t=0) → rouge (t=1)
    hue = 240 - int(t * 240)  # 240=bleu, 0=rouge
    return QColor.fromHsv(hue, 200, 220)
```

### Architecture de mise à jour
1. `QTimer` côté UI (100ms) → lire le ring buffer
2. Émettre un signal Qt `metrics_updated(dict[node_id, NodeMetrics])`
3. `GraphScene` reçoit le signal → appelle `node_item.update_metrics(metrics)` pour chaque noeud concerné
4. `NodeItem.update_metrics` stocke les métriques, appelle `update()` pour déclencher un repaint

### Points d'attention
- Ne pas appeler `update()` sur tous les noeuds à chaque tick : ne mettre à jour que les noeuds dont les métriques ont changé
- `QGraphicsItem.update()` est asynchrone → Qt batch les repaints
- Éviter les allocations dans le slot de mise à jour (réutiliser les objets QColor)

---

## 4.4 — Inspecteur de noeuds

### Objectif
Afficher les détails d'un noeud au clic : poids, gradients, activations, histogrammes.

### Panneau d'inspection
```
NodeInspector(QDockWidget):
  - Nom et type du noeud
  - Paramètres (read-only pendant training, éditable sinon)
  - Onglet "Poids" : histogramme des valeurs de poids
  - Onglet "Gradients" : histogramme des gradients
  - Onglet "Activations" : histogramme ou heatmap de la dernière activation
  - Stats : mean, std, min, max, norme L2, % valeurs nulles (mort neurons)
```

### Histogramme en temps réel
Utiliser l'algorithme de **Welford** pour calculer mean/variance en un seul passage :
```python
# Online mean & variance
n, mean, M2 = 0, 0.0, 0.0
for x in values:
    n += 1
    delta = x - mean
    mean += delta / n
    delta2 = x - mean
    M2 += delta * delta2
variance = M2 / n
```

Pour l'histogramme lui-même : `torch.histc(tensor, bins=50)` côté training process, envoyer les bin counts.

### Rendu du widget histogramme
- Option A : `matplotlib` embarqué dans Qt (lourd mais simple)
- Option B : `pyqtgraph` (léger, natif Qt, adapté au temps réel) — **recommandé**
- Option C : implémentation custom `QWidget` avec `QPainter`

---

## 4.5 — Panneaux de visualisation

### Loss & métriques curves
- `pyqtgraph.PlotWidget` mis à jour en streaming
- Courbes train/val sur le même graphe
- Zoom, pan, export image

### Weight distributions (par epoch)
- Empiler les histogrammes epoch par epoch → "violin plot temporel"
- Utile pour détecter le vanishing/exploding gradient

### Activation maps (Conv2d)
- Si le noeud est un Conv2d : afficher la feature map de la dernière image du batch
- Normaliser entre 0 et 1, afficher avec une colormap
- `QLabel` + `QPixmap` converti depuis numpy array

### Points d'attention
- Les activation maps sont volumineuses : n'envoyer qu'un sous-ensemble (première image du batch, premiers canaux)
- Proposer un mode "snapshot" (capture à la demande) vs "live" (update toutes les N steps)
