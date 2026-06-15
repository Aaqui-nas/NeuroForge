from pathlib import Path

import pytest


@pytest.fixture
def tmp_project_dir(tmp_path: Path) -> Path:
    """Temporary directory simulating a NeuroForge project root."""
    (tmp_path / ".neuroforge").mkdir()
    (tmp_path / ".neuroforge" / "objects").mkdir()
    (tmp_path / ".neuroforge" / "refs").mkdir()
    (tmp_path / ".neuroforge" / "metadata").mkdir()
    return tmp_path
