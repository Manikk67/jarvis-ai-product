"""Tests for command registry and command execution."""

from core.command_registry import find_command, is_whitelisted
from core.jarvis_engine import handle_commands
from commands.register_commands import register_all_commands


def test_commands_registered():
    register_all_commands()
    assert find_command("open youtube") is not None
    assert find_command("yt") is not None
    assert find_command("study workspace") is not None


def test_alias_matching():
    register_all_commands()
    yt = find_command("launch youtube")
    chrome = find_command("open chrome")
    assert yt is not None
    assert chrome is not None
    assert yt.name != chrome.name


def test_time_command():
    response = handle_commands("what time is it")
    assert "time is" in response.lower()


def test_date_command():
    response = handle_commands("today's date")
    assert "date is" in response.lower()


def test_hello_command():
    response = handle_commands("hello")
    assert "hello" in response.lower() or "assist" in response.lower()


def test_help_command():
    response = handle_commands("help")
    assert "commands" in response.lower()


def test_unknown_command():
    response = handle_commands("xyzzy_plugh_random")
    assert "unknown" in response.lower()


def test_whitelist_ai_patterns():
    register_all_commands()
    assert is_whitelisted("explain quantum computing")
    assert is_whitelisted("summarize this article")


def test_natural_language_prefix_stripped():
    register_all_commands()
    cmd = find_command("hey jarvis open youtube")
    assert cmd is not None
    assert "youtube" in cmd.name
