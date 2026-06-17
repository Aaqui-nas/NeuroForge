from __future__ import annotations

import pytest

from neuroforge.graph.model import DataType, PortDirection
from neuroforge.graph.registry import (
    NodeDefinition,
    NodeRegistry,
    PortDefinition,
    build_default_registry,
)

# ── Helpers ───────────────────────────────────────────────────────────────────

EXPECTED_NODE_TYPES = {
    "linear",
    "conv1d",
    "conv2d",
    "conv3d",
    "relu",
    "gelu",
    "sigmoid",
    "tanh",
    "softmax",
    "batchnorm1d",
    "batchnorm2d",
    "layernorm",
    "dropout",
    "flatten",
    "reshape",
    "permute",
    "add",
    "concat",
    "input",
    "output",
}

EXPECTED_CATEGORIES = {
    "Linear",
    "Conv",
    "Activation",
    "Norm",
    "Regularisation",
    "Shape",
    "Connexion",
    "I/O",
}


def make_definition(node_type: str = "linear", category: str = "Linear") -> NodeDefinition:
    port = PortDefinition(
        id="in",
        name="input",
        direction=PortDirection.INPUT,
        data_type=DataType.TENSOR,
        required=True,
    )
    return NodeDefinition(
        type=node_type,
        display_name=node_type.capitalize(),
        category=category,
        ports=(port,),
        default_params={},
        param_schema={},
    )


# ── NodeRegistry ──────────────────────────────────────────────────────────────


class TestNodeRegistryRegisterAndGet:
    def test_registered_definition_is_retrievable(self) -> None:
        registry = NodeRegistry()
        defn = make_definition("linear")
        registry.register(defn)
        assert registry.get("linear") is defn

    def test_get_unknown_type_raises_key_error(self) -> None:
        registry = NodeRegistry()
        with pytest.raises(KeyError):
            registry.get("nonexistent")

    def test_register_duplicate_type_raises(self) -> None:
        registry = NodeRegistry()
        registry.register(make_definition("linear"))
        with pytest.raises((KeyError, ValueError)):
            registry.register(make_definition("linear"))

    def test_multiple_definitions_are_independent(self) -> None:
        registry = NodeRegistry()
        d1 = make_definition("linear", "Linear")
        d2 = make_definition("relu", "Activation")
        registry.register(d1)
        registry.register(d2)
        assert registry.get("linear") is d1
        assert registry.get("relu") is d2


class TestNodeRegistryAll:
    def test_all_returns_empty_when_nothing_registered(self) -> None:
        assert NodeRegistry().all() == []

    def test_all_returns_all_registered_definitions(self) -> None:
        registry = NodeRegistry()
        d1 = make_definition("linear", "Linear")
        d2 = make_definition("relu", "Activation")
        registry.register(d1)
        registry.register(d2)
        assert sorted(registry.all(), key=lambda d: d.type) == sorted(
            [d1, d2], key=lambda d: d.type
        )


class TestNodeRegistryCategories:
    def test_categories_returns_empty_when_nothing_registered(self) -> None:
        assert NodeRegistry().categories() == []

    def test_categories_are_unique(self) -> None:
        registry = NodeRegistry()
        registry.register(make_definition("relu", "Activation"))
        registry.register(make_definition("gelu", "Activation"))
        registry.register(make_definition("linear", "Linear"))
        cats = registry.categories()
        assert len(cats) == len(set(cats))

    def test_categories_returns_all_present_categories(self) -> None:
        registry = NodeRegistry()
        registry.register(make_definition("relu", "Activation"))
        registry.register(make_definition("linear", "Linear"))
        assert set(registry.categories()) == {"Activation", "Linear"}


class TestNodeRegistryByCategory:
    def test_by_category_returns_matching_nodes(self) -> None:
        registry = NodeRegistry()
        d_relu = make_definition("relu", "Activation")
        d_gelu = make_definition("gelu", "Activation")
        d_linear = make_definition("linear", "Linear")
        registry.register(d_relu)
        registry.register(d_gelu)
        registry.register(d_linear)
        result = registry.by_category("Activation")
        assert sorted(result, key=lambda d: d.type) == sorted(
            [d_relu, d_gelu], key=lambda d: d.type
        )

    def test_by_category_returns_empty_for_unknown_category(self) -> None:
        registry = NodeRegistry()
        registry.register(make_definition("linear", "Linear"))
        assert registry.by_category("Unknown") == []


# ── build_default_registry ────────────────────────────────────────────────────


class TestBuildDefaultRegistry:
    def setup_method(self) -> None:
        self.registry = build_default_registry()

    def test_returns_node_registry(self) -> None:
        assert isinstance(self.registry, NodeRegistry)

    def test_all_expected_types_are_registered(self) -> None:
        registered = {d.type for d in self.registry.all()}
        assert EXPECTED_NODE_TYPES.issubset(registered)

    def test_all_expected_categories_are_present(self) -> None:
        assert EXPECTED_CATEGORIES.issubset(set(self.registry.categories()))

    def test_no_duplicate_types(self) -> None:
        types = [d.type for d in self.registry.all()]
        assert len(types) == len(set(types))

    def test_every_node_has_at_least_one_port(self) -> None:
        for defn in self.registry.all():
            assert len(defn.ports) >= 1, f"{defn.type} has no ports"

    def test_default_params_is_dict(self) -> None:
        for defn in self.registry.all():
            assert isinstance(defn.default_params, dict), (
                f"{defn.type}.default_params is not a dict"
            )

    def test_param_schema_is_dict(self) -> None:
        for defn in self.registry.all():
            assert isinstance(defn.param_schema, dict), f"{defn.type}.param_schema is not a dict"

    def test_input_node_has_output_port(self) -> None:
        defn = self.registry.get("input")
        assert any(p.direction == PortDirection.OUTPUT for p in defn.ports)

    def test_output_node_has_input_port(self) -> None:
        defn = self.registry.get("output")
        assert any(p.direction == PortDirection.INPUT for p in defn.ports)

    def test_linear_has_expected_params(self) -> None:
        defn = self.registry.get("linear")
        assert "in_features" in defn.default_params
        assert "out_features" in defn.default_params

    def test_conv2d_has_expected_params(self) -> None:
        defn = self.registry.get("conv2d")
        assert "in_channels" in defn.default_params
        assert "out_channels" in defn.default_params
        assert "kernel_size" in defn.default_params

    def test_dropout_has_p_param(self) -> None:
        defn = self.registry.get("dropout")
        assert "p" in defn.default_params

    def test_all_tensor_ports_have_tensor_data_type(self) -> None:
        for defn in self.registry.all():
            for port in defn.ports:
                assert port.data_type in DataType, f"{defn.type}.{port.id} has invalid data_type"
