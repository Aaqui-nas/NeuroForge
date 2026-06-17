from __future__ import annotations

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QBrush, QColor, QFont, QPainter, QPainterPath, QPen, QTransform
from PySide6.QtWidgets import (
    QGraphicsEllipseItem,
    QGraphicsItem,
    QGraphicsPathItem,
    QGraphicsSceneContextMenuEvent,
    QGraphicsSceneMouseEvent,
    QStyle,  # noqa: E402
    QStyleOptionGraphicsItem,
    QWidget,
)

from neuroforge.graph.model import Edge, Node, Port, PortDirection, PortId

PORT_RADIUS = 5.0
NODE_WIDTH = 160.0
NODE_HEADER_HEIGHT = 30.0
NODE_PORT_SPACING = 22.0
BEZIER_TANGENT = 100.0

_COLOR_HEADER = QColor("#4a6fa5")
_COLOR_HEADER_COMPONENT = QColor("#7a3fa0")
_COLOR_BODY = QColor("#2b2b2b")
_COLOR_BORDER = QColor("#666666")
_COLOR_BORDER_SELECTED = QColor("#ffffff")
_COLOR_TEXT = QColor("#ffffff")
_COLOR_PORT_INPUT = QColor("#88aaff")
_COLOR_PORT_OUTPUT = QColor("#ffaa44")
_COLOR_EDGE = QColor("#aaaaaa")
_COLOR_DRAFT = QColor("#ffffff")


class PortItem(QGraphicsEllipseItem):
    """A clickable circle representing one port on a `NodeItem`.

    Positioned by its parent `NodeItem` via `setPos`. The local origin
    ``(0, 0)`` is the center of the circle, so `center` simply maps that
    point to scene coordinates.
    """

    def __init__(self, port: Port, parent: QGraphicsItem) -> None:
        """Create a port circle centered at the item's local origin.

        Args:
            port: The model port this item represents.
            parent: The `NodeItem` that owns this port.
        """
        rect = QRectF(-PORT_RADIUS, -PORT_RADIUS, PORT_RADIUS * 2, PORT_RADIUS * 2)
        super().__init__(rect, parent)
        self._port = port
        color = _COLOR_PORT_INPUT if port.direction is PortDirection.INPUT else _COLOR_PORT_OUTPUT
        self.setBrush(QBrush(color))
        self.setPen(QPen(Qt.GlobalColor.black, 1.0))
        self.setZValue(1)

    def port_id(self) -> PortId:
        """Return the port's unique identifier within its node."""
        return self._port.id

    def center(self) -> QPointF:
        """Return the center of this port in scene coordinates.

        Used by `EdgeItem` and `EdgeDraftItem` to anchor bezier curves.
        """
        return self.mapToScene(QPointF(0.0, 0.0))

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        """Start an edge draft when the user clicks a port."""
        scene = self.scene()
        if scene is not None:
            from neuroforge.ui.graph_editor.scene import GraphScene

            if isinstance(scene, GraphScene):
                parent = self.parentItem()
                if isinstance(parent, NodeItem):
                    scene.begin_edge_draft(parent.node_id(), self._port.id)
        event.accept()

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        scene = self.scene()
        if scene is not None:
            from neuroforge.ui.graph_editor.scene import GraphScene

            if isinstance(scene, GraphScene) and scene._edge_draft is not None:
                scene._edge_draft.update_end(event.scenePos())
        event.accept()

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        scene = self.scene()
        if scene is not None:
            from neuroforge.ui.graph_editor.scene import GraphScene

            if isinstance(scene, GraphScene) and scene._edge_draft is not None:
                hit = scene.itemAt(event.scenePos(), QTransform())
                if isinstance(hit, PortItem) and hit is not self:
                    parent = hit.parentItem()
                    if isinstance(parent, NodeItem):
                        scene.complete_edge_draft(parent.node_id(), hit.port_id())
                else:
                    scene.cancel_edge_draft()
        event.accept()


def _node_height(node: Node) -> float:
    """Compute node height from its port count.

    Height = header + max(n_inputs, n_outputs) rows, at least one row.
    """
    n_in = sum(1 for p in node.ports.values() if p.direction is PortDirection.INPUT)
    n_out = sum(1 for p in node.ports.values() if p.direction is PortDirection.OUTPUT)
    return NODE_HEADER_HEIGHT + max(n_in, n_out, 1) * NODE_PORT_SPACING


