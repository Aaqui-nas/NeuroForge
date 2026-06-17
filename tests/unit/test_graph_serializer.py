from __future__ import annotations

import json
from pathlib import Path

import pytest

from neuroforge.graph.model import (
    DataType,
    Edge,
    Graph,
    Node,
    Port,
    PortDirection,
)
from neuroforge.graph.serializer import SCHEMA_VERSION, GraphSerializer

# ── Helpers ───────────────────────────────────────────────────────────────────


def make_port(pid: str, direction: PortDirection = PortDirection.INPUT) -> Port:
    return Port(id=pid, name=pid, direction=direction, data_type=DataType.TENSOR, required=True)


def make_node(nid: str, *, with_port: bool = False) -> Node:
    ports = {"p_in": make_port("p_in")} if with_port else {}
    return Node(id=nid, type="linear", name=nid, position=(1.0, 2.0), ports=ports, params={"x": 1})


def make_edge(eid: str, src: str, dst: str) -> Edge:
    return Edge(id=eid, src_node=src, src_port="out", dst_node=dst, dst_port="in")


def make_graph() -> Graph:
    g = Graph()
    g.add_node(make_node("a", with_port=True))
    g.add_node(make_node("b", with_port=True))
    g.add_edge(make_edge("e1", "a", "b"))
    return g


# ── to_dict ───────────────────────────────────────────────────────────────────


def test_to_dict_contains_schema_version() -> None:
    s = GraphSerializer()
    d = s.to_dict(Graph())
    assert d["schema_version"] == SCHEMA_VERSION


def test_to_dict_contains_nodes_and_edges_keys() -> None:
    s = GraphSerializer()
    d = s.to_dict(Graph())
    assert "nodes" in d and "edges" in d


def test_to_dict_nodes_are_dicts_not_objects() -> None:
    s = GraphSerializer()
    g = Graph()
    g.add_node(make_node("a"))
    d = s.to_dict(g)
    assert isinstance(d["nodes"]["a"], dict)


def test_to_dict_edge_is_dict() -> None:
    s = GraphSerializer()
    g = Graph()
    g.add_edge(make_edge("e1", "a", "b"))
    d = s.to_dict(g)
    assert isinstance(d["edges"]["e1"], dict)


def test_to_dict_enum_stored_as_int() -> None:
    s = GraphSerializer()
    g = Graph()
    g.add_node(make_node("a", with_port=True))
    d = s.to_dict(g)
    port = list(d["nodes"]["a"]["ports"].values())[0]
    assert isinstance(port["direction"], int)
    assert isinstance(port["data_type"], int)


def test_to_dict_position_stored_as_list() -> None:
    s = GraphSerializer()
    g = Graph()
    g.add_node(make_node("a"))
    d = s.to_dict(g)
    assert isinstance(d["nodes"]["a"]["position"], list)


# ── from_dict ─────────────────────────────────────────────────────────────────


def test_from_dict_returns_graph() -> None:
    s = GraphSerializer()
    assert isinstance(s.from_dict({"schema_version": 1, "nodes": {}, "edges": {}}), Graph)


def test_from_dict_reconstructs_nodes() -> None:
    s = GraphSerializer()
    g = make_graph()
    assert "a" in s.from_dict(s.to_dict(g)).nodes


def test_from_dict_reconstructs_node_type() -> None:
    s = GraphSerializer()
    g = Graph()
    g.add_node(make_node("a"))
    restored = s.from_dict(s.to_dict(g))
    assert isinstance(restored.nodes["a"], Node)


def test_from_dict_reconstructs_position_as_tuple() -> None:
    s = GraphSerializer()
    g = Graph()
    g.add_node(make_node("a"))
    restored = s.from_dict(s.to_dict(g))
    assert restored.nodes["a"].position == (1.0, 2.0)


def test_from_dict_reconstructs_port_enums() -> None:
    s = GraphSerializer()
    g = Graph()
    g.add_node(make_node("a", with_port=True))
    port = s.from_dict(s.to_dict(g)).nodes["a"].ports["p_in"]
    assert port.direction is PortDirection.INPUT
    assert port.data_type is DataType.TENSOR


def test_from_dict_reconstructs_edges() -> None:
    s = GraphSerializer()
    g = make_graph()
    restored = s.from_dict(s.to_dict(g))
    assert isinstance(restored.edges["e1"], Edge)
    assert restored.edges["e1"].src_node == "a"
    assert restored.edges["e1"].dst_node == "b"


def test_from_dict_missing_schema_version_defaults_to_1() -> None:
    s = GraphSerializer()
    g = s.from_dict({"nodes": {}, "edges": {}})
    assert isinstance(g, Graph)


# ── round-trip ────────────────────────────────────────────────────────────────


def test_roundtrip_node_count() -> None:
    s = GraphSerializer()
    g = make_graph()
    assert len(s.from_dict(s.to_dict(g)).nodes) == 2


def test_roundtrip_edge_count() -> None:
    s = GraphSerializer()
    g = make_graph()
    assert len(s.from_dict(s.to_dict(g)).edges) == 1


def test_roundtrip_preserves_params() -> None:
    s = GraphSerializer()
    g = Graph()
    g.add_node(make_node("a"))
    assert s.from_dict(s.to_dict(g)).nodes["a"].params == {"x": 1}


def test_roundtrip_preserves_port_required() -> None:
    s = GraphSerializer()
    g = Graph()
    g.add_node(make_node("a", with_port=True))
    assert s.from_dict(s.to_dict(g)).nodes["a"].ports["p_in"].required is True


# ── save / load ───────────────────────────────────────────────────────────────


def test_save_creates_file(tmp_path: Path) -> None:
    s = GraphSerializer()
    path = tmp_path / "graphs" / "g1.json"
    s.save(make_graph(), path)
    assert path.exists()


def test_save_creates_parent_directories(tmp_path: Path) -> None:
    s = GraphSerializer()
    path = tmp_path / "deep" / "nested" / "g1.json"
    s.save(Graph(), path)
    assert path.exists()


def test_save_writes_valid_json(tmp_path: Path) -> None:
    s = GraphSerializer()
    path = tmp_path / "g.json"
    s.save(make_graph(), path)
    with open(path) as f:
        data = json.load(f)
    assert isinstance(data, dict)


def test_load_raises_if_file_missing(tmp_path: Path) -> None:
    s = GraphSerializer()
    with pytest.raises(FileNotFoundError):
        s.load(tmp_path / "nonexistent.json")


def test_load_returns_graph(tmp_path: Path) -> None:
    s = GraphSerializer()
    path = tmp_path / "g.json"
    s.save(make_graph(), path)
    assert isinstance(s.load(path), Graph)


def test_save_load_roundtrip(tmp_path: Path) -> None:
    s = GraphSerializer()
    path = tmp_path / "g.json"
    original = make_graph()
    s.save(original, path)
    restored = s.load(path)
    assert set(restored.nodes) == set(original.nodes)
    assert set(restored.edges) == set(original.edges)
