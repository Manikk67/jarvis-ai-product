"""
Command registry — single source of truth for all JARVIS commands.

Each command registers aliases so natural language variations map to one action.
"""

import logging
import re
from dataclasses import dataclass, field
from typing import Callable, Optional

logger = logging.getLogger(__name__)

CommandHandler = Callable[[str], Optional[str]]


@dataclass
class RegisteredCommand:
    name: str
    aliases: list[str]
    handler: CommandHandler
    category: str
    description: str = ""
    _normalized_aliases: set[str] = field(default_factory=set, init=False, repr=False)

    def __post_init__(self) -> None:
        self._normalized_aliases = {_normalize(a) for a in [self.name, *self.aliases]}

    def matches(self, command: str) -> bool:
        normalized = _normalize(command)
        if normalized in self._normalized_aliases:
            return True
        for alias in self._normalized_aliases:
            if normalized == alias or normalized.startswith(alias + " "):
                return True
        return False


_registry: list[RegisteredCommand] = []
_alias_map: dict[str, RegisteredCommand] = {}


def reset_registry() -> None:
    """Clear registry — for testing only."""
    _registry.clear()
    _alias_map.clear()


def _normalize(text: str) -> str:
    text = text.lower().strip()
    for prefix in ("jarvis ", "hey jarvis ", "please "):
        if text.startswith(prefix):
            text = text[len(prefix):]
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def register_command(
    name: str,
    aliases: Optional[list] = None,
    category: str = "general",
    description: str = "",
) -> Callable[[CommandHandler], CommandHandler]:
    def decorator(handler: CommandHandler) -> CommandHandler:
        cmd = RegisteredCommand(
            name=name,
            aliases=aliases or [],
            handler=handler,
            category=category,
            description=description,
        )
        _registry.append(cmd)
        for alias in cmd._normalized_aliases:
            _alias_map[alias] = cmd
        logger.debug("Registered command: %s (%d aliases)", name, len(cmd._normalized_aliases))
        return handler

    return decorator


def find_command(command: str) -> Optional[RegisteredCommand]:
    normalized = _normalize(command)

    if normalized in _alias_map:
        return _alias_map[normalized]

    for cmd in _registry:
        if cmd.matches(normalized):
            return cmd

    return None


def get_all_commands() -> list[RegisteredCommand]:
    return list(_registry)


def get_command_list_text() -> str:
    lines = ["Available commands:"]
    by_category: dict[str, list[RegisteredCommand]] = {}

    for cmd in _registry:
        by_category.setdefault(cmd.category, []).append(cmd)

    for category, commands in sorted(by_category.items()):
        lines.append(f"\n{category.upper()}:")
        for cmd in commands:
            alias_preview = ", ".join(sorted(cmd._normalized_aliases)[:5])
            lines.append(f"  • {cmd.name} — {alias_preview}")

    return "\n".join(lines)


def is_whitelisted(command: str) -> bool:
    """Check if command matches a registered command or is an AI fallback pattern."""
    if find_command(command):
        return True

    normalized = _normalize(command)
    ai_patterns = (
        "explain ",
        "summarize ",
        "what is ",
        "how do ",
        "tell me ",
    )
    return any(normalized.startswith(p) for p in ai_patterns)
