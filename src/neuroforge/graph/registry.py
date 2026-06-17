from __future__ import annotations

import dataclasses
from typing import Any

from .model import DataType, PortDirection


@dataclasses.dataclass(frozen=True)
class PortDefinition:
    """Static description of a port slot on a node type.

    Attributes:
        id: Unique identifier within the node (e.g. ``"input"``, ``"a"``).
        name: Human-readable label displayed in the UI.
        direction: Whether data flows into or out of this port.
        data_type: Expected tensor or scalar type carried by this port.
        required: If ``True``, the port must be connected before the graph
            can be used for code generation or training.
    """

    id: str
    name: str
    direction: PortDirection
    data_type: DataType
    required: bool = True


@dataclasses.dataclass(frozen=True)
class NodeDefinition:
    """Immutable descriptor for a node type registered in a `NodeRegistry`.

    Attributes:
        type: Unique machine identifier (e.g. ``"conv2d"``).
        display_name: Human-readable name shown in the UI palette.
        category: Palette group this node belongs to (e.g. ``"Conv"``).
        ports: Ordered tuple of `PortDefinition` instances for this node type.
        default_params: Mapping of parameter name to its default value,
            used when a new node is instantiated from this definition.
        param_schema: Mapping of parameter name to a descriptor dict
            (``{"type": "int", "min": 1}``), used to generate the parameter
            panel UI.
    """

    type: str
    display_name: str
    category: str
    ports: tuple[PortDefinition, ...]
    default_params: dict[str, Any]
    param_schema: dict[str, Any]


class NodeRegistry:
    """Catalogue that maps node type strings to their `NodeDefinition`.

    Use `build_default_registry` to obtain a pre-populated instance with all
    built-in Phase-1 node types.  Custom node types can be added via
    `register`.
    """

    def __init__(self) -> None:
        self._definitions: dict[str, NodeDefinition] = {}

    def register(self, definition: NodeDefinition) -> None:
        """Add a node definition to the registry.

        Args:
            definition: The `NodeDefinition` to register.

        Raises:
            KeyError: If a definition with the same ``type`` is already
                registered.
        """
        if definition.type in self._definitions:
            raise KeyError(f"Node type already registered: {definition.type!r}")
        self._definitions[definition.type] = definition

    def get(self, node_type: str) -> NodeDefinition:
        """Return the definition registered under *node_type*.

        Args:
            node_type: The ``type`` string of the desired node (e.g.
                ``"linear"``).

        Returns:
            The matching `NodeDefinition`.

        Raises:
            KeyError: If *node_type* has not been registered.
        """
        return self._definitions[node_type]

    def all(self) -> list[NodeDefinition]:
        """Return all registered definitions in insertion order."""
        return list(self._definitions.values())

    def categories(self) -> list[str]:
        """Return the deduplicated list of category names present in the registry."""
        return list(set(d.category for d in self._definitions.values()))

    def by_category(self, category: str) -> list[NodeDefinition]:
        """Return all definitions whose category matches *category*.

        Args:
            category: The category string to filter on (e.g. ``"Activation"``).

        Returns:
            A list of matching `NodeDefinition` instances, empty if none match.
        """
        return [d for d in self._definitions.values() if d.category == category]


def _tensor_in(port_id: str = "input", required: bool = True) -> PortDefinition:
    return PortDefinition(port_id, port_id, PortDirection.INPUT, DataType.TENSOR, required)


def _tensor_out(port_id: str = "output") -> PortDefinition:
    return PortDefinition(port_id, port_id, PortDirection.OUTPUT, DataType.TENSOR)


