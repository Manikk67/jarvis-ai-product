from automation.pc_control import (
    shutdown_pc,
    restart_pc,
    lock_pc,
    open_task_manager
)

from core.voice_engine import speak

# ==========================================
# HANDLE SYSTEM COMMANDS
# ==========================================

def handle_system_commands(command):

    command = command.lower()

    # SHUTDOWN
    if "shutdown computer" in command:

        speak("Shutting down computer")

        shutdown_pc()

        return True

    # RESTART
    elif "restart computer" in command:

        speak("Restarting computer")

        restart_pc()

        return True

    # LOCK
    elif "lock computer" in command:

        speak("Locking computer")

        lock_pc()

        return True

    # TASK MANAGER
    elif "task manager" in command:

        speak("Opening task manager")

        open_task_manager()

        return True

    return False