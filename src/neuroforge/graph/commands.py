from __future__ import annotations

import dataclasses
import uuid
from abc import ABC, abstractmethod
from typing import Any

from .model import Edge, EdgeId, Graph, Node, NodeId


class Command(ABC):
    """Base class for all reversible graph operations."""

    @abstractmethod
    def execute(self) -> None:
        """Apply the operation to the graph."""

    @abstractmethod
    def undo(self) -> None:
        """Reverse the operation, restoring prior graph state."""


class CommandHistory:
    """Undo/redo stack for a sequence of `Command` objects.

    Maintains a bounded stack (``MAX_SIZE`` entries). Pushing a new command
    while there is a redo branch discards all future entries first.

    Attributes:
        MAX_SIZE: Maximum number of commands kept in history.
    """

    MAX_SIZE = 100

    def __init__(self) -> None:
        self._stack: list[Command] = []
        self._index: int = -1

    def push(self, command: Command) -> None:
        """Execute *command* and add it to the history.

        Discards any redo branch before pushing. Trims the oldest entry
        when the stack exceeds `MAX_SIZE`.

        Args:
            command: The command to execute and record.
        """
        del self._stack[self._index + 1 :]
        command.execute()
        self._stack.append(command)
        if len(self._stack) > self.MAX_SIZE:
            self._stack.pop(0)
            self._index = len(self._stack) - 1
        else:
            self._index += 1

    def undo(self) -> None:
        """Undo the last executed command. No-op if there is nothing to undo."""
        if not self.can_undo():
            return
        self._stack[self._index].undo()
        self._index -= 1

    def redo(self) -> None:
        """Re-execute the last undone command. No-op if there is nothing to redo."""
        if not self.can_redo():
            return
        self._index += 1
        self._stack[self._index].execute()

    def can_undo(self) -> bool:
        """Return ``True`` if there is at least one command to undo."""
        return self._index >= 0

    def can_redo(self) -> bool:
        """Return ``True`` if there is at least one undone command to redo."""
        return self._index < len(self._stack) - 1

    def clear(self) -> None:
        """Discard all history entries."""
        self._stack = []
        self._index = -1


class MacroCommand(Command):
    """A composite command that executes a list of sub-commands atomically.

    ``execute`` runs sub-commands in order; ``undo`` reverses them.
    """

    def __init__(self, commands: list[Command]) -> None:
        """
        Args:
            commands: Ordered list of sub-commands.
        """
        self._commands = commands

    def execute(self) -> None:
        for cmd in self._commands:
            cmd.execute()

    def undo(self) -> None:
        for cmd in reversed(self._commands):
            cmd.undo()


class AddNodeCommand(Command):
    """Add a node to the graph; undo removes it."""

    def __init__(self, graph: Graph, node: Node) -> None:
        """
        Args:
            graph: Target graph.
            node: The node to add.
        """
        self._graph = graph
        self._node = node

    def execute(self) -> None:
        self._graph.add_node(self._node)

    def undo(self) -> None:
        self._graph.remove_node(self._node.id)


class RemoveNodeCommand(Command):
    """Remove a node (and its edges) from the graph; undo restores all."""

    def __init__(self, graph: Graph, node_id: NodeId) -> None:
        """
        Args:
            graph: Target graph.
            node_id: ID of the node to remove.
        """
        self._graph = graph
        self._node_id = node_id
        self._removed_node: Node | None = None
        self._removed_edges: list[Edge] = []

    def execute(self) -> None:
        self._removed_node = self._graph.get_node(self._node_id)
        if self._removed_node is None:
            return
        self._removed_edges = [
            e
            for e in self._graph.edges.values()
            if e.src_node == self._node_id or e.dst_node == self._node_id
        ]
        self._graph.remove_node(self._node_id)

    def undo(self) -> None:
        if self._removed_node is None:
            return
        self._graph.add_node(self._removed_node)
        for edge in self._removed_edges:
            self._graph.add_edge(edge)


class MoveNodeCommand(Command):
    """Update the position of a node; undo reverts to the previous position."""

    def __init__(
        self,
        graph: Graph,
        node_id: NodeId,
        old_pos: tuple[float, float],
        new_pos: tuple[float, float],
    ) -> None:
        """
        Args:
            graph: Target graph.
            node_id: ID of the node to move.
            old_pos: Position before the move (used by undo).
            new_pos: Position after the move.
        """
        self._graph = graph
        self._node_id = node_id
        self._old_pos = old_pos
        self._new_pos = new_pos

    def execute(self) -> None:
        if self._node_id in self._graph.nodes:
            self._graph.nodes[self._node_id] = dataclasses.replace(
                self._graph.nodes[self._node_id], position=self._new_pos
            )

    def undo(self) -> None:
        if self._node_id in self._graph.nodes:
            self._graph.nodes[self._node_id] = dataclasses.replace(
                self._graph.nodes[self._node_id], position=self._old_pos
            )


