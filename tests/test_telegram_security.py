"""Tests for Telegram security configuration."""

import config
from commands.register_commands import register_all_commands
from core.command_registry import is_whitelisted
from core.jarvis_engine import handle_commands

PROJECT_ROOT = __import__("pathlib").Path(__file__).resolve().parent.parent


def test_admin_user_id_is_integer():
    assert isinstance(config.TELEGRAM_ADMIN_USER_ID, int)


def test_password_not_hardcoded_in_source():
    source = (PROJECT_ROOT / "core" / "telegram_bot.py").read_text(encoding="utf-8")
    assert "200519" not in source
    assert "AAHAjTBRx" not in source


def test_whitelist_blocks_random_commands():
    response = handle_commands("rm -rf /")
    assert "unknown" in response.lower()


def test_whitelist_allows_registered():
    register_all_commands()
    assert is_whitelisted("open youtube")
    assert is_whitelisted("help")


def test_env_vars_defined():
    assert hasattr(config, "TELEGRAM_BOT_TOKEN")
    assert hasattr(config, "TELEGRAM_PASSWORD")
    assert hasattr(config, "TELEGRAM_ADMIN_USER_ID")
