# mypy: disable-error-code="empty-body"
from __future__ import annotations

import dataclasses
from typing import Any

from .model import DataType, PortDirection


@dataclasses.dataclass(frozen=True)
class PortDefinition:
    id: str
    name: str
    direction: PortDirection
    data_type: DataType
    required: bool = True


@dataclasses.dataclass(frozen=True)
class NodeDefinition:
    type: str
    display_name: str
    category: str
    ports: tuple[PortDefinition, ...]
    default_params: dict[str, Any]
    param_schema: dict[str, Any]


class NodeRegistry:
    def register(self, definition: NodeDefinition) -> None: ...

    def get(self, node_type: str) -> NodeDefinition: ...

    def all(self) -> list[NodeDefinition]: ...

    def categories(self) -> list[str]: ...

    def by_category(self, category: str) -> list[NodeDefinition]: ...


def build_default_registry() -> NodeRegistry: ...
