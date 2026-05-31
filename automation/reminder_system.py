"""Persistent reminder system with background checker."""

import logging
import threading
import time
import uuid
from datetime import datetime, timedelta
from typing import Optional

from core.config_loader import load_reminders, save_reminders

logger = logging.getLogger(__name__)

_checker_started = False
_on_trigger = None


def set_reminder_callback(callback) -> None:
    global _on_trigger
    _on_trigger = callback


def _parse_delay(text: str) -> Optional[int]:
    """Parse delay from text like 'in 5 minutes', 'in 30 seconds', 'in 2 hours'."""
    import re

    text = text.lower()
    patterns = [
        (r"in\s+(\d+)\s*seconds?", 1),
        (r"in\s+(\d+)\s*minutes?", 60),
        (r"in\s+(\d+)\s*hours?", 3600),
        (r"in\s+(\d+)\s*secs?", 1),
        (r"in\s+(\d+)\s*mins?", 60),
        (r"in\s+(\d+)\s*hrs?", 3600),
        (r"(\d+)\s*seconds?", 1),
        (r"(\d+)\s*minutes?", 60),
    ]

    for pattern, multiplier in patterns:
        match = re.search(pattern, text)
        if match:
            return int(match.group(1)) * multiplier

    return None


def add_reminder(message: str, delay_seconds: int) -> dict:
    reminders = load_reminders()
    reminder = {
        "id": str(uuid.uuid4())[:8],
        "message": message,
        "trigger_at": (datetime.now() + timedelta(seconds=delay_seconds)).isoformat(),
        "created_at": datetime.now().isoformat(),
    }
    reminders.append(reminder)
    save_reminders(reminders)
    logger.info("Reminder added: %s in %ds", message, delay_seconds)
    return reminder


def add_reminder_from_text(text: str) -> str:
    """Parse 'remind me to call mom in 5 minutes'."""
    import re

    text = text.strip()
    match = re.match(r"remind\s+me\s+to\s+(.+)", text, re.IGNORECASE)
    if not match:
        return "Say: remind me to <task> in <time>. Example: remind me to call mom in 5 minutes."

    remainder = match.group(1).strip()
    delay = _parse_delay(remainder)

    if delay is None:
        return "Could not parse time. Try: remind me to <task> in 5 minutes."

    message = remainder
    for pattern in [
        r"\s+in\s+\d+\s*(seconds?|minutes?|hours?|secs?|mins?|hrs?)\s*$",
        r"\s+\d+\s*(seconds?|minutes?|hours?)\s*$",
    ]:
        message = re.sub(pattern, "", message, flags=re.IGNORECASE).strip()

    if not message:
        return "What should I remind you about?"

    reminder = add_reminder(message, delay)
    return f"Reminder set: '{reminder['message']}' in {delay // 60 or delay} minute(s)."


def list_reminders() -> str:
    reminders = load_reminders()
    if not reminders:
        return "No active reminders."

    lines = ["Active reminders:"]
    now = datetime.now()

    for item in reminders:
        trigger = datetime.fromisoformat(item["trigger_at"])
        remaining = max(0, int((trigger - now).total_seconds()))
        mins = remaining // 60
        secs = remaining % 60
        lines.append(
            f"  [{item['id']}] {item['message']} — in {mins}m {secs}s"
        )

    return "\n".join(lines)


def delete_reminder(reminder_id: str) -> str:
    reminders = load_reminders()
    original_count = len(reminders)
    reminders = [r for r in reminders if r["id"] != reminder_id.lower()]

    if len(reminders) == original_count:
        return f"Reminder '{reminder_id}' not found."

    save_reminders(reminders)
    return f"Reminder '{reminder_id}' deleted."


def delete_reminder_from_text(text: str) -> str:
    import re

    match = re.search(r"delete\s+reminder\s+(\w+)", text, re.IGNORECASE)
    if match:
        return delete_reminder(match.group(1))
    return "Say: delete reminder <id>. Use 'show reminders' to see IDs."


def _reminder_checker() -> None:
    while True:
        try:
            reminders = load_reminders()
            now = datetime.now()
            remaining = []

            for item in reminders:
                trigger = datetime.fromisoformat(item["trigger_at"])
                if now >= trigger:
                    msg = f"Reminder: {item['message']}"
                    logger.info(msg)
                    if _on_trigger:
                        _on_trigger(msg)
                else:
                    remaining.append(item)

            if len(remaining) != len(reminders):
                save_reminders(remaining)

        except Exception as exc:
            logger.error("Reminder checker error: %s", exc)

        time.sleep(1)


def start_reminder_system(on_trigger=None) -> None:
    global _checker_started

    if on_trigger:
        set_reminder_callback(on_trigger)

    if _checker_started:
        return

    thread = threading.Thread(target=_reminder_checker, daemon=True)
    thread.start()
    _checker_started = True
    logger.info("Reminder system started")
