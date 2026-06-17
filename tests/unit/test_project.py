from __future__ import annotations

import dataclasses
import json
from datetime import datetime
from pathlib import Path

import pytest

from neuroforge.core.project import FORMAT_VERSION, Project, ProjectConfig

# ── ProjectConfig ────────────────────────────────────────────────────────────


def test_project_config_is_frozen(tmp_path: Path) -> None:
    config = ProjectConfig("x", "y", tmp_path, datetime.now())
    with pytest.raises((dataclasses.FrozenInstanceError, AttributeError)):
        config.name = "z"  # type: ignore[misc]


def test_project_config_default_format_version(tmp_path: Path) -> None:
    config = ProjectConfig("x", "y", tmp_path, datetime.now())
    assert config.format_version == FORMAT_VERSION


# ── Project.create ───────────────────────────────────────────────────────────


def test_create_returns_project(tmp_path: Path) -> None:
    project = Project.create("MyNet", "A test network", tmp_path)
    assert isinstance(project, Project)


def test_create_sets_name_and_description(tmp_path: Path) -> None:
    project = Project.create("MyNet", "desc", tmp_path)
    assert project.config.name == "MyNet"
    assert project.config.description == "desc"


def test_create_sets_root(tmp_path: Path) -> None:
    project = Project.create("MyNet", "desc", tmp_path)
    assert project.config.root == tmp_path


def test_create_sets_created_at_close_to_now(tmp_path: Path) -> None:
    before = datetime.now()
    project = Project.create("MyNet", "desc", tmp_path)
    after = datetime.now()
    assert before <= project.config.created_at <= after


def test_create_does_not_write_to_disk(tmp_path: Path) -> None:
    Project.create("MyNet", "desc", tmp_path)
    assert not (tmp_path / "project.json").exists()


# ── Project.save ─────────────────────────────────────────────────────────────


def test_save_creates_project_json(tmp_path: Path) -> None:
    project = Project.create("MyNet", "desc", tmp_path)
    project.save()
    assert (tmp_path / "project.json").exists()


def test_save_creates_root_directory_if_missing(tmp_path: Path) -> None:
    root = tmp_path / "new" / "nested" / "project"
    project = Project.create("MyNet", "desc", root)
    project.save()
    assert (root / "project.json").exists()


def test_save_writes_valid_json(tmp_path: Path) -> None:
    project = Project.create("MyNet", "desc", tmp_path)
    project.save()
    with open(tmp_path / "project.json") as f:
        data = json.load(f)
    assert isinstance(data, dict)


def test_save_json_contains_expected_fields(tmp_path: Path) -> None:
    project = Project.create("MyNet", "desc", tmp_path)
    project.save()
    with open(tmp_path / "project.json") as f:
        data = json.load(f)
    cfg = data["config"]
    assert cfg["name"] == "MyNet"
    assert cfg["description"] == "desc"
    assert "root" in cfg
    assert "created_at" in cfg
    assert cfg["format_version"] == FORMAT_VERSION


def test_save_serializes_root_as_string(tmp_path: Path) -> None:
    project = Project.create("MyNet", "desc", tmp_path)
    project.save()
    with open(tmp_path / "project.json") as f:
        data = json.load(f)
    assert isinstance(data["config"]["root"], str)


def test_save_serializes_created_at_as_iso_string(tmp_path: Path) -> None:
    project = Project.create("MyNet", "desc", tmp_path)
    project.save()
    with open(tmp_path / "project.json") as f:
        data = json.load(f)
    iso = data["config"]["created_at"]
    assert isinstance(iso, str)
    datetime.fromisoformat(iso)  # must not raise


# ── Project.load ─────────────────────────────────────────────────────────────


def test_load_raises_if_directory_missing(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        Project.load(tmp_path / "nonexistent")


def test_load_raises_if_project_json_missing(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        Project.load(tmp_path)


def test_load_returns_project(tmp_path: Path) -> None:
    Project.create("MyNet", "desc", tmp_path).save()
    project = Project.load(tmp_path)
    assert isinstance(project, Project)


# ── Round-trip ───────────────────────────────────────────────────────────────


def test_roundtrip_preserves_name(tmp_path: Path) -> None:
    Project.create("MyNet", "desc", tmp_path).save()
    assert Project.load(tmp_path).config.name == "MyNet"


def test_roundtrip_preserves_description(tmp_path: Path) -> None:
    Project.create("MyNet", "my desc", tmp_path).save()
    assert Project.load(tmp_path).config.description == "my desc"


def test_roundtrip_preserves_root(tmp_path: Path) -> None:
    Project.create("MyNet", "desc", tmp_path).save()
    assert Project.load(tmp_path).config.root == tmp_path


def test_roundtrip_preserves_created_at(tmp_path: Path) -> None:
    original = Project.create("MyNet", "desc", tmp_path)
    original.save()
    loaded = Project.load(tmp_path)
    assert loaded.config.created_at == original.config.created_at


def test_roundtrip_preserves_format_version(tmp_path: Path) -> None:
    Project.create("MyNet", "desc", tmp_path).save()
    assert Project.load(tmp_path).config.format_version == FORMAT_VERSION


# ── Helpers ──────────────────────────────────────────────────────────────────


def test_graph_dir_is_under_root(tmp_path: Path) -> None:
    project = Project.create("MyNet", "desc", tmp_path)
    assert project.graph_dir() == tmp_path / "graphs"


def test_component_dir_is_under_root(tmp_path: Path) -> None:
    project = Project.create("MyNet", "desc", tmp_path)
    assert project.component_dir() == tmp_path / "components"


def test_graph_dir_and_component_dir_are_distinct(tmp_path: Path) -> None:
    project = Project.create("MyNet", "desc", tmp_path)
    assert project.graph_dir() != project.component_dir()