class NodeItem(QGraphicsItem):
    """Visual representation of a `Node` in the graph editor.

    Input ports are placed on the left edge, output ports on the right.
    The item is movable and selectable; dragging emits ``node_moved`` on
    the parent `GraphScene`.

    Coordinates: the local origin ``(0, 0)`` is the top-left corner of
    the node body.
    """

    def __init__(self, node: Node) -> None:
        """Build the node item and all its child `PortItem` instances.

        Args:
            node: The model node this item represents.
        """
        super().__init__()
        self._node = node
        self._port_items: dict[PortId, PortItem] = {}

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemUsesExtendedStyleOption)

        self.setPos(node.position[0], node.position[1])
        self._build_port_items()

    def _build_port_items(self) -> None:
        """Create and position one `PortItem` per port in the model node.

        Input ports are stacked on the left edge (x=0), output ports on
        the right edge (x=NODE_WIDTH), starting below the header.
        """
        inputs = [p for p in self._node.ports.values() if p.direction is PortDirection.INPUT]
        outputs = [p for p in self._node.ports.values() if p.direction is PortDirection.OUTPUT]
        for i, port in enumerate(inputs):
            item = PortItem(port, self)
            item.setPos(0.0, NODE_HEADER_HEIGHT + (i + 0.5) * NODE_PORT_SPACING)
            self._port_items[port.id] = item
        for i, port in enumerate(outputs):
            item = PortItem(port, self)
            item.setPos(NODE_WIDTH, NODE_HEADER_HEIGHT + (i + 0.5) * NODE_PORT_SPACING)
            self._port_items[port.id] = item

    def node_id(self) -> str:
        """Return the model node's unique identifier."""
        return self._node.id

    def boundingRect(self) -> QRectF:
        """Return the bounding rectangle of the node body.

        Required by Qt — defines the area that needs to be repainted and
        handles hit-testing for mouse events.
        """
        return QRectF(0, 0, NODE_WIDTH, _node_height(self._node))

    def paint(
        self,
        painter: QPainter,
        option: QStyleOptionGraphicsItem,
        widget: QWidget | None = None,
    ) -> None:
        """Draw the node: body, header, title, and port labels.

        Qt calls this whenever the item needs to be repainted. Child
        `PortItem` instances paint themselves automatically.
        """
        rect = self.boundingRect()
        selected = bool(option.state & QStyle.StateFlag.State_Selected)

        painter.setBrush(QBrush(_COLOR_BODY))
        painter.setPen(QPen(_COLOR_BORDER_SELECTED if selected else _COLOR_BORDER, 1.5))
        painter.drawRoundedRect(rect, 4.0, 4.0)

        header_rect = QRectF(0, 0, NODE_WIDTH, NODE_HEADER_HEIGHT)
        header_color = _COLOR_HEADER_COMPONENT if self._node.component_id else _COLOR_HEADER
        painter.setBrush(QBrush(header_color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(header_rect, 4.0, 4.0)
        painter.drawRect(QRectF(0, NODE_HEADER_HEIGHT / 2, NODE_WIDTH, NODE_HEADER_HEIGHT / 2))

        painter.setPen(QPen(_COLOR_TEXT))
        font = QFont()
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(header_rect, Qt.AlignmentFlag.AlignCenter, self._node.name)

        font.setBold(False)
        painter.setFont(font)
        painter.setPen(QPen(_COLOR_TEXT))
        inputs = [p for p in self._node.ports.values() if p.direction is PortDirection.INPUT]
        outputs = [p for p in self._node.ports.values() if p.direction is PortDirection.OUTPUT]
        for i, port in enumerate(inputs):
            y = NODE_HEADER_HEIGHT + (i + 0.5) * NODE_PORT_SPACING
            label = QRectF(8, y - NODE_PORT_SPACING / 2, NODE_WIDTH / 2 - 8, NODE_PORT_SPACING)
            painter.drawText(
                label, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, port.name
            )
        for i, port in enumerate(outputs):
            y = NODE_HEADER_HEIGHT + (i + 0.5) * NODE_PORT_SPACING
            label = QRectF(
                NODE_WIDTH / 2, y - NODE_PORT_SPACING / 2, NODE_WIDTH / 2 - 8, NODE_PORT_SPACING
            )
            painter.drawText(
                label, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight, port.name
            )

    def port_item(self, port_id: PortId) -> PortItem:
        """Return the `PortItem` for *port_id*.

        Args:
            port_id: The port identifier to look up.

        Raises:
            KeyError: If no port with that ID exists on this node.
        """
        if port_id not in self._port_items:
            raise KeyError(f"No port {port_id!r} on node {self._node.id!r}")
        return self._port_items[port_id]

    def port_center(self, port_id: PortId) -> QPointF:
        """Return the scene-coordinate center of the given port.

        Args:
            port_id: The port identifier to look up.
        """
        return self.port_item(port_id).center()

    def set_position(self, x: float, y: float) -> None:
        """Move the node to *(x, y)* in scene coordinates.

        Args:
            x: Horizontal position.
            y: Vertical position.
        """
        self.setPos(x, y)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        super().mouseMoveEvent(event)
        scene = self.scene()
        if scene is not None:
            from neuroforge.ui.graph_editor.scene import GraphScene

            if isinstance(scene, GraphScene):
                scene._refresh_edges_for_node(self._node.id)

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        super().mouseReleaseEvent(event)
        scene = self.scene()
        if scene is not None:
            from neuroforge.ui.graph_editor.scene import GraphScene

            if isinstance(scene, GraphScene):
                scene.node_moved.emit(self._node.id, self.x(), self.y())

    def mouseDoubleClickEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        """Emit ``node_double_clicked`` on the scene when the node is double-clicked."""
        scene = self.scene()
        if scene is not None:
            from neuroforge.ui.graph_editor.scene import GraphScene

            if isinstance(scene, GraphScene):
                scene.node_double_clicked.emit(self._node.id)
        event.accept()

    def contextMenuEvent(self, event: QGraphicsSceneContextMenuEvent) -> None:
        """Show a context menu with a delete action."""
        from PySide6.QtWidgets import QMenu

        menu = QMenu()
        delete_action = menu.addAction("Supprimer")
        if menu.exec(event.screenPos()) is delete_action:
            scene = self.scene()
            if scene is not None:
                from neuroforge.ui.graph_editor.scene import GraphScene

                if isinstance(scene, GraphScene):
                    scene.remove_node_item(self._node.id)
        event.accept()


class EdgeItem(QGraphicsPathItem):
    """A cubic Bézier curve connecting two ports in the graph editor.

    The curve is recomputed via `update_path` whenever either endpoint
    node moves.
    """

    def __init__(self, edge: Edge, src_item: NodeItem, dst_item: NodeItem) -> None:
        """Create the edge and draw its initial path.

        Args:
            edge: The model edge this item represents.
            src_item: The `NodeItem` that owns the source port.
            dst_item: The `NodeItem` that owns the destination port.
        """
        super().__init__()
        self._edge = edge
        self._src_item = src_item
        self._dst_item = dst_item
        self.setPen(QPen(_COLOR_EDGE, 2.0))
        self.setZValue(-1)
        self.update_path()

    def edge_id(self) -> str:
        """Return the model edge's unique identifier."""
        return self._edge.id

    def update_path(self) -> None:
        """Recompute the Bézier curve from the current port positions.

        Should be called whenever a connected node moves.
        """
        p0 = self._src_item.port_center(self._edge.src_port)
        p3 = self._dst_item.port_center(self._edge.dst_port)
        self.setPath(self._bezier_path(p0, p3))

    def _bezier_path(self, p0: QPointF, p3: QPointF) -> QPainterPath:
        """Build a cubic Bézier path from *p0* to *p3*.

        Tangent handles are offset horizontally by `BEZIER_TANGENT` so that
        curves entering and leaving ports always do so horizontally.

        Args:
            p0: Start point (source port center, scene coordinates).
            p3: End point (destination port center, scene coordinates).

        Returns:
            A `QPainterPath` containing a single cubic segment.
        """
        path = QPainterPath(p0)
        p1 = QPointF(p0.x() + BEZIER_TANGENT, p0.y())
        p2 = QPointF(p3.x() - BEZIER_TANGENT, p3.y())
        path.cubicTo(p1, p2, p3)
        return path


_DRAFT_PEN = QPen(_COLOR_DRAFT, 2.0, Qt.PenStyle.DashLine)


class EdgeDraftItem(QGraphicsPathItem):
    """A temporary dashed Bézier curve drawn while the user drags a new edge.

    Created by `GraphScene.begin_edge_draft` and removed by
    `GraphScene.cancel_edge_draft` or when the edge is confirmed.
    """

    def __init__(self, src_pos: QPointF) -> None:
        """Create the draft anchored at *src_pos*.

        Args:
            src_pos: Scene-coordinate position of the source port.
        """
        super().__init__()
        self._src_pos = src_pos
        self.setPen(_DRAFT_PEN)
        self.setZValue(-1)
        self.update_end(src_pos)

    def update_end(self, dst_pos: QPointF) -> None:
        """Redraw the draft curve to end at *dst_pos*.

        Called on every mouse-move event while dragging.

        Args:
            dst_pos: Current mouse position in scene coordinates.
        """
        path = QPainterPath(self._src_pos)
        p1 = QPointF(self._src_pos.x() + BEZIER_TANGENT, self._src_pos.y())
        p2 = QPointF(dst_pos.x() - BEZIER_TANGENT, dst_pos.y())
        path.cubicTo(p1, p2, dst_pos)
        self.setPath(path)
