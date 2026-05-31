"""Config-driven workspace launcher."""

import logging
import time

from core.app_discovery import launch_app, launch_browser_url, launch_folder
from core.config_loader import load_workspace_config

logger = logging.getLogger(__name__)


def _launch_item(item: dict) -> bool:
    item_type = item.get("type", "")
    target = item.get("target", "")

    if item_type == "app":
        return launch_app(target)
    if item_type == "browser":
        return launch_browser_url(target)
    if item_type == "folder":
        return launch_folder(target)

    logger.warning("Unknown workspace item type: %s", item_type)
    return False


def start_workspace(name: str) -> str:
    config = load_workspace_config()
    normalized = name.lower().strip()

    if normalized not in config:
        available = ", ".join(config.keys())
        return f"Workspace '{name}' not found. Available: {available}"

    workspace = config[normalized]
    items = workspace.get("items", [])
    launched = 0

    for item in items:
        if _launch_item(item):
            launched += 1
        time.sleep(0.5)

    description = workspace.get("description", normalized)
    return f"Started '{normalized}' workspace ({launched}/{len(items)} items). {description}"
