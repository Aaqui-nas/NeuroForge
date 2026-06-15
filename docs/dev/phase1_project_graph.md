# Phase 1 — Projet & Éditeur de graphe

---

## 1.1 — Modèle de projet

### Objectif
Représenter un projet NeuroForge : métadonnées, configuration, path vers les ressources.

### Concepts
- `ProjectConfig` : dataclass immuable (nom, description, path racine, date de création)
- `Project` : entité vivante, charge/sauvegarde son état depuis le disque

### Sérialisation
Format JSON dans `<project_dir>/project.json`.

### Points d'attention
- Versionner le format JSON (champ `format_version`) pour pouvoir migrer plus tard
- Un projet doit être chargeable depuis n'importe quel path (paths relatifs dans le JSON)

---

## 1.2 — Modèle de graphe

### Objectif
Représenter le graphe de noeuds en mémoire, indépendamment de l'UI.

### Types principaux

```
NodeId = str (UUID)
EdgeId = str (UUID)
PortId = str

PortDirection: Enum → INPUT | OUTPUT
DataType: Enum → TENSOR | INT | FLOAT | STRING | ANY

Port:
  id: PortId
  name: str
  direction: PortDirection
  data_type: DataType
  required: bool

Node:
  id: NodeId
  type: str          # "linear", "relu", "conv2d"...
  name: str
  position: tuple[float, float]
  ports: dict[PortId, Port]
  params: dict[str, Any]

Edge:
  id: EdgeId
  src_node: NodeId
  src_port: PortId
  dst_node: NodeId
  dst_port: PortId

Graph:
  nodes: dict[NodeId, Node]
  edges: dict[EdgeId, Edge]
```

