"""Tests for persistent reminder system."""

import pytest

from automation.reminder_system import (
    add_reminder,
    add_reminder_from_text,
    delete_reminder,
    list_reminders,
)
from core.config_loader import load_reminders, save_reminders


@pytest.fixture(autouse=True)
def clear_reminders():
    save_reminders([])
    yield
    save_reminders([])


def test_add_and_list_reminder():
    add_reminder("Test task", 300)
    reminders = load_reminders()
    assert len(reminders) == 1
    assert reminders[0]["message"] == "Test task"
    assert "id" in reminders[0]


def test_parse_reminder_text():
    response = add_reminder_from_text("remind me to call mom in 5 minutes")
    assert "reminder set" in response.lower()
    reminders = load_reminders()
    assert len(reminders) == 1
    assert "call mom" in reminders[0]["message"]


def test_delete_reminder():
    reminder = add_reminder("Delete me", 600)
    result = delete_reminder(reminder["id"])
    assert "deleted" in result.lower()
    assert len(load_reminders()) == 0


def test_show_empty_reminders():
    save_reminders([])
    result = list_reminders()
    assert "no active" in result.lower()


def test_invalid_reminder_text():
    result = add_reminder_from_text("remind me something")
    assert "could not parse" in result.lower() or "say:" in result.lower()
