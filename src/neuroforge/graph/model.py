# mypy: disable-error-code="empty-body"
from __future__ import annotations

import dataclasses
from collections import deque
from enum import Enum, auto
from typing import Any

NodeId = str
EdgeId = str
PortId = str


class PortDirection(Enum):
    """Direction of a port on a node."""

    INPUT = auto()
    OUTPUT = auto()


class DataType(Enum):
    """Data type flowing through a port connection."""

    TENSOR = auto()
    INT = auto()
    FLOAT = auto()
    STRING = auto()
    ANY = auto()


@dataclasses.dataclass
class Port:
    """A typed connection point on a node.

    Attributes:
        id: Unique identifier within the parent node.
        name: Human-readable label shown in the UI.
        direction: Whether this port receives or emits data.
        data_type: Type of value flowing through this port.
        required: If True, the port must be connected before the graph can run.
    """

    id: PortId
    name: str
    direction: PortDirection
    data_type: DataType
    required: bool


@dataclasses.dataclass
class Node:
    """A single operation in the computation graph.

    Attributes:
        id: UUID string, unique across the graph.
        type: Registry key identifying the node kind (e.g. ``"linear"``).
        name: Display name, editable by the user.
        position: (x, y) canvas coordinates for the UI.
        ports: Mapping of port id → Port.
        params: Hyperparameters for this operation (e.g. ``{"out_features": 128}``).
    """

    id: NodeId
    type: str
    name: str
    position: tuple[float, float]
    ports: dict[PortId, Port]
    params: dict[str, Any]
    component_id: str | None = None


@dataclasses.dataclass
class Edge:
    """A directed connection between two ports.

    Attributes:
        id: UUID string, unique across the graph.
        src_node: ID of the node that produces the value.
        src_port: Output port on the source node.
        dst_node: ID of the node that consumes the value.
        dst_port: Input port on the destination node.
    """

    id: EdgeId
    src_node: NodeId
    src_port: PortId
    dst_node: NodeId
    dst_port: PortId


@dataclasses.dataclass
class Graph:
    """In-memory representation of the neural network computation graph (DAG).

    Attributes:
        nodes: Mapping of node id → Node.
        edges: Mapping of edge id → Edge.
    """

    nodes: dict[NodeId, Node] = dataclasses.field(default_factory=dict)
    edges: dict[EdgeId, Edge] = dataclasses.field(default_factory=dict)

    def add_node(self, node: Node) -> None:
        """Add a node to the graph. Silently ignored if the id already exists.

        Args:
            node: The node to add.
        """
        if node.id not in self.nodes:
            self.nodes[node.id] = node

    def remove_node(self, node_id: NodeId) -> list[EdgeId]:
        """Remove a node and all edges that reference it.

        Args:
            node_id: ID of the node to remove.

        Returns:
            IDs of edges that were removed as a cascade (needed for undo).
            Empty list if the node did not exist.
        """
        if node_id not in self.nodes:
            return []
        self.nodes.pop(node_id)
        removed = [
            e.id for e in self.edges.values() if e.src_node == node_id or e.dst_node == node_id
        ]
        for edge_id in removed:
            self.remove_edge(edge_id)
        return removed

    def add_edge(self, edge: Edge) -> None:
        """Add an edge to the graph. Silently ignored if the id already exists.

        Args:
            edge: The edge to add.
        """
        if edge.id not in self.edges:
            self.edges[edge.id] = edge

    def remove_edge(self, edge_id: EdgeId) -> None:
        """Remove an edge. No-op if the edge does not exist.

        Args:
            edge_id: ID of the edge to remove.
        """
        self.edges.pop(edge_id, None)

    def get_node(self, node_id: NodeId) -> Node | None:
        """Return the node for the given id, or None if not found.

        Args:
            node_id: ID to look up.
        """
        return self.nodes.get(node_id)

    def get_edge(self, edge_id: EdgeId) -> Edge | None:
        """Return the edge for the given id, or None if not found.

        Args:
            edge_id: ID to look up.
        """
        return self.edges.get(edge_id)

    def edges_from(self, node_id: NodeId) -> list[Edge]:
        """Return all edges whose source is the given node.

        Args:
            node_id: Source node ID.
        """
        return [e for e in self.edges.values() if e.src_node == node_id]

    def edges_to(self, node_id: NodeId) -> list[Edge]:
        """Return all edges whose destination is the given node.

        Args:
            node_id: Destination node ID.
        """
        return [e for e in self.edges.values() if e.dst_node == node_id]

    def topological_order(self) -> list[NodeId]:
        """Return node IDs in topological order using Kahn's algorithm (BFS).

        Returns:
            List of node IDs from sources to sinks.

        Raises:
            ValueError: If the graph contains a cycle.
        """
        in_degree = {node_id: 0 for node_id in self.nodes}
        for edge in self.edges.values():
            in_degree[edge.dst_node] += 1

        queue: deque[NodeId] = deque(node_id for node_id, deg in in_degree.items() if deg == 0)
        order: list[NodeId] = []

        while queue:
            node_id = queue.popleft()
            order.append(node_id)
            for edge in self.edges_from(node_id):
                in_degree[edge.dst_node] -= 1
                if in_degree[edge.dst_node] == 0:
                    queue.append(edge.dst_node)

        if len(order) != len(self.nodes):
            raise ValueError("Graph contains a cycle")

        return order
