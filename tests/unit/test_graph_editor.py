from __future__ import annotations

import pytest
from pytestqt.qtbot import QtBot

from neuroforge.graph.model import DataType, Edge, Graph, Node, Port, PortDirection
from neuroforge.ui.graph_editor.items import (
    BEZIER_TANGENT,
    NODE_HEADER_HEIGHT,
    NODE_PORT_SPACING,
    NODE_WIDTH,
    EdgeDraftItem,
    EdgeItem,
    NodeItem,
    PortItem,
)
from neuroforge.ui.graph_editor.scene import GraphScene
from neuroforge.ui.graph_editor.view import ZOOM_MAX, ZOOM_MIN, GraphView

# ── Helpers ───────────────────────────────────────────────────────────────────


def make_port(pid: str, direction: PortDirection = PortDirection.INPUT) -> Port:
    return Port(id=pid, name=pid, direction=direction, data_type=DataType.TENSOR, required=True)


def make_node(nid: str, ports: dict[str, Port] | None = None) -> Node:
    return Node(id=nid, type="linear", name=nid, position=(0.0, 0.0), ports=ports or {}, params={})


def make_edge(eid: str, src: str, src_port: str, dst: str, dst_port: str) -> Edge:
    return Edge(id=eid, src_node=src, src_port=src_port, dst_node=dst, dst_port=dst_port)


def two_node_graph() -> Graph:
    """Graph with two connected nodes: a[out] → b[in]."""
    g = Graph()
    g.add_node(make_node("a", {"out": make_port("out", PortDirection.OUTPUT)}))
    g.add_node(make_node("b", {"in": make_port("in", PortDirection.INPUT)}))
    g.add_edge(make_edge("e1", "a", "out", "b", "in"))
    return g


# ── NodeItem ──────────────────────────────────────────────────────────────────


class TestNodeItem:
    def test_node_id_matches_model(self, qtbot: QtBot) -> None:
        node = make_node("n1", {"in": make_port("in")})
        item = NodeItem(node)
        assert item.node_id() == "n1"

    def test_bounding_rect_width(self, qtbot: QtBot) -> None:
        node = make_node("n1", {"in": make_port("in")})
        item = NodeItem(node)
        assert item.boundingRect().width() == NODE_WIDTH

    def test_bounding_rect_height_scales_with_port_count(self, qtbot: QtBot) -> None:
        ports = {f"p{i}": make_port(f"p{i}") for i in range(3)}
        item = NodeItem(make_node("n1", ports))
        expected_min = NODE_HEADER_HEIGHT + 3 * NODE_PORT_SPACING
        assert item.boundingRect().height() >= expected_min

    def test_port_item_returns_port_item(self, qtbot: QtBot) -> None:
        node = make_node("n1", {"in": make_port("in")})
        item = NodeItem(node)
        assert isinstance(item.port_item("in"), PortItem)

    def test_port_item_unknown_raises(self, qtbot: QtBot) -> None:
        item = NodeItem(make_node("n1", {"in": make_port("in")}))
        with pytest.raises(KeyError):
            item.port_item("nonexistent")

    def test_port_center_returns_qpointf(self, qtbot: QtBot) -> None:
        from PySide6.QtCore import QPointF

        node = make_node("n1", {"in": make_port("in")})
        item = NodeItem(node)
        assert isinstance(item.port_center("in"), QPointF)

    def test_set_position_moves_item(self, qtbot: QtBot) -> None:
        item = NodeItem(make_node("n1"))
        item.set_position(42.0, 99.0)
        assert item.x() == pytest.approx(42.0)
        assert item.y() == pytest.approx(99.0)


# ── PortItem ──────────────────────────────────────────────────────────────────


class TestPortItem:
    def _make_parent(self) -> NodeItem:
        return NodeItem(make_node("n1", {"in": make_port("in")}))

    def test_port_id_matches_model(self, qtbot: QtBot) -> None:
        parent = self._make_parent()
        port = make_port("in")
        item = PortItem(port, parent)
        assert item.port_id() == "in"

    def test_center_returns_qpointf(self, qtbot: QtBot) -> None:
        from PySide6.QtCore import QPointF

        parent = self._make_parent()
        item = PortItem(make_port("in"), parent)
        assert isinstance(item.center(), QPointF)


