# mypy: disable-error-code="empty-body"
from __future__ import annotations

import dataclasses

from .model import EdgeId, Graph, NodeId


@dataclasses.dataclass
class ValidationError:
    code: str
    message: str
    node_id: NodeId | None = None
    edge_id: EdgeId | None = None


@dataclasses.dataclass
class ValidationResult:
    is_valid: bool
    errors: list[ValidationError]


class GraphValidator:
    def validate(self, graph: Graph) -> ValidationResult: ...

    def _check_no_cycles(self, graph: Graph) -> list[ValidationError]: ...

    def _check_type_compatibility(self, graph: Graph) -> list[ValidationError]: ...

    def _check_required_ports(self, graph: Graph) -> list[ValidationError]: ...

    def _check_single_producer(self, graph: Graph) -> list[ValidationError]: ...

    def _check_no_orphan_edges(self, graph: Graph) -> list[ValidationError]: ...
