"""Tests for app discovery and path resolution."""

from unittest.mock import patch

from core.app_discovery import get_app_path, launch_browser_url, launch_folder
from core.config_loader import save_app_path


def test_saved_app_path_used():
    save_app_path("testapp", "C:\\fake\\testapp.exe")
    with patch("core.app_discovery.Path.exists", return_value=True):
        path = get_app_path("testapp")
    assert path == "C:\\fake\\testapp.exe"


def test_browser_url_launch():
    with patch("webbrowser.open") as mock_open:
        result = launch_browser_url("youtube")
    assert result is True
    mock_open.assert_called_once()


def test_folder_resolution():
    with patch("core.app_discovery._resolve_folder", return_value="C:\\Users\\Desktop"):
        with patch("os.startfile") as mock_start:
            result = launch_folder("desktop")
    assert result is True
    mock_start.assert_called_once()


def test_app_not_found_without_path():
    path = get_app_path("nonexistent_app_xyz")
    assert path is None