# ── EdgeItem ──────────────────────────────────────────────────────────────────


class TestEdgeItem:
    def test_edge_id_matches_model(self, qtbot: QtBot) -> None:
        src = NodeItem(make_node("a", {"out": make_port("out", PortDirection.OUTPUT)}))
        dst = NodeItem(make_node("b", {"in": make_port("in")}))
        edge = make_edge("e1", "a", "out", "b", "in")
        item = EdgeItem(edge, src, dst)
        assert item.edge_id() == "e1"

    def test_update_path_produces_non_empty_path(self, qtbot: QtBot) -> None:
        src = NodeItem(make_node("a", {"out": make_port("out", PortDirection.OUTPUT)}))
        dst = NodeItem(make_node("b", {"in": make_port("in")}))
        edge = make_edge("e1", "a", "out", "b", "in")
        item = EdgeItem(edge, src, dst)
        item.update_path()
        assert not item.path().isEmpty()


# ── EdgeDraftItem ─────────────────────────────────────────────────────────────


class TestEdgeDraftItem:
    def test_update_end_produces_non_empty_path(self, qtbot: QtBot) -> None:
        from PySide6.QtCore import QPointF

        draft = EdgeDraftItem(QPointF(0.0, 0.0))
        draft.update_end(QPointF(200.0, 100.0))
        assert not draft.path().isEmpty()

    def test_bezier_tangent_offset_applied(self, qtbot: QtBot) -> None:
        from PySide6.QtCore import QPointF

        src = QPointF(0.0, 0.0)
        dst = QPointF(200.0, 0.0)
        draft = EdgeDraftItem(src)
        draft.update_end(dst)
        # Path must span at least BEZIER_TANGENT in x to confirm tangents are used.
        rect = draft.path().boundingRect()
        assert rect.width() >= BEZIER_TANGENT


# ── GraphScene ────────────────────────────────────────────────────────────────


