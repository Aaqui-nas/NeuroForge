from __future__ import annotations

import dataclasses
import uuid

from .model import DataType, Graph, NodeId, Port, PortDirection


@dataclasses.dataclass
class ComponentDefinition:
    """A reusable subgraph component extracted from a parent graph.

    Attributes:
        id: Unique identifier for this component.
        name: Human-readable label shown in the component library.
        inner_graph: The graph containing the grouped nodes and their
            internal edges.
        input_interface: Ports through which data enters the component
            (one per incoming external edge at creation time).
        output_interface: Ports through which data leaves the component
            (one per outgoing external edge at creation time).
    """

    id: str
    name: str
    inner_graph: Graph
    input_interface: list[Port]
    output_interface: list[Port]


class ComponentLibrary:
    """Registry of `ComponentDefinition` objects for a project.

    Components are stored by their unique ID. Use `create_from_selection`
    to extract a subgraph from a `Graph` and register it in one step.
    """

    def __init__(self) -> None:
        self._components: dict[str, ComponentDefinition] = {}

    def register(self, component: ComponentDefinition) -> None:
        """Store *component* in the library.

        Args:
            component: The component to register.
        """
        self._components[component.id] = component

    def get(self, component_id: str) -> ComponentDefinition:
        """Return the component with the given ID.

        Args:
            component_id: The component's unique identifier.

        Raises:
            KeyError: If no component with that ID is registered.
        """
        return self._components[component_id]

    def all(self) -> list[ComponentDefinition]:
        """Return all registered components."""
        return list(self._components.values())

    def remove(self, component_id: str) -> None:
        """Remove the component with the given ID.

        Args:
            component_id: The component's unique identifier.

        Raises:
            KeyError: If no component with that ID is registered.
        """
        if component_id not in self._components:
            raise KeyError(f"Component not found: {component_id!r}")
        del self._components[component_id]

    def create_from_selection(
        self, graph: Graph, node_ids: list[NodeId], name: str
    ) -> ComponentDefinition:
        """Extract a set of nodes into a new `ComponentDefinition`.

        Algorithm:
        1. Build the *inner_graph* from the selected nodes and their
           internal edges (both endpoints inside the selection).
        2. Identify *incoming* external edges (source outside, destination
           inside) → each becomes an INPUT port on the component's interface.
        3. Identify *outgoing* external edges (source inside, destination
           outside) → each becomes an OUTPUT port.
        4. Register and return the resulting `ComponentDefinition`.

        Args:
            graph: The parent graph to extract from.
            node_ids: IDs of the nodes to group.
            name: Display name for the new component.

        Returns:
            The newly created and registered `ComponentDefinition`.
        """
        node_set = set(node_ids)

        inner = Graph()
        for nid in node_ids:
            if nid in graph.nodes:
                inner.add_node(graph.nodes[nid])

        input_ports: list[Port] = []
        output_ports: list[Port] = []

        for edge in graph.edges.values():
            src_inside = edge.src_node in node_set
            dst_inside = edge.dst_node in node_set

            if src_inside and dst_inside:
                inner.add_edge(edge)
            elif not src_inside and dst_inside:
                src_port = (
                    graph.nodes[edge.src_node].ports.get(edge.src_port)
                    if edge.src_node in graph.nodes
                    else None
                )
                data_type = src_port.data_type if src_port else DataType.ANY
                port_id = f"in_{edge.dst_node}_{edge.dst_port}"
                input_ports.append(
                    Port(
                        id=port_id,
                        name=port_id,
                        direction=PortDirection.INPUT,
                        data_type=data_type,
                        required=True,
                    )
                )
            elif src_inside and not dst_inside:
                src_port = (
                    graph.nodes[edge.src_node].ports.get(edge.src_port)
                    if edge.src_node in graph.nodes
                    else None
                )
                data_type = src_port.data_type if src_port else DataType.ANY
                port_id = f"out_{edge.src_node}_{edge.src_port}"
                output_ports.append(
                    Port(
                        id=port_id,
                        name=port_id,
                        direction=PortDirection.OUTPUT,
                        data_type=data_type,
                        required=False,
                    )
                )

        component = ComponentDefinition(
            id=str(uuid.uuid4()),
            name=name,
            inner_graph=inner,
            input_interface=input_ports,
            output_interface=output_ports,
        )
        self.register(component)
        return component
