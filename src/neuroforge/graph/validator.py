from __future__ import annotations

import dataclasses
from collections import Counter

from .model import DataType, EdgeId, Graph, NodeId, PortDirection


@dataclasses.dataclass
class ValidationError:
    """A single validation rule violation.

    Attributes:
        code: Machine-readable identifier (e.g. ``"CYCLE"``).
        message: Human-readable explanation.
        node_id: Offending node, if applicable.
        edge_id: Offending edge, if applicable.
    """

    code: str
    message: str
    node_id: NodeId | None = None
    edge_id: EdgeId | None = None


@dataclasses.dataclass
class ValidationResult:
    """Outcome of a full graph validation pass.

    Attributes:
        is_valid: True only when ``errors`` is empty.
        errors: All violations found; may be empty.
    """

    is_valid: bool
    errors: list[ValidationError]


def _types_compatible(src: DataType, dst: DataType) -> bool:
    """Return True if a value of *src* type can flow into a *dst* port."""
    return src is DataType.ANY or dst is DataType.ANY or src is dst


class GraphValidator:
    """Validates a `Graph` against the five DAG invariants required for training.

    Call `validate` to run all checks in one pass. Individual ``_check_*``
    methods are exposed so they can be tested in isolation.
    """

    def validate(self, graph: Graph) -> ValidationResult:
        """Run all validation checks and return the aggregated result.

        Orphan-edge and cycle checks run first; if either fails the remaining
        semantic checks are skipped to avoid spurious errors from missing nodes.

        Args:
            graph: The graph to validate.

        Returns:
            A `ValidationResult` with ``is_valid=True`` iff no errors were found.
        """
        errors: list[ValidationError] = []

        orphan_errors = self._check_no_orphan_edges(graph)
        errors.extend(orphan_errors)
        if orphan_errors:
            return ValidationResult(is_valid=False, errors=errors)

        cycle_errors = self._check_no_cycles(graph)
        errors.extend(cycle_errors)
        if not cycle_errors:
            errors.extend(self._check_type_compatibility(graph))
            errors.extend(self._check_required_ports(graph))
            errors.extend(self._check_single_producer(graph))

        return ValidationResult(is_valid=len(errors) == 0, errors=errors)

    def _check_no_orphan_edges(self, graph: Graph) -> list[ValidationError]:
        """Verify that every edge references existing source and destination nodes."""
        errors: list[ValidationError] = []
        for edge in graph.edges.values():
            if edge.src_node not in graph.nodes:
                errors.append(
                    ValidationError(
                        code="ORPHAN_EDGE",
                        message=(
                            f"Edge '{edge.id}' references unknown source node '{edge.src_node}'."
                        ),
                        edge_id=edge.id,
                    )
                )
            if edge.dst_node not in graph.nodes:
                errors.append(
                    ValidationError(
                        code="ORPHAN_EDGE",
                        message=(
                            f"Edge '{edge.id}' references unknown destination node"
                            f" '{edge.dst_node}'."
                        ),
                        edge_id=edge.id,
                    )
                )
        return errors

    def _check_no_cycles(self, graph: Graph) -> list[ValidationError]:
        """Detect cycles using Kahn's algorithm (via `Graph.topological_order`)."""
        try:
            graph.topological_order()
        except ValueError:
            return [
                ValidationError(
                    code="CYCLE",
                    message="The graph contains a cycle and is not a valid DAG.",
                )
            ]
        return []

    def _check_type_compatibility(self, graph: Graph) -> list[ValidationError]:
        """Verify that connected ports carry compatible data types.

        `DataType.ANY` is compatible with every other type.
        """
        errors: list[ValidationError] = []
        for edge in graph.edges.values():
            src_node = graph.nodes[edge.src_node]
            dst_node = graph.nodes[edge.dst_node]
            src_port = src_node.ports.get(edge.src_port)
            dst_port = dst_node.ports.get(edge.dst_port)
            if src_port is None or dst_port is None:
                continue
            if not _types_compatible(src_port.data_type, dst_port.data_type):
                errors.append(
                    ValidationError(
                        code="TYPE_MISMATCH",
                        message=(
                            f"Edge '{edge.id}' connects {src_port.data_type.name} "
                            f"→ {dst_port.data_type.name}: incompatible types."
                        ),
                        edge_id=edge.id,
                    )
                )
        return errors

    def _check_required_ports(self, graph: Graph) -> list[ValidationError]:
        """Verify that every required INPUT port has at least one incoming edge."""
        connected: set[tuple[NodeId, str]] = {
            (e.dst_node, e.dst_port) for e in graph.edges.values()
        }
        errors: list[ValidationError] = []
        for node in graph.nodes.values():
            for port in node.ports.values():
                if (
                    port.direction is PortDirection.INPUT
                    and port.required
                    and (node.id, port.id) not in connected
                ):
                    errors.append(
                        ValidationError(
                            code="REQUIRED_PORT_UNCONNECTED",
                            message=(
                                f"Node '{node.id}': required input port '{port.name}' "
                                f"has no incoming connection."
                            ),
                            node_id=node.id,
                        )
                    )
        return errors

    def _check_single_producer(self, graph: Graph) -> list[ValidationError]:
        """Verify that no INPUT port receives more than one incoming edge."""
        incoming: Counter[tuple[NodeId, str]] = Counter(
            (e.dst_node, e.dst_port) for e in graph.edges.values()
        )
        errors: list[ValidationError] = []
        for (node_id, port_id), count in incoming.items():
            if count > 1:
                errors.append(
                    ValidationError(
                        code="MULTIPLE_PRODUCERS",
                        message=(
                            f"Node '{node_id}', port '{port_id}' has {count} incoming "
                            f"edges — only one producer is allowed per input port."
                        ),
                        node_id=node_id,
                    )
                )
        return errors
