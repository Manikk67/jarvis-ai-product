"""Unified JARVIS command engine — single entry point for all interfaces."""

import logging

from core.ai_engine import ask_ai
from core.command_registry import find_command, is_whitelisted
from core.config_loader import ensure_data_dirs
from commands.register_commands import register_all_commands

logger = logging.getLogger(__name__)

_initialized = False


def _ensure_initialized() -> None:
    global _initialized
    if not _initialized:
        ensure_data_dirs()
        register_all_commands()
        _initialized = True


def handle_commands(command: str, *, speak_fn=None) -> str:
    """
    Process a user command and return a text response.

    Args:
        command: Raw user input.
        speak_fn: Optional TTS callback for local/voice interfaces.
    """
    if not command or not command.strip():
        return "Please send a command."

    _ensure_initialized()
    command = command.strip()

    registered = find_command(command)

    if registered:
        try:
            response = registered.handler(command)
            response = response or f"{registered.name} executed."
            logger.info("Command '%s' -> %s", command, registered.name)

            if speak_fn:
                speak_fn(response)

            return response
        except Exception as exc:
            logger.exception("Command failed: %s", command)
            error = f"Error executing '{registered.name}': {exc}"
            if speak_fn:
                speak_fn(error)
            return error

    if is_whitelisted(command):
        response = ask_ai(command)
    else:
        response = (
            "Unknown command. Send 'help' to see available commands.\n"
            "For general questions, try: explain <topic> or summarize <text>."
        )

    if speak_fn:
        speak_fn(response)

    return response
