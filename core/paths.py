"""Project path constants — always resolve from project root."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
CONFIG_DIR = PROJECT_ROOT / "config"

SETTINGS_FILE = CONFIG_DIR / "settings.json"
WORKSPACE_CONFIG_FILE = CONFIG_DIR / "workspace_config.json"
APP_PATHS_FILE = DATA_DIR / "app_paths.json"
REMINDERS_FILE = DATA_DIR / "reminders.json"
