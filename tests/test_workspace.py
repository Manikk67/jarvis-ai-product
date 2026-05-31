"""Tests for workspace configuration and execution."""

from unittest.mock import patch

from automation.workspace_automation import start_workspace
from core.config_loader import load_workspace_config


def test_workspace_config_loaded():
    config = load_workspace_config()
    assert "study workspace" in config
    assert "work workspace" in config


def test_study_workspace_items():
    config = load_workspace_config()
    study = config["study workspace"]
    targets = [item["target"] for item in study["items"]]
    assert "documents" in targets
    assert "chrome" in targets
    assert "chatgpt" in targets
    assert "notepad" in targets


def test_work_workspace_items():
    config = load_workspace_config()
    work = config["work workspace"]
    targets = [item["target"] for item in work["items"]]
    assert "chrome" in targets
    assert "chatgpt" in targets
    assert "gemini" in targets
    assert "whatsapp" in targets


@patch("automation.workspace_automation._launch_item", return_value=True)
def test_start_workspace(mock_launch):
    result = start_workspace("study workspace")
    assert "started" in result.lower()
    assert mock_launch.call_count == 4


def test_unknown_workspace():
    result = start_workspace("nonexistent workspace")
    assert "not found" in result.lower()
