from __future__ import annotations

import pytest

from neuroforge.graph.components import ComponentDefinition, ComponentLibrary
from neuroforge.graph.model import DataType, Edge, Graph, Node, Port, PortDirection

# ── Helpers ───────────────────────────────────────────────────────────────────


def make_port(pid: str, direction: PortDirection) -> Port:
    return Port(id=pid, name=pid, direction=direction, data_type=DataType.TENSOR, required=True)


def make_node(nid: str, ports: dict[str, Port] | None = None) -> Node:
    return Node(id=nid, type="linear", name=nid, position=(0.0, 0.0), ports=ports or {}, params={})


def make_edge(eid: str, src: str, src_port: str, dst: str, dst_port: str) -> Edge:
    return Edge(id=eid, src_node=src, src_port=src_port, dst_node=dst, dst_port=dst_port)


def make_component(cid: str = "c1", name: str = "MyComp") -> ComponentDefinition:
    return ComponentDefinition(
        id=cid,
        name=name,
        inner_graph=Graph(),
        input_interface=[],
        output_interface=[],
    )


def linear_graph() -> tuple[Graph, str, str]:
    """Graph: ext_src → [a → b] → ext_dst. Returns (graph, 'a', 'b')."""
    g = Graph()
    g.add_node(make_node("ext_src", {"out": make_port("out", PortDirection.OUTPUT)}))
    g.add_node(
        make_node(
            "a",
            {
                "in": make_port("in", PortDirection.INPUT),
                "out": make_port("out", PortDirection.OUTPUT),
            },
        )
    )
    g.add_node(
        make_node(
            "b",
            {
                "in": make_port("in", PortDirection.INPUT),
                "out": make_port("out", PortDirection.OUTPUT),
            },
        )
    )
    g.add_node(make_node("ext_dst", {"in": make_port("in", PortDirection.INPUT)}))
    g.add_edge(make_edge("e0", "ext_src", "out", "a", "in"))
    g.add_edge(make_edge("e1", "a", "out", "b", "in"))
    g.add_edge(make_edge("e2", "b", "out", "ext_dst", "in"))
    return g, "a", "b"


# ── ComponentLibrary ──────────────────────────────────────────────────────────


class TestComponentLibraryBasic:
    def test_register_and_get(self) -> None:
        lib = ComponentLibrary()
        comp = make_component("c1")
        lib.register(comp)
        assert lib.get("c1") is comp

    def test_get_unknown_raises_key_error(self) -> None:
        with pytest.raises(KeyError):
            ComponentLibrary().get("nope")

    def test_all_returns_empty_initially(self) -> None:
        assert ComponentLibrary().all() == []

    def test_all_returns_registered_components(self) -> None:
        lib = ComponentLibrary()
        c1, c2 = make_component("c1"), make_component("c2")
        lib.register(c1)
        lib.register(c2)
        assert sorted(c.id for c in lib.all()) == ["c1", "c2"]

    def test_remove_deletes_component(self) -> None:
        lib = ComponentLibrary()
        lib.register(make_component("c1"))
        lib.remove("c1")
        assert lib.all() == []

    def test_remove_unknown_raises_key_error(self) -> None:
        with pytest.raises(KeyError):
            ComponentLibrary().remove("nope")


# ── create_from_selection ─────────────────────────────────────────────────────


class TestCreateFromSelection:
    def test_returns_component_definition(self) -> None:
        g, a, b = linear_graph()
        lib = ComponentLibrary()
        result = lib.create_from_selection(g, [a, b], "Group")
        assert isinstance(result, ComponentDefinition)

    def test_component_has_correct_name(self) -> None:
        g, a, b = linear_graph()
        lib = ComponentLibrary()
        result = lib.create_from_selection(g, [a, b], "MyGroup")
        assert result.name == "MyGroup"

    def test_component_has_unique_id(self) -> None:
        g1, a1, b1 = linear_graph()
        g2, a2, b2 = linear_graph()
        lib = ComponentLibrary()
        r1 = lib.create_from_selection(g1, [a1, b1], "G")
        r2 = lib.create_from_selection(g2, [a2, b2], "G")
        assert r1.id != r2.id

    def test_inner_graph_contains_selected_nodes(self) -> None:
        g, a, b = linear_graph()
        lib = ComponentLibrary()
        result = lib.create_from_selection(g, [a, b], "Group")
        assert a in result.inner_graph.nodes
        assert b in result.inner_graph.nodes

    def test_inner_graph_contains_internal_edges(self) -> None:
        g, a, b = linear_graph()
        lib = ComponentLibrary()
        result = lib.create_from_selection(g, [a, b], "Group")
        # e1 connects a → b, both inside the group
        assert "e1" in result.inner_graph.edges

    def test_input_interface_from_incoming_external_edges(self) -> None:
        g, a, b = linear_graph()
        lib = ComponentLibrary()
        result = lib.create_from_selection(g, [a, b], "Group")
        # e0 arrives from ext_src (outside) into a (inside) → becomes INPUT port
        assert len(result.input_interface) == 1
        assert result.input_interface[0].direction is PortDirection.INPUT

    def test_output_interface_from_outgoing_external_edges(self) -> None:
        g, a, b = linear_graph()
        lib = ComponentLibrary()
        result = lib.create_from_selection(g, [a, b], "Group")
        # e2 leaves b (inside) to ext_dst (outside) → becomes OUTPUT port
        assert len(result.output_interface) == 1
        assert result.output_interface[0].direction is PortDirection.OUTPUT

    def test_component_is_registered_in_library(self) -> None:
        g, a, b = linear_graph()
        lib = ComponentLibrary()
        result = lib.create_from_selection(g, [a, b], "Group")
        assert lib.get(result.id) is result
