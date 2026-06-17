from __future__ import annotations

import pytest

from neuroforge.graph.model import (
    DataType,
    Edge,
    Graph,
    Node,
    Port,
    PortDirection,
)

# ── Fixtures ─────────────────────────────────────────────────────────────────


def make_node(node_id: str, **kwargs: object) -> Node:
    return Node(
        id=node_id,
        type="linear",
        name=kwargs.get("name", node_id),  # type: ignore[arg-type]
        position=(0.0, 0.0),
        ports={},
        params={},
    )


def make_edge(edge_id: str, src: str, dst: str) -> Edge:
    return Edge(
        id=edge_id,
        src_node=src,
        src_port="out",
        dst_node=dst,
        dst_port="in",
    )


def make_port(port_id: str, direction: PortDirection = PortDirection.INPUT) -> Port:
    return Port(
        id=port_id,
        name=port_id,
        direction=direction,
        data_type=DataType.TENSOR,
        required=True,
    )


# ── Graph.add_node ────────────────────────────────────────────────────────────


def test_add_node_stores_node() -> None:
    g = Graph()
    n = make_node("a")
    g.add_node(n)
    assert "a" in g.nodes


def test_add_node_duplicate_is_ignored() -> None:
    g = Graph()
    n1 = make_node("a", name="first")
    n2 = make_node("a", name="second")
    g.add_node(n1)
    g.add_node(n2)
    assert g.nodes["a"].name == "first"


def test_add_node_increments_count() -> None:
    g = Graph()
    g.add_node(make_node("a"))
    g.add_node(make_node("b"))
    assert len(g.nodes) == 2


# ── Graph.remove_node ─────────────────────────────────────────────────────────


def test_remove_node_deletes_node() -> None:
    g = Graph()
    g.add_node(make_node("a"))
    g.remove_node("a")
    assert "a" not in g.nodes


def test_remove_node_returns_empty_for_unknown_id() -> None:
    g = Graph()
    assert g.remove_node("ghost") == []


def test_remove_node_cascades_outgoing_edges() -> None:
    g = Graph()
    g.add_node(make_node("a"))
    g.add_node(make_node("b"))
    g.add_edge(make_edge("e1", "a", "b"))
    g.remove_node("a")
    assert "e1" not in g.edges


def test_remove_node_cascades_incoming_edges() -> None:
    g = Graph()
    g.add_node(make_node("a"))
    g.add_node(make_node("b"))
    g.add_edge(make_edge("e1", "a", "b"))
    g.remove_node("b")
    assert "e1" not in g.edges


def test_remove_node_returns_cascaded_edge_ids() -> None:
    g = Graph()
    g.add_node(make_node("a"))
    g.add_node(make_node("b"))
    g.add_node(make_node("c"))
    g.add_edge(make_edge("e1", "a", "b"))
    g.add_edge(make_edge("e2", "b", "c"))
    removed = g.remove_node("b")
    assert set(removed) == {"e1", "e2"}


def test_remove_node_only_removes_connected_edges() -> None:
    g = Graph()
    g.add_node(make_node("a"))
    g.add_node(make_node("b"))
    g.add_node(make_node("c"))
    g.add_edge(make_edge("e1", "a", "b"))
    g.add_edge(make_edge("e2", "b", "c"))
    g.remove_node("a")
    assert "e2" in g.edges


# ── Graph.add_edge / remove_edge ──────────────────────────────────────────────


def test_add_edge_stores_edge() -> None:
    g = Graph()
    g.add_edge(make_edge("e1", "a", "b"))
    assert "e1" in g.edges


def test_add_edge_duplicate_is_ignored() -> None:
    g = Graph()
    g.add_edge(make_edge("e1", "a", "b"))
    g.add_edge(make_edge("e1", "x", "y"))
    assert g.edges["e1"].src_node == "a"


def test_remove_edge_deletes_edge() -> None:
    g = Graph()
    g.add_edge(make_edge("e1", "a", "b"))
    g.remove_edge("e1")
    assert "e1" not in g.edges


def test_remove_edge_unknown_id_is_noop() -> None:
    g = Graph()
    g.remove_edge("ghost")  # must not raise


# ── Graph.get_node / get_edge ─────────────────────────────────────────────────