def build_default_registry() -> NodeRegistry:
    """Build and return a `NodeRegistry` pre-populated with all Phase-1 node types.

    The catalogue covers the following categories:

    * **I/O** — ``input``, ``output``
    * **Linear** — ``linear``
    * **Conv** — ``conv1d``, ``conv2d``, ``conv3d``
    * **Activation** — ``relu``, ``gelu``, ``sigmoid``, ``tanh``, ``softmax``
    * **Norm** — ``batchnorm1d``, ``batchnorm2d``, ``layernorm``
    * **Regularisation** — ``dropout``
    * **Shape** — ``flatten``, ``reshape``, ``permute``
    * **Connexion** — ``add``, ``concat``

    Returns:
        A fully populated `NodeRegistry`.
    """
    r = NodeRegistry()

    r.register(
        NodeDefinition(
            type="input",
            display_name="Input",
            category="I/O",
            ports=(_tensor_out("output"),),
            default_params={},
            param_schema={},
        )
    )

    r.register(
        NodeDefinition(
            type="output",
            display_name="Output",
            category="I/O",
            ports=(_tensor_in("input"),),
            default_params={},
            param_schema={},
        )
    )

    r.register(
        NodeDefinition(
            type="linear",
            display_name="Linear",
            category="Linear",
            ports=(_tensor_in(), _tensor_out()),
            default_params={"in_features": 128, "out_features": 64, "bias": True},
            param_schema={
                "in_features": {"type": "int", "min": 1},
                "out_features": {"type": "int", "min": 1},
                "bias": {"type": "bool"},
            },
        )
    )

    for suffix, display in (("conv1d", "Conv1d"), ("conv2d", "Conv2d"), ("conv3d", "Conv3d")):
        r.register(
            NodeDefinition(
                type=suffix,
                display_name=display,
                category="Conv",
                ports=(_tensor_in(), _tensor_out()),
                default_params={
                    "in_channels": 1,
                    "out_channels": 32,
                    "kernel_size": 3,
                    "stride": 1,
                    "padding": 0,
                },
                param_schema={
                    "in_channels": {"type": "int", "min": 1},
                    "out_channels": {"type": "int", "min": 1},
                    "kernel_size": {"type": "int", "min": 1},
                    "stride": {"type": "int", "min": 1},
                    "padding": {"type": "int", "min": 0},
                },
            )
        )

    for act_type, act_name in (
        ("relu", "ReLU"),
        ("gelu", "GELU"),
        ("sigmoid", "Sigmoid"),
        ("tanh", "Tanh"),
    ):
        r.register(
            NodeDefinition(
                type=act_type,
                display_name=act_name,
                category="Activation",
                ports=(_tensor_in(), _tensor_out()),
                default_params={},
                param_schema={},
            )
        )

    r.register(
        NodeDefinition(
            type="softmax",
            display_name="Softmax",
            category="Activation",
            ports=(_tensor_in(), _tensor_out()),
            default_params={"dim": -1},
            param_schema={"dim": {"type": "int"}},
        )
    )

    r.register(
        NodeDefinition(
            type="batchnorm1d",
            display_name="BatchNorm1d",
            category="Norm",
            ports=(_tensor_in(), _tensor_out()),
            default_params={"num_features": 64},
            param_schema={"num_features": {"type": "int", "min": 1}},
        )
    )

    r.register(
        NodeDefinition(
            type="batchnorm2d",
            display_name="BatchNorm2d",
            category="Norm",
            ports=(_tensor_in(), _tensor_out()),
            default_params={"num_features": 64},
            param_schema={"num_features": {"type": "int", "min": 1}},
        )
    )

    r.register(
        NodeDefinition(
            type="layernorm",
            display_name="LayerNorm",
            category="Norm",
            ports=(_tensor_in(), _tensor_out()),
            default_params={"normalized_shape": [64]},
            param_schema={"normalized_shape": {"type": "list[int]"}},
        )
    )

    r.register(
        NodeDefinition(
            type="dropout",
            display_name="Dropout",
            category="Regularisation",
            ports=(_tensor_in(), _tensor_out()),
            default_params={"p": 0.5},
            param_schema={"p": {"type": "float", "min": 0.0, "max": 1.0}},
        )
    )

    r.register(
        NodeDefinition(
            type="flatten",
            display_name="Flatten",
            category="Shape",
            ports=(_tensor_in(), _tensor_out()),
            default_params={"start_dim": 1, "end_dim": -1},
            param_schema={
                "start_dim": {"type": "int"},
                "end_dim": {"type": "int"},
            },
        )
    )

    r.register(
        NodeDefinition(
            type="reshape",
            display_name="Reshape",
            category="Shape",
            ports=(_tensor_in(), _tensor_out()),
            default_params={"shape": [-1]},
            param_schema={"shape": {"type": "list[int]"}},
        )
    )

    r.register(
        NodeDefinition(
            type="permute",
            display_name="Permute",
            category="Shape",
            ports=(_tensor_in(), _tensor_out()),
            default_params={"dims": [0, 1]},
            param_schema={"dims": {"type": "list[int]"}},
        )
    )

    r.register(
        NodeDefinition(
            type="add",
            display_name="Add",
            category="Connexion",
            ports=(_tensor_in("a"), _tensor_in("b"), _tensor_out()),
            default_params={},
            param_schema={},
        )
    )

    r.register(
        NodeDefinition(
            type="concat",
            display_name="Concat",
            category="Connexion",
            ports=(_tensor_in("a"), _tensor_in("b"), _tensor_out()),
            default_params={"dim": 1},
            param_schema={"dim": {"type": "int"}},
        )
    )

    return r
