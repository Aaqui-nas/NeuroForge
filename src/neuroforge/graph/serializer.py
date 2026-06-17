from __future__ import annotations

import dataclasses
import enum
import json
from pathlib import Path
from typing import Any

from .model import DataType, Edge, Graph, Node, Port, PortDirection

SCHEMA_VERSION = 1


def _to_serializable(obj: Any) -> Any:
    """Recursively convert Enum → int and tuple → list for JSON compatibility."""
    if isinstance(obj, enum.Enum):
        return obj.value
    if isinstance(obj, dict):
        return {k: _to_serializable(v) for k, v in obj.items()}
    if isinstance(obj, list | tuple):
        return [_to_serializable(v) for v in obj]
    return obj


class GraphSerializer:
    """Serializes and deserializes a `Graph` to/from JSON.

    The JSON file format includes a ``schema_version`` field at the root
    so that future breaking changes can be handled by `_migrate`.

    Example path: ``<project_root>/graphs/<graph_id>.json``
    """

    def to_dict(self, graph: Graph) -> dict[str, Any]:
        """Convert a `Graph` to a JSON-serializable dict.

        Enum values are stored as their integer representation.
        Tuples (position) are stored as lists.

        Args:
            graph: The graph to serialize.

        Returns:
            A dict ready to be passed to ``json.dump``.
        """
        data: dict[str, Any] = _to_serializable(dataclasses.asdict(graph))
        data["schema_version"] = SCHEMA_VERSION
        return data

    def from_dict(self, data: dict[str, Any]) -> Graph:
        """Reconstruct a `Graph` from a deserialized dict.

        Calls `_migrate` automatically if the stored schema version is older
        than `SCHEMA_VERSION`.

        Args:
            data: Raw dict from ``json.load``.

        Returns:
            A fully reconstructed `Graph`.

        Raises:
            KeyError: If required fields are missing.
            ValueError: If enum values are invalid.
        """
        version = data.get("schema_version", 1)
        if version < SCHEMA_VERSION:
            data = self._migrate(data, version)

        nodes = {nid: self._node_from_dict(n) for nid, n in data["nodes"].items()}
        edges = {eid: self._edge_from_dict(e) for eid, e in data["edges"].items()}
        return Graph(nodes=nodes, edges=edges)

    def save(self, graph: Graph, path: Path) -> None:
        """Write the graph to a JSON file.

        Creates parent directories automatically.

        Args:
            graph: The graph to save.
            path: Full file path, e.g. ``project.graph_dir() / f"{graph_id}.json"``.
        """
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            json.dump(self.to_dict(graph), f, indent=4)

    def load(self, path: Path) -> Graph:
        """Load a graph from a JSON file.

        Args:
            path: Full path to the ``.json`` file.

        Returns:
            The deserialized `Graph`.

        Raises:
            FileNotFoundError: If the file does not exist.
        """
        with open(path) as f:
            data = json.load(f)
        return self.from_dict(data)

    def _migrate(self, data: dict[str, Any], from_version: int) -> dict[str, Any]:
        """Upgrade ``data`` from an older schema version to `SCHEMA_VERSION`.

        Add a ``if from_version < N:`` block here each time a breaking change
        is introduced in the JSON format.

        Args:
            data: Raw dict at ``from_version`` format.
            from_version: The schema version stored in the file.

        Returns:
            The dict updated to `SCHEMA_VERSION` format.
        """
        return data

    def _port_from_dict(self, data: dict[str, Any]) -> Port:
        return Port(
            id=data["id"],
            name=data["name"],
            direction=PortDirection(data["direction"]),
            data_type=DataType(data["data_type"]),
            required=data["required"],
        )

    def _node_from_dict(self, data: dict[str, Any]) -> Node:
        pos = data["position"]
        return Node(
            id=data["id"],
            type=data["type"],
            name=data["name"],
            position=(pos[0], pos[1]),
            ports={pid: self._port_from_dict(p) for pid, p in data["ports"].items()},
            params=data["params"],
        )

    def _edge_from_dict(self, data: dict[str, Any]) -> Edge:
        return Edge(
            id=data["id"],
            src_node=data["src_node"],
            src_port=data["src_port"],
            dst_node=data["dst_node"],
            dst_port=data["dst_port"],
        )