class AddEdgeCommand(Command):
    """Add an edge to the graph; undo removes it."""

    def __init__(self, graph: Graph, edge: Edge) -> None:
        """
        Args:
            graph: Target graph.
            edge: The edge to add.
        """
        self._graph = graph
        self._edge = edge

    def execute(self) -> None:
        self._graph.add_edge(self._edge)

    def undo(self) -> None:
        self._graph.remove_edge(self._edge.id)


class RemoveEdgeCommand(Command):
    """Remove an edge from the graph; undo restores it."""

    def __init__(self, graph: Graph, edge_id: EdgeId) -> None:
        """
        Args:
            graph: Target graph.
            edge_id: ID of the edge to remove.
        """
        self._graph = graph
        self._edge_id = edge_id
        self._removed_edge: Edge | None = None

    def execute(self) -> None:
        self._removed_edge = self._graph.get_edge(self._edge_id)
        if self._removed_edge is not None:
            self._graph.remove_edge(self._edge_id)

    def undo(self) -> None:
        if self._removed_edge is not None:
            self._graph.add_edge(self._removed_edge)


class UpdateParamCommand(Command):
    """Update one parameter on a node; undo restores the previous value.

    If *old_value* is ``None``, undo removes the parameter key entirely
    (the parameter did not exist before the command was executed).
    """

    def __init__(
        self,
        graph: Graph,
        node_id: NodeId,
        param: str,
        old_value: Any,
        new_value: Any,
    ) -> None:
        """
        Args:
            graph: Target graph.
            node_id: ID of the node whose parameter changes.
            param: Parameter key.
            old_value: Value before the change (``None`` if the key was absent).
            new_value: Value after the change.
        """
        self._graph = graph
        self._node_id = node_id
        self._param = param
        self._old_value = old_value
        self._new_value = new_value

    def execute(self) -> None:
        node = self._graph.get_node(self._node_id)
        if node is not None:
            node.params[self._param] = self._new_value

    def undo(self) -> None:
        node = self._graph.get_node(self._node_id)
        if node is None:
            return
        if self._old_value is None:
            node.params.pop(self._param, None)
        else:
            node.params[self._param] = self._old_value


class GroupNodesCommand(Command):
    """Remove a set of nodes (and their edges) and insert a ComponentNode placeholder.

    On undo, the placeholder is removed and the original nodes and edges are
    restored. Pass *component_node* to insert a visual placeholder; omit it
    (``None``) for a pure removal (e.g. in tests).
    """

    def __init__(
        self,
        graph: Graph,
        node_ids: list[NodeId],
        name: str,
        component_node: Node | None = None,
    ) -> None:
        """
        Args:
            graph: Target graph.
            node_ids: IDs of the nodes to group.
            name: Display name for the resulting component.
            component_node: Optional placeholder node to insert after grouping.
        """
        self._graph = graph
        self._node_ids = list(node_ids)
        self._name = name
        self._component_node = component_node
        self._removed_nodes: list[Node] = []
        self._removed_edges: list[Edge] = []
        self._reconnection_edges: list[Edge] = []

    def execute(self) -> None:
        node_set = set(self._node_ids)
        self._removed_nodes = [
            self._graph.nodes[nid] for nid in self._node_ids if nid in self._graph.nodes
        ]
        self._removed_edges = [
            e
            for e in self._graph.edges.values()
            if e.src_node in node_set or e.dst_node in node_set
        ]
        incoming = [e for e in self._removed_edges if e.src_node not in node_set]
        outgoing = [e for e in self._removed_edges if e.dst_node not in node_set]

        for nid in self._node_ids:
            self._graph.remove_node(nid)

        if self._component_node is not None:
            self._graph.add_node(self._component_node)
            self._reconnection_edges = []
            for e in incoming:
                new_edge = Edge(
                    id=str(uuid.uuid4()),
                    src_node=e.src_node,
                    src_port=e.src_port,
                    dst_node=self._component_node.id,
                    dst_port=f"in_{e.dst_node}_{e.dst_port}",
                )
                self._graph.add_edge(new_edge)
                self._reconnection_edges.append(new_edge)
            for e in outgoing:
                new_edge = Edge(
                    id=str(uuid.uuid4()),
                    src_node=self._component_node.id,
                    src_port=f"out_{e.src_node}_{e.src_port}",
                    dst_node=e.dst_node,
                    dst_port=e.dst_port,
                )
                self._graph.add_edge(new_edge)
                self._reconnection_edges.append(new_edge)

    def undo(self) -> None:
        for edge in self._reconnection_edges:
            if edge.id in self._graph.edges:
                self._graph.remove_edge(edge.id)
        self._reconnection_edges = []
        if self._component_node is not None:
            self._graph.remove_node(self._component_node.id)
        for node in self._removed_nodes:
            self._graph.add_node(node)
        for edge in self._removed_edges:
            self._graph.add_edge(edge)
