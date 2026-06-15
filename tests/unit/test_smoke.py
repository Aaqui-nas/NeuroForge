"""Smoke tests — verify the package is importable and minimally functional."""

import importlib


def test_package_importable() -> None:
    mod = importlib.import_module("neuroforge")
    assert mod is not None


def test_submodules_importable() -> None:
    submodules = [
        "neuroforge.core",
        "neuroforge.graph",
        "neuroforge.training",
        "neuroforge.datasets",
        "neuroforge.tracking",
        "neuroforge.storage",
        "neuroforge.visualization",
        "neuroforge.ui",
    ]
    for name in submodules:
        mod = importlib.import_module(name)
        assert mod is not None, f"{name} could not be imported"