### Points d'attention
- Le graphe est un DAG (Directed Acyclic Graph) — les cycles doivent être refusés
- Une arête ne peut connecter que des ports de types compatibles
- Utiliser des UUIDs pour les IDs (jamais d'index entiers mutables)

---

## 1.3 — Sérialisation du graphe

### Format
JSON : `<project_dir>/graphs/<graph_id>.json`

### Algorithme de désérialisation
1. Charger les noeuds → instancier les `Node`
2. Charger les arêtes → vérifier que les noeuds référencés existent
3. Reconstruire les connexions
4. Valider le graphe (appeler le validateur de la section 1.4)

### Points d'attention
- Ne pas mettre l'UI state dans la sérialisation (position est OK, état de sélection non)
- Prévoir un champ `schema_version` pour les migrations futures

---

## 1.4 — Validation du graphe

### Objectif
S'assurer qu'un graphe est valide avant toute utilisation (génération de code, entraînement).

### Règles à valider
1. **Pas de cycles** — algorithme de détection de cycle dans un DAG
2. **Types compatibles** — un port TENSOR ne peut pas recevoir un INT
3. **Ports requis connectés** — tous les ports `required=True` ont une arête entrante
4. **Un seul producteur par port** — un port INPUT ne peut avoir qu'une arête entrante
5. **Pas d'arête orpheline** — les deux noeuds d'une arête existent

### Algorithme clé : détection de cycle
**DFS colorié** (3 couleurs : WHITE, GRAY, BLACK)
- WHITE : non visité
- GRAY : en cours de visite (dans la pile d'appel)
- BLACK : entièrement visité
- Si on atteint un noeud GRAY → cycle détecté

Alternativement : **algorithme de Kahn** (tri topologique par BFS)
- Calculer le in-degree de chaque noeud
- Mettre en file les noeuds à in-degree 0
- Retirer les arêtes des noeuds traités, mettre en file les nouveaux in-degree 0
- Si tous les noeuds sont traités → pas de cycle

### Retour de validation
```
ValidationResult:
  is_valid: bool
  errors: list[ValidationError]

ValidationError:
  code: str
  message: str
  node_id: NodeId | None
  edge_id: EdgeId | None
```

---

## 1.5 — Éditeur de graphe UI

### Objectif
Interface graphique pour créer, connecter et manipuler les noeuds.

### Architecture Qt
- `GraphScene(QGraphicsScene)` : contient les items
- `GraphView(QGraphicsView)` : pan, zoom, drag
- `NodeItem(QGraphicsItem)` : rendu d'un noeud
- `PortItem(QGraphicsEllipseItem)` : point de connexion cliquable
- `EdgeItem(QGraphicsPathItem)` : courbe de Bézier entre deux ports

### Algorithme : courbe de Bézier pour les arêtes
```
P0 = position du port source
P3 = position du port destination
P1 = P0 + (100, 0)    # tangente de sortie (vers la droite)
P2 = P3 - (100, 0)    # tangente d'entrée (vers la gauche)
```
Utiliser `QPainterPath.cubicTo(P1, P2, P3)`.

### Interactions à implémenter
- Drag depuis un port → dessiner l'arête en cours (`EdgeDraft`)
- Drop sur un port compatible → créer l'arête
- Drop dans le vide → annuler
- Double-click sur un noeud → ouvrir les paramètres
- Clic droit → context menu (supprimer, dupliquer, grouper)
- Molette → zoom
- Drag sur fond → pan

### Points d'attention
- Séparer le **modèle** (`graph/`) de la **vue** (`ui/graph_editor/`) — la scène ne modifie pas directement le Graph, elle émet des signaux
- Signal → Controller → Graph (pattern MVC ou Command)
- Le rendu de milliers de noeuds peut être lent : utiliser `QGraphicsItem.setFlag(ItemUsesExtendedStyleOption)` et le culling natif de Qt

---

## 1.6 — Bibliothèque de noeuds

### Objectif
Fournir un catalogue de noeuds prêts à l'emploi mappant les modules PyTorch.

### Noeuds Phase 1

| Catégorie | Noeuds |
|-----------|--------|
| Linear | Linear |
| Conv | Conv1d, Conv2d, Conv3d |
| Activation | ReLU, GELU, Sigmoid, Tanh, Softmax |
| Norm | BatchNorm1d, BatchNorm2d, LayerNorm |
| Regularisation | Dropout |
| Shape | Flatten, Reshape, Permute |
| Connexion | Add (résiduelle), Concat |
| I/O | Input, Output |

### Structure d'une définition de noeud
```python
NodeDefinition:
  type: str
  display_name: str
  category: str
  ports: list[PortDefinition]
  default_params: dict[str, Any]
  param_schema: dict  # pour générer l'UI de paramètres
```

### Registre
Un `NodeRegistry` singleton (ou dict global) qui mappe `type → NodeDefinition`.
Permettra d'ajouter des noeuds custom plus tard via plugins.

---

## 1.7 — Undo/Redo

### Pattern Command
```
Command (ABC):
  execute() → None
  undo() → None

CommandHistory:
  _stack: list[Command]
  _index: int
  push(cmd) → None
  undo() → None
  redo() → None
```

### Commandes à implémenter
- `AddNodeCommand`
- `RemoveNodeCommand`
- `MoveNodeCommand`
- `AddEdgeCommand`
- `RemoveEdgeCommand`
- `UpdateParamCommand`
- `GroupNodesCommand` (section 1.8)

### Points d'attention
- Composer les commandes : `MacroCommand` pour les opérations multi-étapes (ex: coller une sélection = N AddNode + M AddEdge)
- Limite de taille de l'historique (ex: 100 commandes) pour éviter les fuites mémoire

---

## 1.8 — Subgraphs & composants réutilisables

### Objectif
Permettre de grouper des noeuds en un composant réutilisable (`ComponentNode`).

### Algorithme de création d'un subgraph
1. L'utilisateur sélectionne un ensemble de noeuds S
2. Identifier les arêtes **entrantes** (src hors S, dst dans S) → deviennent les ports INPUT du composant
3. Identifier les arêtes **sortantes** (src dans S, dst hors S) → deviennent les ports OUTPUT du composant
4. Créer un `ComponentDefinition` avec un graphe interne
5. Remplacer S par un unique `ComponentNode` dans le graphe parent
6. Reconnect les arêtes externes sur les ports du nouveau noeud

### Structure
```
ComponentDefinition:
  id: str
  name: str
  inner_graph: Graph
  input_interface: list[Port]
  output_interface: list[Port]
```

### Points d'attention
- Les composants doivent être nestables (un composant peut contenir des composants)
- Stocker les `ComponentDefinition` dans un `ComponentLibrary` du projet
- Résolution récursive lors de la génération de code PyTorch (phase 2)
