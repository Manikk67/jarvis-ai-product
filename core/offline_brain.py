import random

import config


def get_offline_response(command: str) -> str:
    command = command.lower()
    user = config.USER_NAME
    assistant = config.ASSISTANT_NAME

    if any(g in command for g in ("hello", "hi", "hey", "good morning", "good evening")):
        return f"Hello {user}. How can I assist you today?"

    if "who are you" in command:
        return f"I am {assistant}, your personal productivity assistant."

    if "motivate me" in command or "motivation" in command or "inspire" in command:
        motivations = [
            "Success comes from consistency.",
            "Small daily progress creates big success.",
            "Discipline is more powerful than motivation.",
            "Focus now. Your future self will thank you.",
        ]
        return random.choice(motivations)

    return f"Hello {user}. Send 'help' to see what I can do."
