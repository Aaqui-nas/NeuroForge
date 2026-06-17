# mypy: disable-error-code="empty-body"
from __future__ import annotations

import dataclasses
from enum import Enum, auto
from typing import Any

NodeId = str
EdgeId = str
PortId = str


class PortDirection(Enum):
    INPUT = auto()
    OUTPUT = auto()


class DataType(Enum):
    TENSOR = auto()
    INT = auto()
    FLOAT = auto()
    STRING = auto()
    ANY = auto()


@dataclasses.dataclass
class Port:
    id: PortId
    name: str
    direction: PortDirection
    data_type: DataType
    required: bool


@dataclasses.dataclass
class Node:
    id: NodeId
    type: str
    name: str
    position: tuple[float, float]
    ports: dict[PortId, Port]
    params: dict[str, Any]


@dataclasses.dataclass
class Edge:
    id: EdgeId
    src_node: NodeId
    src_port: PortId
    dst_node: NodeId
    dst_port: PortId


@dataclasses.dataclass
class Graph:
    nodes: dict[NodeId, Node] = dataclasses.field(default_factory=dict)
    edges: dict[EdgeId, Edge] = dataclasses.field(default_factory=dict)

    def add_node(self, node: Node) -> None: ...

    def remove_node(self, node_id: NodeId) -> list[EdgeId]: ...

    def add_edge(self, edge: Edge) -> None: ...

    def remove_edge(self, edge_id: EdgeId) -> None: ...

    def get_node(self, node_id: NodeId) -> Node: ...

    def get_edge(self, edge_id: EdgeId) -> Edge: ...

    def edges_from(self, node_id: NodeId) -> list[Edge]: ...

    def edges_to(self, node_id: NodeId) -> list[Edge]: ...

    def topological_order(self) -> list[NodeId]: ...
