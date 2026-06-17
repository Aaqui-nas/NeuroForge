# mypy: disable-error-code="empty-body"
from __future__ import annotations

import dataclasses
import json
from datetime import datetime
from pathlib import Path

FORMAT_VERSION = 1


@dataclasses.dataclass(frozen=True)
class ProjectConfig:
    """Immutable metadata for a NeuroForge project.

    Attributes:
        name: Human-readable project name.
        description: Short description of the project's purpose.
        root: Absolute path to the project directory on disk.
        created_at: Timestamp of project creation.
        format_version: JSON schema version for forward-compatibility.
    """

    name: str
    description: str
    root: Path
    created_at: datetime
    format_version: int = FORMAT_VERSION


@dataclasses.dataclass
class Project:
    """A NeuroForge project, backed by a directory on disk.

    The project directory has the following layout::

        <root>/
          project.json    # serialized ProjectConfig
          graphs/         # one JSON file per Graph
          components/     # one JSON file per ComponentDefinition

    Attributes:
        config: Immutable project metadata.
    """

    config: ProjectConfig

    @classmethod
    def create(cls, name: str, description: str, root: Path) -> Project:
        """Create a new in-memory project (does not write to disk).

        Args:
            name: Project name.
            description: Short description.
            root: Directory that will contain the project files.

        Returns:
            A new unsaved `Project` instance.
        """
        return cls(ProjectConfig(name, description, root, datetime.now()))

    @classmethod
    def load(cls, root: Path) -> Project:
        """Load a project from an existing directory.

        Args:
            root: Path to the project root directory.

        Returns:
            The deserialized `Project`.

        Raises:
            FileNotFoundError: If `root/project.json` does not exist.
            KeyError: If the JSON is missing expected fields.
        """
        with open(root / "project.json") as f:
            data = json.load(f)

        config_data = data["config"]
        config = ProjectConfig(
            name=config_data["name"],
            description=config_data["description"],
            root=Path(config_data["root"]),
            created_at=datetime.fromisoformat(config_data["created_at"]),
            format_version=config_data["format_version"],
        )
        return cls(config)

    def save(self) -> None:
        """Persist the project config to `<root>/project.json`.

        Creates `root` and any missing parent directories automatically.
        """
        data = dataclasses.asdict(self)
        data["config"]["root"] = str(data["config"]["root"])
        data["config"]["created_at"] = data["config"]["created_at"].isoformat()

        self.config.root.mkdir(parents=True, exist_ok=True)
        with open(self.config.root / "project.json", "w") as f:
            json.dump(data, f, indent=4)

    def graph_dir(self) -> Path:
        """Return the directory where graph JSON files are stored."""
        return self.config.root / "graphs"

    def component_dir(self) -> Path:
        """Return the directory where component JSON files are stored."""
        return self.config.root / "components"
