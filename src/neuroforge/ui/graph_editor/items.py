# mypy: disable-error-code="empty-body"
from __future__ import annotations

from PySide6.QtCore import QPointF, QRectF
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import (
    QGraphicsEllipseItem,
    QGraphicsItem,
    QGraphicsPathItem,
    QGraphicsSceneContextMenuEvent,
    QGraphicsSceneMouseEvent,
    QStyleOptionGraphicsItem,
    QWidget,
)

from neuroforge.graph.model import Edge, Node, Port, PortId

PORT_RADIUS = 5.0
NODE_WIDTH = 160.0
NODE_HEADER_HEIGHT = 30.0
NODE_PORT_SPACING = 22.0
BEZIER_TANGENT = 100.0


class PortItem(QGraphicsEllipseItem):
    def __init__(self, port: Port, parent: QGraphicsItem) -> None: ...

    def port_id(self) -> PortId: ...

    def center(self) -> QPointF: ...

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None: ...

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None: ...


class NodeItem(QGraphicsItem):
    def __init__(self, node: Node) -> None: ...

    def node_id(self) -> str: ...

    def boundingRect(self) -> QRectF: ...

    def paint(
        self,
        painter: QPainter,
        option: QStyleOptionGraphicsItem,
        widget: QWidget | None = None,
    ) -> None: ...

    def port_item(self, port_id: PortId) -> PortItem: ...

    def port_center(self, port_id: PortId) -> QPointF: ...

    def set_position(self, x: float, y: float) -> None: ...

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None: ...

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None: ...

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None: ...

    def mouseDoubleClickEvent(self, event: QGraphicsSceneMouseEvent) -> None: ...

    def contextMenuEvent(self, event: QGraphicsSceneContextMenuEvent) -> None: ...


class EdgeItem(QGraphicsPathItem):
    def __init__(self, edge: Edge, src_item: NodeItem, dst_item: NodeItem) -> None: ...

    def edge_id(self) -> str: ...

    def update_path(self) -> None: ...

    def _bezier_path(self, p0: QPointF, p3: QPointF) -> None: ...


class EdgeDraftItem(QGraphicsPathItem):
    def __init__(self, src_pos: QPointF) -> None: ...

    def update_end(self, dst_pos: QPointF) -> None: ...
