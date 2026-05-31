"""Automatic Windows application discovery and path resolution."""

import logging
import os
from pathlib import Path
from typing import Optional

from core.config_loader import load_app_paths, load_settings, save_app_path

logger = logging.getLogger(__name__)

_SEARCH_DEPTH = 4
_MAX_SEARCH_DIRS = 200


def _expand_path(path: str) -> Path:
    return Path(os.path.expandvars(os.path.expanduser(path)))


def _resolve_folder(name: str) -> Optional[str]:
    settings = load_settings()
    aliases = settings.get("folder_aliases", {})
    candidates = aliases.get(name.lower(), [name.capitalize()])
    home = Path.home()

    for candidate in candidates:
        folder = home / candidate
        if folder.is_dir():
            return str(folder)

    return None


def _search_in_directory(root: Path, names: list, depth: int = 0) -> Optional[str]:
    if depth > _SEARCH_DEPTH or not root.is_dir():
        return None

    try:
        for entry in root.iterdir():
            if entry.is_file() and entry.name.lower() in [n.lower() for n in names]:
                return str(entry)
            if entry.is_file() and entry.suffix.lower() == ".lnk":
                if any(n.lower() in entry.name.lower() for n in names):
                    return str(entry)
    except OSError:
        return None

    if depth < _SEARCH_DEPTH:
        try:
            for entry in root.iterdir():
                if entry.is_dir():
                    found = _search_in_directory(entry, names, depth + 1)
                    if found:
                        return found
        except OSError:
            pass

    return None


def _discover_app(app_name: str) -> Optional[str]:
    settings = load_settings()
    discovery = settings.get("app_discovery", {})
    known = discovery.get("known_apps", {})
    search_names = known.get(app_name.lower(), [f"{app_name}.exe"])

    search_locations = discovery.get("search_locations", [])
    searched = 0

    for location in search_locations:
        root = _expand_path(location)
        if not root.exists():
            continue

        found = _search_in_directory(root, search_names)
        if found:
            logger.info("Discovered %s at %s", app_name, found)
            return found

        searched += 1
        if searched >= _MAX_SEARCH_DIRS:
            break

    return None


def get_app_path(app_name: str, prompt_callback=None) -> Optional[str]:
    """Resolve app path from cache, discovery, or user prompt."""
    name = app_name.lower()
    saved = load_app_paths()

    if name in saved and Path(saved[name]).exists():
        return saved[name]

    discovered = _discover_app(name)
    if discovered:
        save_app_path(name, discovered)
        return discovered

    if prompt_callback:
        user_path = prompt_callback(app_name)
        if user_path and Path(user_path).exists():
            save_app_path(name, user_path)
            return user_path

    logger.warning("App not found: %s", app_name)
    return None


def launch_app(app_name: str, prompt_callback=None) -> bool:
    path = get_app_path(app_name, prompt_callback)
    if not path:
        return False

    try:
        os.startfile(path)
        return True
    except OSError as exc:
        logger.error("Failed to launch %s: %s", app_name, exc)
        return False


def launch_folder(folder_name: str) -> bool:
    path = _resolve_folder(folder_name)
    if not path:
        return False

    try:
        os.startfile(path)
        return True
    except OSError as exc:
        logger.error("Failed to open folder %s: %s", folder_name, exc)
        return False


def launch_browser_url(url_key: str) -> bool:
    settings = load_settings()
    urls = settings.get("browser_urls", {})
    url = urls.get(url_key.lower())

    if not url:
        return False

    import webbrowser

    webbrowser.open(url)
    return True
