# mypy: disable-error-code="empty-body"
from __future__ import annotations

import dataclasses

from .model import Graph, NodeId, Port


@dataclasses.dataclass
class ComponentDefinition:
    id: str
    name: str
    inner_graph: Graph
    input_interface: list[Port]
    output_interface: list[Port]


class ComponentLibrary:
    def register(self, component: ComponentDefinition) -> None: ...

    def get(self, component_id: str) -> ComponentDefinition: ...

    def all(self) -> list[ComponentDefinition]: ...

    def remove(self, component_id: str) -> None: ...

    def create_from_selection(
        self, graph: Graph, node_ids: list[NodeId], name: str
    ) -> ComponentDefinition: ...
