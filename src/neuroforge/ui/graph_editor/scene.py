# mypy: disable-error-code="empty-body"
from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QGraphicsScene

from neuroforge.graph.model import Edge, EdgeId, Graph, Node, NodeId


class GraphScene(QGraphicsScene):
    node_added: Signal = Signal(str)
    node_removed: Signal = Signal(str)
    node_moved: Signal = Signal(str, float, float)
    edge_added: Signal = Signal(str)
    edge_removed: Signal = Signal(str)
    node_double_clicked: Signal = Signal(str)
    selection_updated: Signal = Signal(list)

    def __init__(self, graph: Graph) -> None: ...

    def load_graph(self, graph: Graph) -> None: ...

    def add_node_item(self, node: Node) -> None: ...

    def remove_node_item(self, node_id: NodeId) -> None: ...

    def add_edge_item(self, edge: Edge) -> None: ...

    def remove_edge_item(self, edge_id: EdgeId) -> None: ...

    def begin_edge_draft(self, src_node_id: NodeId, src_port_id: str) -> None: ...

    def cancel_edge_draft(self) -> None: ...

    def selected_node_ids(self) -> list[NodeId]: ...