def test_get_node_returns_node() -> None:
    g = Graph()
    n = make_node("a")
    g.add_node(n)
    assert g.get_node("a") is n


def test_get_node_returns_none_for_missing() -> None:
    g = Graph()
    assert g.get_node("ghost") is None


def test_get_edge_returns_edge() -> None:
    g = Graph()
    e = make_edge("e1", "a", "b")
    g.add_edge(e)
    assert g.get_edge("e1") is e


def test_get_edge_returns_none_for_missing() -> None:
    g = Graph()
    assert g.get_edge("ghost") is None


# ── Graph.edges_from / edges_to ───────────────────────────────────────────────


def test_edges_from_returns_outgoing() -> None:
    g = Graph()
    g.add_edge(make_edge("e1", "a", "b"))
    g.add_edge(make_edge("e2", "a", "c"))
    g.add_edge(make_edge("e3", "b", "c"))
    result = {e.id for e in g.edges_from("a")}
    assert result == {"e1", "e2"}


def test_edges_from_returns_empty_when_none() -> None:
    g = Graph()
    g.add_edge(make_edge("e1", "a", "b"))
    assert g.edges_from("b") == []


def test_edges_to_returns_incoming() -> None:
    g = Graph()
    g.add_edge(make_edge("e1", "a", "c"))
    g.add_edge(make_edge("e2", "b", "c"))
    g.add_edge(make_edge("e3", "a", "b"))
    result = {e.id for e in g.edges_to("c")}
    assert result == {"e1", "e2"}


def test_edges_to_returns_empty_when_none() -> None:
    g = Graph()
    g.add_edge(make_edge("e1", "a", "b"))
    assert g.edges_to("a") == []


# ── Graph.topological_order ───────────────────────────────────────────────────


def test_topological_order_empty_graph() -> None:
    assert Graph().topological_order() == []


def test_topological_order_single_node() -> None:
    g = Graph()
    g.add_node(make_node("a"))
    assert g.topological_order() == ["a"]


def test_topological_order_linear_chain() -> None:
    g = Graph()
    for nid in ("a", "b", "c"):
        g.add_node(make_node(nid))
    g.add_edge(make_edge("e1", "a", "b"))
    g.add_edge(make_edge("e2", "b", "c"))
    order = g.topological_order()
    assert order.index("a") < order.index("b") < order.index("c")


def test_topological_order_diamond() -> None:
    # a → b, a → c, b → d, c → d
    g = Graph()
    for nid in ("a", "b", "c", "d"):
        g.add_node(make_node(nid))
    g.add_edge(make_edge("e1", "a", "b"))
    g.add_edge(make_edge("e2", "a", "c"))
    g.add_edge(make_edge("e3", "b", "d"))
    g.add_edge(make_edge("e4", "c", "d"))
    order = g.topological_order()
    assert order.index("a") < order.index("b")
    assert order.index("a") < order.index("c")
    assert order.index("b") < order.index("d")
    assert order.index("c") < order.index("d")


def test_topological_order_includes_all_nodes() -> None:
    g = Graph()
    for nid in ("a", "b", "c"):
        g.add_node(make_node(nid))
    g.add_edge(make_edge("e1", "a", "b"))
    g.add_edge(make_edge("e2", "b", "c"))
    assert set(g.topological_order()) == {"a", "b", "c"}


def test_topological_order_raises_on_cycle() -> None:
    g = Graph()
    g.add_node(make_node("a"))
    g.add_node(make_node("b"))
    g.add_edge(make_edge("e1", "a", "b"))
    g.add_edge(make_edge("e2", "b", "a"))
    with pytest.raises(ValueError, match="cycle"):
        g.topological_order()


def test_topological_order_raises_on_self_loop() -> None:
    g = Graph()
    g.add_node(make_node("a"))
    g.add_edge(make_edge("e1", "a", "a"))
    with pytest.raises(ValueError, match="cycle"):
        g.topological_order()


# ── Port ──────────────────────────────────────────────────────────────────────


def test_port_stores_all_fields() -> None:
    p = make_port("p1", PortDirection.OUTPUT)
    assert p.id == "p1"
    assert p.direction == PortDirection.OUTPUT
    assert p.data_type == DataType.TENSOR
    assert p.required is True
