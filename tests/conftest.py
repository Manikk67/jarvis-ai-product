"""Pytest configuration and shared fixtures."""

import json
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture(autouse=True)
def reset_command_state(tmp_path, monkeypatch):
    """Isolate tests with temp data directory and fresh command registry."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    monkeypatch.setattr("core.paths.DATA_DIR", data_dir)
    monkeypatch.setattr("core.paths.APP_PATHS_FILE", data_dir / "app_paths.json")
    monkeypatch.setattr("core.paths.REMINDERS_FILE", data_dir / "reminders.json")
    monkeypatch.setattr("core.config_loader.DATA_DIR", data_dir)
    monkeypatch.setattr("core.config_loader.APP_PATHS_FILE", data_dir / "app_paths.json")
    monkeypatch.setattr("core.config_loader.REMINDERS_FILE", data_dir / "reminders.json")

    (data_dir / "app_paths.json").write_text("{}")
    (data_dir / "reminders.json").write_text("[]")

    from commands.register_commands import reset_registration
    from core import jarvis_engine

    reset_registration()
    jarvis_engine._initialized = False

    yield

    reset_registration()
    jarvis_engine._initialized = False
