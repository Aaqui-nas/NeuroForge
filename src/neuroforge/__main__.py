from __future__ import annotations

import sys
import uuid

from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QApplication,
    QDockWidget,
    QInputDialog,
    QMainWindow,
    QStatusBar,
)

from neuroforge.graph.commands import (
    AddEdgeCommand,
    AddNodeCommand,
    CommandHistory,
    GroupNodesCommand,
    MoveNodeCommand,
    RemoveNodeCommand,
)
from neuroforge.graph.components import ComponentLibrary
from neuroforge.graph.model import Edge, Graph, Node, Port
from neuroforge.graph.registry import NodeDefinition, NodeRegistry, build_default_registry
from neuroforge.ui.graph_editor.scene import GraphScene
from neuroforge.ui.graph_editor.view import GraphView
from neuroforge.ui.palette import NodePalette


def _node_from_def(
    defn: NodeDefinition,
    node_id: str,
    name: str,
    position: tuple[float, float],
) -> Node:
    """Instantiate a `Node` from a `NodeDefinition`."""
    ports = {
        pd.id: Port(
            id=pd.id,
            name=pd.name,
            direction=pd.direction,
            data_type=pd.data_type,
            required=pd.required,
        )
        for pd in defn.ports
    }
    return Node(
        id=node_id,
        type=defn.type,
        name=name,
        position=position,
        ports=ports,
        params=dict(defn.default_params),
    )


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("NeuroForge")
        self.resize(1280, 720)

        self._registry: NodeRegistry = build_default_registry()
        self._graph = Graph()
        self._history = CommandHistory()
        self._components = ComponentLibrary()

        for node_type, node_id, name, pos in [
            ("input", "n1", "Input", (50.0, 200.0)),
            ("linear", "n2", "Linear", (300.0, 170.0)),
            ("relu", "n3", "ReLU", (550.0, 170.0)),
            ("output", "n4", "Output", (800.0, 200.0)),
        ]:
            defn = self._registry.get(node_type)
            AddNodeCommand(self._graph, _node_from_def(defn, node_id, name, pos)).execute()

        for edge in [
            Edge(id="e1", src_node="n1", src_port="output", dst_node="n2", dst_port="input"),
            Edge(id="e2", src_node="n2", src_port="output", dst_node="n3", dst_port="input"),
            Edge(id="e3", src_node="n3", src_port="output", dst_node="n4", dst_port="input"),
        ]:
            AddEdgeCommand(self._graph, edge).execute()

        self._scene = GraphScene(self._graph)
        self._view = GraphView(self._scene)
        self.setCentralWidget(self._view)

        self._palette = NodePalette(self._registry, self._components)
        self._palette.node_type_activated.connect(self._on_palette_node_activated)
        dock = QDockWidget("Nœuds", self)
        dock.setWidget(self._palette)
        dock.setFeatures(
            QDockWidget.DockWidgetFeature.DockWidgetMovable
            | QDockWidget.DockWidgetFeature.DockWidgetFloatable
        )
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, dock)

        self._status = QStatusBar()
        self.setStatusBar(self._status)
        self._refresh_status()

        self._scene.node_moved.connect(self._on_node_moved)
        self._scene.connection_requested.connect(self._on_connection_requested)
        self._scene.node_added.connect(self._refresh_status)
        self._scene.node_removed.connect(self._refresh_status)
        self._scene.edge_added.connect(self._refresh_status)
        self._scene.edge_removed.connect(self._refresh_status)

        QShortcut(QKeySequence.StandardKey.Undo, self).activated.connect(self._undo)
        QShortcut(QKeySequence.StandardKey.Redo, self).activated.connect(self._redo)
        QShortcut(QKeySequence("Ctrl+Y"), self).activated.connect(self._redo)
        QShortcut(QKeySequence(Qt.Key.Key_Delete), self).activated.connect(self._delete_selected)
        QShortcut(QKeySequence("Ctrl+G"), self).activated.connect(self._group_selected)

    def _on_palette_node_activated(self, node_type: str) -> None:
        """Ajoute un nœud ou un composant au centre de la vue courante."""
        center = self._view.mapToScene(self._view.viewport().rect().center())
        pos = (center.x(), center.y())

        if node_type.startswith("component:"):
            comp_id = node_type[len("component:") :]
            comp = self._components.get(comp_id)
            ports = {p.id: p for p in comp.input_interface + comp.output_interface}
            node = Node(
                id=str(uuid.uuid4()),
                type="component",
                name=comp.name,
                position=pos,
                ports=ports,
                params={},
                component_id=comp.id,
            )
        else:
            defn = self._registry.get(node_type)
            node = _node_from_def(defn, str(uuid.uuid4()), defn.display_name, pos)

        self._history.push(AddNodeCommand(self._graph, node))
        self._scene.add_node_item(node)
        self._refresh_status()

    def _on_connection_requested(
        self, src_node: str, src_port: str, dst_node: str, dst_port: str
    ) -> None:
        """Crée une arête dans le modèle et la scène, et la pousse dans l'historique."""
        edge = Edge(
            id=str(uuid.uuid4()),
            src_node=src_node,
            src_port=src_port,
            dst_node=dst_node,
            dst_port=dst_port,
        )
        self._history.push(AddEdgeCommand(self._graph, edge))
        self._scene.add_edge_item(edge)
        self._refresh_status()

    def _on_node_moved(self, node_id: str, x: float, y: float) -> None:
        """Pousse un MoveNodeCommand pour que le déplacement soit annulable."""
        if node_id not in self._graph.nodes:
            return
        old_pos = self._graph.nodes[node_id].position
        new_pos = (x, y)
        if old_pos == new_pos:
            return
        self._history.push(MoveNodeCommand(self._graph, node_id, old_pos, new_pos))
        self._refresh_status()

    def _delete_selected(self) -> None:
        """Supprime les nœuds sélectionnés du modèle et de la scène."""
        for node_id in self._scene.selected_node_ids():
            self._history.push(RemoveNodeCommand(self._graph, node_id))
            self._scene.remove_node_item(node_id)

    def _group_selected(self) -> None:
        """Groupe les nœuds sélectionnés en un composant réutilisable (Ctrl+G)."""
        node_ids = self._scene.selected_node_ids()
        if len(node_ids) < 2:
            return
        name, ok = QInputDialog.getText(self, "Nouveau composant", "Nom du composant :")
        if not ok or not name.strip():
            return
        name = name.strip()

        comp = self._components.create_from_selection(self._graph, node_ids, name)

        positions = [
            self._graph.nodes[nid].position for nid in node_ids if nid in self._graph.nodes
        ]
        cx = sum(p[0] for p in positions) / len(positions)
        cy = sum(p[1] for p in positions) / len(positions)

        ports = {p.id: p for p in comp.input_interface + comp.output_interface}
        component_node = Node(
            id=str(uuid.uuid4()),
            type="component",
            name=name,
            position=(cx, cy),
            ports=ports,
            params={},
            component_id=comp.id,
        )

        self._history.push(GroupNodesCommand(self._graph, node_ids, name, component_node))
        self._scene.load_graph(self._graph)
        self._palette.refresh()
        self._refresh_status()

    def _undo(self) -> None:
        self._history.undo()
        self._scene.load_graph(self._graph)
        self._refresh_status()

    def _redo(self) -> None:
        self._history.redo()
        self._scene.load_graph(self._graph)
        self._refresh_status()

    def _refresh_status(self, *_: object) -> None:
        n = len(self._graph.nodes)
        e = len(self._graph.edges)
        c = len(self._components.all())
        undo = "oui" if self._history.can_undo() else "non"
        redo = "oui" if self._history.can_redo() else "non"
        self._status.showMessage(
            f"Nœuds : {n}   Arêtes : {e}   Composants : {c}   "
            f"Undo (Ctrl+Z) : {undo}   Redo (Ctrl+Y) : {redo}"
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
