from __future__ import annotations

from neuroforge.graph.model import DataType, Edge, Graph, Node, Port, PortDirection
from neuroforge.graph.validator import GraphValidator, ValidationError

# ── Helpers ───────────────────────────────────────────────────────────────────


def make_node(nid: str, ports: dict[str, Port] | None = None) -> Node:
    return Node(id=nid, type="linear", name=nid, position=(0.0, 0.0), ports=ports or {}, params={})


def make_port(
    pid: str, direction: PortDirection, data_type: DataType = DataType.TENSOR, required: bool = True
) -> Port:
    return Port(id=pid, name=pid, direction=direction, data_type=data_type, required=required)


def make_edge(eid: str, src: str, src_port: str, dst: str, dst_port: str) -> Edge:
    return Edge(id=eid, src_node=src, src_port=src_port, dst_node=dst, dst_port=dst_port)


def linear_graph() -> Graph:
    """a[out] → b[in] → c[in] — valid 3-node chain."""
    g = Graph()
    g.add_node(make_node("a", {"out": make_port("out", PortDirection.OUTPUT)}))
    g.add_node(
        make_node(
            "b",
            {
                "in": make_port("in", PortDirection.INPUT),
                "out": make_port("out", PortDirection.OUTPUT),
            },
        )
    )
    g.add_node(make_node("c", {"in": make_port("in", PortDirection.INPUT)}))
    g.add_edge(make_edge("e1", "a", "out", "b", "in"))
    g.add_edge(make_edge("e2", "b", "out", "c", "in"))
    return g


def error_codes(errors: list[ValidationError]) -> set[str]:
    return {e.code for e in errors}


# ── validate (full pass) ──────────────────────────────────────────────────────


def test_valid_graph_passes() -> None:
    assert GraphValidator().validate(linear_graph()).is_valid


def test_empty_graph_is_valid() -> None:
    assert GraphValidator().validate(Graph()).is_valid


def test_single_node_no_ports_is_valid() -> None:
    g = Graph()
    g.add_node(make_node("a"))
    assert GraphValidator().validate(g).is_valid


def test_invalid_graph_returns_errors() -> None:
    g = Graph()
    g.add_node(make_node("a"))
    g.add_edge(make_edge("e1", "a", "out", "ghost", "in"))
    result = GraphValidator().validate(g)
    assert not result.is_valid
    assert len(result.errors) > 0


def test_semantic_checks_skipped_when_orphan_edges_present() -> None:
    g = Graph()
    g.add_node(make_node("a", {"out": make_port("out", PortDirection.OUTPUT)}))
    g.add_edge(make_edge("e1", "a", "out", "missing", "in"))
    result = GraphValidator().validate(g)
    codes = error_codes(result.errors)
    assert "ORPHAN_EDGE" in codes
    assert "REQUIRED_PORT_UNCONNECTED" not in codes


# ── _check_no_orphan_edges ────────────────────────────────────────────────────


def test_orphan_src_node_detected() -> None:
    g = Graph()
    g.add_node(make_node("b"))
    g.add_edge(make_edge("e1", "ghost", "out", "b", "in"))
    errors = GraphValidator()._check_no_orphan_edges(g)
    assert any(e.code == "ORPHAN_EDGE" for e in errors)


def test_orphan_dst_node_detected() -> None:
    g = Graph()
    g.add_node(make_node("a"))
    g.add_edge(make_edge("e1", "a", "out", "ghost", "in"))
    errors = GraphValidator()._check_no_orphan_edges(g)
    assert any(e.code == "ORPHAN_EDGE" for e in errors)


def test_no_orphan_edges_on_valid_graph() -> None:
    assert GraphValidator()._check_no_orphan_edges(linear_graph()) == []


# ── _check_no_cycles ──────────────────────────────────────────────────────────


def test_cycle_detected() -> None:
    g = Graph()
    g.add_node(make_node("a"))
    g.add_node(make_node("b"))
    g.add_edge(make_edge("e1", "a", "out", "b", "in"))
    g.add_edge(make_edge("e2", "b", "out", "a", "in"))
    errors = GraphValidator()._check_no_cycles(g)
    assert any(e.code == "CYCLE" for e in errors)


def test_self_loop_detected() -> None:
    g = Graph()
    g.add_node(make_node("a"))
    g.add_edge(make_edge("e1", "a", "out", "a", "in"))
    errors = GraphValidator()._check_no_cycles(g)
    assert any(e.code == "CYCLE" for e in errors)


