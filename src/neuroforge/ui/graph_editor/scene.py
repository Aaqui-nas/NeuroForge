from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QGraphicsScene

from neuroforge.graph.model import Edge, EdgeId, Graph, Node, NodeId
from neuroforge.ui.graph_editor.items import EdgeDraftItem, EdgeItem, NodeItem


class GraphScene(QGraphicsScene):
    """The Qt scene that holds and manages all visual items of a graph.

    Acts as the bridge between the graph model (`Graph`) and the visual
    layer (`NodeItem`, `EdgeItem`). All mutations go through this class;
    items never modify the model directly.

    Signals:
        node_added: Emitted with the node ID after a `NodeItem` is added.
        node_removed: Emitted with the node ID after a `NodeItem` is removed.
        node_moved: Emitted with (node_id, x, y) after a node is dragged.
        edge_added: Emitted with the edge ID after an `EdgeItem` is added.
        edge_removed: Emitted with the edge ID after an `EdgeItem` is removed.
        node_double_clicked: Emitted with the node ID on double-click.
        selection_updated: Emitted with the list of selected node IDs on
            every selection change.
    """

    node_added: Signal = Signal(str)
    node_removed: Signal = Signal(str)
    node_moved: Signal = Signal(str, float, float)
    edge_added: Signal = Signal(str)
    edge_removed: Signal = Signal(str)
    node_double_clicked: Signal = Signal(str)
    selection_updated: Signal = Signal(list)
    connection_requested: Signal = Signal(
        str, str, str, str
    )  # src_node, src_port, dst_node, dst_port

    def __init__(self, graph: Graph) -> None:
        """Create the scene and populate it from *graph*.

        Args:
            graph: Initial graph to display.
        """
        super().__init__()
        self._node_items: dict[NodeId, NodeItem] = {}
        self._edge_items: dict[EdgeId, EdgeItem] = {}
        self._edge_draft: EdgeDraftItem | None = None
        self._draft_src_node_id: NodeId | None = None
        self._draft_src_port_id: str | None = None
        self.selectionChanged.connect(self._on_selection_changed)
        self.load_graph(graph)

    def load_graph(self, graph: Graph) -> None:
        """Replace all items in the scene with those from *graph*.

        Clears the scene completely before re-populating, so any existing
        `EdgeDraftItem` is also discarded.

        Args:
            graph: The graph to display.
        """
        self.clear()
        self._node_items = {}
        self._edge_items = {}
        self._edge_draft = None
        for node in graph.nodes.values():
            self._create_node_item(node)
        for edge in graph.edges.values():
            self._create_edge_item(edge)

    def add_node_item(self, node: Node) -> None:
        """Add a `NodeItem` for *node* and emit `node_added`.

        Args:
            node: The model node to display.
        """
        self._create_node_item(node)
        self.node_added.emit(node.id)

    def remove_node_item(self, node_id: NodeId) -> None:
        """Remove the `NodeItem` for *node_id* and its connected edges, then emit `node_removed`.

        Args:
            node_id: ID of the node to remove.

        Raises:
            KeyError: If no item exists for *node_id*.
        """
        connected = [
            eid
            for eid, ei in self._edge_items.items()
            if ei._edge.src_node == node_id or ei._edge.dst_node == node_id
        ]
        for eid in connected:
            self.remove_edge_item(eid)
        item = self._node_items.pop(node_id)
        self.removeItem(item)
        self.node_removed.emit(node_id)

    def add_edge_item(self, edge: Edge) -> None:
        """Add an `EdgeItem` for *edge* and emit `edge_added`.

        Both endpoint nodes must already have a `NodeItem` in the scene.

        Args:
            edge: The model edge to display.

        Raises:
            KeyError: If the source or destination node is not in the scene.
        """
        self._create_edge_item(edge)
        self.edge_added.emit(edge.id)

    def remove_edge_item(self, edge_id: EdgeId) -> None:
        """Remove the `EdgeItem` for *edge_id* and emit `edge_removed`.

        Args:
            edge_id: ID of the edge to remove.

        Raises:
            KeyError: If no item exists for *edge_id*.
        """
        item = self._edge_items.pop(edge_id)
        self.removeItem(item)
        self.edge_removed.emit(edge_id)

    def begin_edge_draft(self, src_node_id: NodeId, src_port_id: str) -> None:
        """Start drawing a draft edge from the given port.

        If a draft is already in progress it is cancelled first.

        Args:
            src_node_id: ID of the source node.
            src_port_id: ID of the source port on that node.
        """
        if self._edge_draft is not None:
            self.cancel_edge_draft()
        src_pos = self._node_items[src_node_id].port_center(src_port_id)
        self._edge_draft = EdgeDraftItem(src_pos)
        self._draft_src_node_id = src_node_id
        self._draft_src_port_id = src_port_id
        self.addItem(self._edge_draft)

    def cancel_edge_draft(self) -> None:
        """Remove the current draft edge from the scene, if any."""
        if self._edge_draft is not None:
            self.removeItem(self._edge_draft)
            self._edge_draft = None
            self._draft_src_node_id = None
            self._draft_src_port_id = None

    def complete_edge_draft(self, dst_node_id: NodeId, dst_port_id: str) -> None:
        """Finalise a draft edge by creating a real `EdgeItem`.

        Called when the user releases the mouse over a destination port.
        The draft is removed and a new edge is added via `add_edge_item`.

        Args:
            dst_node_id: ID of the destination node.
            dst_port_id: ID of the destination port on that node.
        """
        if self._edge_draft is None:
            return
        src_node_id = self._draft_src_node_id
        src_port_id = self._draft_src_port_id
        self.cancel_edge_draft()
        if src_node_id is None or src_port_id is None:
            return
        self.connection_requested.emit(src_node_id, src_port_id, dst_node_id, dst_port_id)

    def selected_node_ids(self) -> list[NodeId]:
        """Return the IDs of all currently selected nodes."""
        return [item.node_id() for item in self.selectedItems() if isinstance(item, NodeItem)]

    def _refresh_edges_for_node(self, node_id: NodeId) -> None:
        """Recompute the path of every edge connected to *node_id*.

        Called by `NodeItem.mouseMoveEvent` while dragging.
        """
        for edge_item in self._edge_items.values():
            if edge_item._edge.src_node == node_id or edge_item._edge.dst_node == node_id:
                edge_item.update_path()

    def _create_node_item(self, node: Node) -> None:
        item = NodeItem(node)
        self.addItem(item)
        self._node_items[node.id] = item

    def _create_edge_item(self, edge: Edge) -> None:
        src_item = self._node_items[edge.src_node]
        dst_item = self._node_items[edge.dst_node]
        item = EdgeItem(edge, src_item, dst_item)
        self.addItem(item)
        self._edge_items[edge.id] = item

    def _on_selection_changed(self) -> None:
        self.selection_updated.emit(self.selected_node_ids())
