"""Load and persist JSON configuration files."""

import json
import logging
from pathlib import Path
from typing import Any

from core.paths import (
    APP_PATHS_FILE,
    CONFIG_DIR,
    DATA_DIR,
    REMINDERS_FILE,
    SETTINGS_FILE,
    WORKSPACE_CONFIG_FILE,
)

logger = logging.getLogger(__name__)


def _read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except (json.JSONDecodeError, OSError) as exc:
        logger.warning("Failed to read %s: %s", path, exc)
        return default


def _write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)


def ensure_data_dirs() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if not APP_PATHS_FILE.exists():
        _write_json(APP_PATHS_FILE, {})
    if not REMINDERS_FILE.exists():
        _write_json(REMINDERS_FILE, [])


def load_settings() -> dict:
    return _read_json(SETTINGS_FILE, {})


def load_workspace_config() -> dict:
    return _read_json(WORKSPACE_CONFIG_FILE, {})


def load_app_paths() -> dict:
    ensure_data_dirs()
    return _read_json(APP_PATHS_FILE, {})


def save_app_path(name: str, path: str) -> None:
    apps = load_app_paths()
    apps[name.lower()] = path
    _write_json(APP_PATHS_FILE, apps)
    logger.info("Saved app path: %s -> %s", name, path)


def load_reminders() -> list:
    ensure_data_dirs()
    return _read_json(REMINDERS_FILE, [])


def save_reminders(reminders: list) -> None:
    ensure_data_dirs()
    _write_json(REMINDERS_FILE, reminders)