class TestGraphScene:
    def test_init_adds_node_items_from_graph(self, qtbot: QtBot) -> None:
        scene = GraphScene(two_node_graph())
        node_items = [i for i in scene.items() if isinstance(i, NodeItem)]
        assert len(node_items) == 2

    def test_init_adds_edge_items_from_graph(self, qtbot: QtBot) -> None:
        scene = GraphScene(two_node_graph())
        edge_items = [i for i in scene.items() if isinstance(i, EdgeItem)]
        assert len(edge_items) == 1

    def test_add_node_item_increases_item_count(self, qtbot: QtBot) -> None:
        scene = GraphScene(Graph())
        scene.add_node_item(make_node("n1"))
        node_items = [i for i in scene.items() if isinstance(i, NodeItem)]
        assert len(node_items) == 1

    def test_add_node_item_emits_signal(self, qtbot: QtBot) -> None:
        scene = GraphScene(Graph())
        with qtbot.waitSignal(scene.node_added, timeout=500) as sig:
            scene.add_node_item(make_node("n1"))
        assert sig.args == ["n1"]

    def test_remove_node_item_decreases_item_count(self, qtbot: QtBot) -> None:
        scene = GraphScene(Graph())
        scene.add_node_item(make_node("n1"))
        scene.remove_node_item("n1")
        node_items = [i for i in scene.items() if isinstance(i, NodeItem)]
        assert len(node_items) == 0

    def test_remove_node_item_emits_signal(self, qtbot: QtBot) -> None:
        scene = GraphScene(Graph())
        scene.add_node_item(make_node("n1"))
        with qtbot.waitSignal(scene.node_removed, timeout=500) as sig:
            scene.remove_node_item("n1")
        assert sig.args == ["n1"]

    def test_add_edge_item_requires_existing_node_items(self, qtbot: QtBot) -> None:
        scene = GraphScene(Graph())
        scene.add_node_item(make_node("a", {"out": make_port("out", PortDirection.OUTPUT)}))
        scene.add_node_item(make_node("b", {"in": make_port("in")}))
        scene.add_edge_item(make_edge("e1", "a", "out", "b", "in"))
        edge_items = [i for i in scene.items() if isinstance(i, EdgeItem)]
        assert len(edge_items) == 1

    def test_add_edge_item_emits_signal(self, qtbot: QtBot) -> None:
        scene = GraphScene(Graph())
        scene.add_node_item(make_node("a", {"out": make_port("out", PortDirection.OUTPUT)}))
        scene.add_node_item(make_node("b", {"in": make_port("in")}))
        with qtbot.waitSignal(scene.edge_added, timeout=500) as sig:
            scene.add_edge_item(make_edge("e1", "a", "out", "b", "in"))
        assert sig.args == ["e1"]

    def test_remove_edge_item_emits_signal(self, qtbot: QtBot) -> None:
        scene = GraphScene(two_node_graph())
        with qtbot.waitSignal(scene.edge_removed, timeout=500) as sig:
            scene.remove_edge_item("e1")
        assert sig.args == ["e1"]

    def test_begin_edge_draft_adds_draft_item(self, qtbot: QtBot) -> None:
        scene = GraphScene(Graph())
        scene.add_node_item(make_node("a", {"out": make_port("out", PortDirection.OUTPUT)}))
        scene.begin_edge_draft("a", "out")
        draft_items = [i for i in scene.items() if isinstance(i, EdgeDraftItem)]
        assert len(draft_items) == 1

    def test_cancel_edge_draft_removes_draft_item(self, qtbot: QtBot) -> None:
        scene = GraphScene(Graph())
        scene.add_node_item(make_node("a", {"out": make_port("out", PortDirection.OUTPUT)}))
        scene.begin_edge_draft("a", "out")
        scene.cancel_edge_draft()
        draft_items = [i for i in scene.items() if isinstance(i, EdgeDraftItem)]
        assert len(draft_items) == 0

    def test_selected_node_ids_returns_empty_by_default(self, qtbot: QtBot) -> None:
        scene = GraphScene(two_node_graph())
        assert scene.selected_node_ids() == []

    def test_load_graph_replaces_existing_items(self, qtbot: QtBot) -> None:
        scene = GraphScene(two_node_graph())
        new_graph = Graph()
        new_graph.add_node(make_node("x"))
        scene.load_graph(new_graph)
        node_items = [i for i in scene.items() if isinstance(i, NodeItem)]
        assert len(node_items) == 1
        assert node_items[0].node_id() == "x"


# ── GraphView ─────────────────────────────────────────────────────────────────


class TestGraphView:
    def make_view(self, qtbot: QtBot) -> GraphView:
        scene = GraphScene(Graph())
        view = GraphView(scene)
        qtbot.addWidget(view)
        return view

    def test_zoom_in_increases_scale(self, qtbot: QtBot) -> None:
        view = self.make_view(qtbot)
        before = view.transform().m11()
        view.zoom_in()
        assert view.transform().m11() > before

    def test_zoom_out_decreases_scale(self, qtbot: QtBot) -> None:
        view = self.make_view(qtbot)
        before = view.transform().m11()
        view.zoom_out()
        assert view.transform().m11() < before

    def test_zoom_reset_restores_identity_scale(self, qtbot: QtBot) -> None:
        view = self.make_view(qtbot)
        view.zoom_in()
        view.zoom_in()
        view.zoom_reset()
        assert view.transform().m11() == pytest.approx(1.0)

    def test_zoom_clamped_at_minimum(self, qtbot: QtBot) -> None:
        view = self.make_view(qtbot)
        for _ in range(100):
            view.zoom_out()
        assert view.transform().m11() >= ZOOM_MIN

    def test_zoom_clamped_at_maximum(self, qtbot: QtBot) -> None:
        view = self.make_view(qtbot)
        for _ in range(100):
            view.zoom_in()
        assert view.transform().m11() <= ZOOM_MAX
