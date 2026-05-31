"""Register all JARVIS commands with the command registry."""

import datetime
import os

from automation.brightness_control import brightness_down, brightness_up
from automation.pc_control import lock_pc, restart_pc, shutdown_pc
from automation.reminder_system import (
    add_reminder_from_text,
    delete_reminder_from_text,
    list_reminders,
)
from automation.screenshot_system import take_screenshot
from automation.volume_control import (
    mute_volume,
    parse_volume_command,
    unmute_volume,
    volume_down,
    volume_up,
)
from automation.workspace_automation import start_workspace
from core.ai_engine import ask_ai
from core.app_discovery import launch_app, launch_browser_url, launch_folder
from core.command_registry import register_command
from core.config_loader import load_settings
from core.offline_brain import get_offline_response

_registered = False


def reset_registration() -> None:
    """Reset command registration — for testing only."""
    global _registered
    from core.command_registry import reset_registry
    reset_registry()
    _registered = False


def register_all_commands() -> None:
    """Call once at startup to populate the command registry."""
    global _registered
    if _registered:
        return
    _registered = True

    settings = load_settings()
    vol_step = settings.get("volume_step", 0.1)
    bright_step = settings.get("brightness_step", 10)

    # ── SYSTEM ──────────────────────────────────────────

    @register_command("brightness up", ["increase brightness", "brighter"], "system")
    def cmd_brightness_up(_cmd: str) -> str:
        return brightness_up(bright_step)

    @register_command("brightness down", ["decrease brightness", "dimmer"], "system")
    def cmd_brightness_down(_cmd: str) -> str:
        return brightness_down(bright_step)

    @register_command("volume up", ["increase volume", "louder"], "system")
    def cmd_volume_up(_cmd: str) -> str:
        return volume_up(vol_step)

    @register_command("volume down", ["decrease volume", "quieter"], "system")
    def cmd_volume_down(_cmd: str) -> str:
        return volume_down(vol_step)

    @register_command("mute volume", ["mute", "silence"], "system")
    def cmd_mute(_cmd: str) -> str:
        return mute_volume()

    @register_command("unmute volume", ["unmute", "unsilence"], "system")
    def cmd_unmute(_cmd: str) -> str:
        return unmute_volume()

    @register_command("volume set", ["volume up to", "volume down to", "set volume"], "system")
    def cmd_volume_set(cmd: str) -> str:
        result = parse_volume_command(cmd)
        return result or "Say: volume up to 50% or set volume to 30%."

    @register_command("screenshot", ["take screenshot", "capture screen"], "system")
    def cmd_screenshot(_cmd: str) -> str:
        filepath = take_screenshot()
        return f"Screenshot saved: {filepath}"

    @register_command("open cmd", ["open command prompt", "open terminal"], "system")
    def cmd_open_cmd(_cmd: str) -> str:
        os.system("start cmd")
        return "Opening Command Prompt."

    @register_command("lock computer", ["lock pc", "lock screen"], "system")
    def cmd_lock(_cmd: str) -> str:
        lock_pc()
        return "Locking computer."

    @register_command("shutdown computer", ["shutdown pc", "shutdown"], "system")
    def cmd_shutdown(_cmd: str) -> str:
        shutdown_pc()
        return "Shutting down computer."

    @register_command("restart computer", ["restart pc", "reboot"], "system")
    def cmd_restart(_cmd: str) -> str:
        restart_pc()
        return "Restarting computer."

    # ── FILES ───────────────────────────────────────────

    for folder in ("desktop", "documents", "downloads", "pictures", "videos"):
        _register_folder_command(folder)

    # ── APPS ────────────────────────────────────────────

    browser_apps = {
        "youtube": ["open youtube", "launch youtube", "yt"],
        "chatgpt": ["open chatgpt", "launch chatgpt"],
        "gemini": ["open gemini", "launch gemini"],
        "copilot": ["open copilot", "launch copilot"],
        "whatsapp": ["open whatsapp", "launch whatsapp"],
    }

    for app, aliases in browser_apps.items():
        _register_browser_command(app, aliases)

    local_apps = {
        "chrome": ["open chrome", "launch chrome"],
        "cursor": ["open cursor", "launch cursor"],
        "files": ["open files", "open file explorer", "open explorer"],
        "python": ["open python", "launch python"],
        "notepad": ["open notepad", "launch notepad"],
    }

    for app, aliases in local_apps.items():
        _register_app_command(app, aliases)

    # ── WORKSPACES ──────────────────────────────────────

    @register_command(
        "study workspace",
        ["start study workspace", "study mode"],
        "workspace",
    )
    def cmd_study_workspace(_cmd: str) -> str:
        return start_workspace("study workspace")

    @register_command(
        "work workspace",
        ["start work workspace", "work mode", "coding workspace"],
        "workspace",
    )
    def cmd_work_workspace(_cmd: str) -> str:
        return start_workspace("work workspace")

    # ── AI / OFFLINE ────────────────────────────────────

    @register_command("hello", ["hi", "hey", "good morning", "good evening"], "ai")
    def cmd_hello(cmd: str) -> str:
        return get_offline_response(cmd)

    @register_command("time", ["what time is it", "current time"], "ai")
    def cmd_time(_cmd: str) -> str:
        current = datetime.datetime.now().strftime("%I:%M %p")
        return f"The time is {current}."

    @register_command("date", ["what is the date", "today's date", "today date"], "ai")
    def cmd_date(_cmd: str) -> str:
        today = datetime.datetime.now().strftime("%d %B %Y")
        return f"Today's date is {today}."

    @register_command("motivate me", ["motivation", "inspire me"], "ai")
    def cmd_motivate(cmd: str) -> str:
        return get_offline_response(cmd)

    @register_command("explain this", ["explain", "what is"], "ai")
    def cmd_explain(cmd: str) -> str:
        return ask_ai(cmd)

    @register_command("summarize this", ["summarize", "summary"], "ai")
    def cmd_summarize(cmd: str) -> str:
        return ask_ai(f"Summarize the following: {cmd}")

    # ── REMINDERS ───────────────────────────────────────

    @register_command("remind me", ["remind me to", "set reminder"], "reminders")
    def cmd_remind(cmd: str) -> str:
        return add_reminder_from_text(cmd)

    @register_command("show reminders", ["list reminders", "my reminders"], "reminders")
    def cmd_show_reminders(_cmd: str) -> str:
        return list_reminders()

    @register_command("delete reminder", ["remove reminder", "cancel reminder"], "reminders")
    def cmd_delete_reminder(cmd: str) -> str:
        return delete_reminder_from_text(cmd)

    # ── HELP ────────────────────────────────────────────

    @register_command("help", ["commands", "what can you do"], "help")
    def cmd_help(_cmd: str) -> str:
        from core.command_registry import get_command_list_text
        return get_command_list_text()


def _register_folder_command(folder: str) -> None:
    aliases = [f"open {folder}", f"launch {folder}"]

    @register_command(f"open {folder}", aliases, "files")
    def handler(_cmd: str, _folder=folder) -> str:
        if launch_folder(_folder):
            return f"Opening {_folder} folder."
        return f"Could not find {_folder} folder."

    return handler


def _register_browser_command(app: str, aliases: list[str]) -> None:
    @register_command(f"open {app}", aliases, "apps")
    def handler(_cmd: str, _app=app) -> str:
        if launch_browser_url(_app):
            return f"Opening {_app}."
        return f"Could not open {_app}."

    return handler


def _register_app_command(app: str, aliases: list[str]) -> None:
    @register_command(f"open {app}", aliases, "apps")
    def handler(_cmd: str, _app=app) -> str:
        if launch_app(_app):
            return f"Opening {_app}."
        return f"Could not find {_app}. Add path to data/app_paths.json."

    return handler