def test_no_cycle_on_valid_graph() -> None:
    assert GraphValidator()._check_no_cycles(linear_graph()) == []


# ── _check_type_compatibility ─────────────────────────────────────────────────


def test_incompatible_types_detected() -> None:
    g = Graph()
    g.add_node(make_node("a", {"out": make_port("out", PortDirection.OUTPUT, DataType.TENSOR)}))
    g.add_node(make_node("b", {"in": make_port("in", PortDirection.INPUT, DataType.INT)}))
    g.add_edge(make_edge("e1", "a", "out", "b", "in"))
    errors = GraphValidator()._check_type_compatibility(g)
    assert any(e.code == "TYPE_MISMATCH" for e in errors)


def test_same_types_compatible() -> None:
    g = Graph()
    g.add_node(make_node("a", {"out": make_port("out", PortDirection.OUTPUT, DataType.TENSOR)}))
    g.add_node(make_node("b", {"in": make_port("in", PortDirection.INPUT, DataType.TENSOR)}))
    g.add_edge(make_edge("e1", "a", "out", "b", "in"))
    assert GraphValidator()._check_type_compatibility(g) == []


def test_any_src_is_compatible_with_any_dst() -> None:
    g = Graph()
    g.add_node(make_node("a", {"out": make_port("out", PortDirection.OUTPUT, DataType.ANY)}))
    g.add_node(make_node("b", {"in": make_port("in", PortDirection.INPUT, DataType.INT)}))
    g.add_edge(make_edge("e1", "a", "out", "b", "in"))
    assert GraphValidator()._check_type_compatibility(g) == []


def test_any_dst_accepts_any_src_type() -> None:
    g = Graph()
    g.add_node(make_node("a", {"out": make_port("out", PortDirection.OUTPUT, DataType.TENSOR)}))
    g.add_node(make_node("b", {"in": make_port("in", PortDirection.INPUT, DataType.ANY)}))
    g.add_edge(make_edge("e1", "a", "out", "b", "in"))
    assert GraphValidator()._check_type_compatibility(g) == []


# ── _check_required_ports ─────────────────────────────────────────────────────


def test_unconnected_required_port_detected() -> None:
    g = Graph()
    g.add_node(make_node("a", {"in": make_port("in", PortDirection.INPUT, required=True)}))
    errors = GraphValidator()._check_required_ports(g)
    assert any(e.code == "REQUIRED_PORT_UNCONNECTED" for e in errors)


def test_optional_unconnected_port_ignored() -> None:
    g = Graph()
    g.add_node(make_node("a", {"in": make_port("in", PortDirection.INPUT, required=False)}))
    assert GraphValidator()._check_required_ports(g) == []


def test_connected_required_port_passes() -> None:
    g = Graph()
    g.add_node(make_node("a", {"out": make_port("out", PortDirection.OUTPUT)}))
    g.add_node(make_node("b", {"in": make_port("in", PortDirection.INPUT, required=True)}))
    g.add_edge(make_edge("e1", "a", "out", "b", "in"))
    assert GraphValidator()._check_required_ports(g) == []


def test_output_port_not_checked_for_required() -> None:
    g = Graph()
    g.add_node(make_node("a", {"out": make_port("out", PortDirection.OUTPUT, required=True)}))
    assert GraphValidator()._check_required_ports(g) == []


# ── _check_single_producer ────────────────────────────────────────────────────


def test_multiple_producers_detected() -> None:
    g = Graph()
    g.add_node(make_node("a"))
    g.add_node(make_node("b"))
    g.add_node(make_node("c"))
    g.add_edge(make_edge("e1", "a", "out", "c", "in"))
    g.add_edge(make_edge("e2", "b", "out", "c", "in"))
    errors = GraphValidator()._check_single_producer(g)
    assert any(e.code == "MULTIPLE_PRODUCERS" for e in errors)


def test_single_producer_passes() -> None:
    g = Graph()
    g.add_node(make_node("a"))
    g.add_node(make_node("b"))
    g.add_edge(make_edge("e1", "a", "out", "b", "in"))
    assert GraphValidator()._check_single_producer(g) == []


def test_two_different_ports_on_same_node_is_fine() -> None:
    g = Graph()
    g.add_node(make_node("a"))
    g.add_node(make_node("b"))
    g.add_edge(make_edge("e1", "a", "out", "b", "in1"))
    g.add_edge(make_edge("e2", "a", "out", "b", "in2"))
    assert GraphValidator()._check_single_producer(g) == []
