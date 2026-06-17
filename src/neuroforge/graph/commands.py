# mypy: disable-error-code="empty-body"
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from .model import Edge, EdgeId, Graph, Node, NodeId


class Command(ABC):
    @abstractmethod
    def execute(self) -> None: ...

    @abstractmethod
    def undo(self) -> None: ...


class CommandHistory:
    MAX_SIZE = 100

    def __init__(self) -> None: ...

    def push(self, command: Command) -> None: ...

    def undo(self) -> None: ...

    def redo(self) -> None: ...

    def can_undo(self) -> bool: ...

    def can_redo(self) -> bool: ...

    def clear(self) -> None: ...


class MacroCommand(Command):
    def __init__(self, commands: list[Command]) -> None: ...

    def execute(self) -> None: ...

    def undo(self) -> None: ...


class AddNodeCommand(Command):
    def __init__(self, graph: Graph, node: Node) -> None: ...

    def execute(self) -> None: ...

    def undo(self) -> None: ...


class RemoveNodeCommand(Command):
    def __init__(self, graph: Graph, node_id: NodeId) -> None: ...

    def execute(self) -> None: ...

    def undo(self) -> None: ...


class MoveNodeCommand(Command):
    def __init__(
        self,
        graph: Graph,
        node_id: NodeId,
        old_pos: tuple[float, float],
        new_pos: tuple[float, float],
    ) -> None: ...

    def execute(self) -> None: ...

    def undo(self) -> None: ...


class AddEdgeCommand(Command):
    def __init__(self, graph: Graph, edge: Edge) -> None: ...

    def execute(self) -> None: ...

    def undo(self) -> None: ...


class RemoveEdgeCommand(Command):
    def __init__(self, graph: Graph, edge_id: EdgeId) -> None: ...

    def execute(self) -> None: ...

    def undo(self) -> None: ...


class UpdateParamCommand(Command):
    def __init__(
        self,
        graph: Graph,
        node_id: NodeId,
        param: str,
        old_value: Any,
        new_value: Any,
    ) -> None: ...

    def execute(self) -> None: ...

    def undo(self) -> None: ...


class GroupNodesCommand(Command):
    def __init__(self, graph: Graph, node_ids: list[NodeId], name: str) -> None: ...

    def execute(self) -> None: ...

    def undo(self) -> None: ...
