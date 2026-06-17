# mypy: disable-error-code="empty-body"
from __future__ import annotations

from pathlib import Path
from typing import Any

from .model import Graph

SCHEMA_VERSION = 1


class GraphSerializer:
    def to_dict(self, graph: Graph) -> dict[str, Any]: ...

    def from_dict(self, data: dict[str, Any]) -> Graph: ...

    def save(self, graph: Graph, path: Path) -> None: ...

    def load(self, path: Path) -> Graph: ...

    def _migrate(self, data: dict[str, Any], from_version: int) -> dict[str, Any]: ...
