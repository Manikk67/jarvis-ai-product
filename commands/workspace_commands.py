from automation.workspace_automation import (
    start_study_workspace,
    start_coding_workspace
)

from core.voice_engine import speak

# ==========================================
# HANDLE WORKSPACE COMMANDS
# ==========================================

def handle_workspace_commands(command):

    command = command.lower()

    # STUDY WORKSPACE
    if "study workspace" in command:

        speak("Starting study workspace")

        start_study_workspace()

        return True

    # CODING WORKSPACE
    elif "coding workspace" in command:

        speak("Starting coding workspace")

        start_coding_workspace()

        return True

    return False