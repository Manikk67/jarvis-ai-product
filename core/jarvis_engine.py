from core.voice_engine import speak

from core.ai_engine import ask_ai

from core.offline_brain import (
    get_offline_response
)

from commands.study_data import study_topics

from commands.notes_system import (
    save_note,
    show_notes
)

from commands.app_manager import (
    add_app,
    open_saved_app
)

from commands.command_memory import (
    add_command,
    get_command
)

from commands.media_commands import (
    handle_media_commands
)

from commands.system_commands import (
    handle_system_commands
)

from commands.workspace_commands import (
    handle_workspace_commands
)

from automation.reminder_system import (
    add_reminder
)

from automation.file_searcher import (
    search_files
)

import datetime
import webbrowser
import os

# ==========================================
# OPEN APPS + FOLDERS
# ==========================================

def open_apps(command):

    apps = {

        "chrome":
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",

        "notepad":
        "notepad.exe",

        "calculator":
        "calc.exe"
    }

    user_home = os.path.expanduser("~")

    folders = {

        "desktop":
        os.path.join(user_home, "OneDrive", "Desktop"),

        "downloads":
        os.path.join(user_home, "Downloads"),

        "documents":
        os.path.join(user_home, "OneDrive", "Documents"),

        "pictures":
        os.path.join(user_home, "OneDrive", "Pictures"),

        "music":
        os.path.join(user_home, "Music"),

        "videos":
        os.path.join(user_home, "Videos")
    }

    for app in apps:

        if app in command:

            os.startfile(apps[app])

            speak(f"Opening {app}")

            return True

    for folder in folders:

        if folder in command:

            try:

                os.startfile(folders[folder])

                speak(f"Opening {folder} folder")

                return True

            except:

                speak(f"{folder} folder not found")

                return True

    return False

# ==========================================
# MAIN COMMAND HANDLER
# ==========================================

def handle_commands(command):

    command = command.lower()

    # ==========================================
    # SAVED COMMANDS
    # ==========================================

    saved_action = get_command(command)

    if saved_action:

        speak(f"Executing saved command {command}")

        handle_commands(saved_action)

        return "Executed saved command"

    # ==========================================
    # MEDIA COMMANDS
    # ==========================================

    if handle_media_commands(command):

        return "Media command executed"

    # ==========================================
    # SYSTEM COMMANDS
    # ==========================================

    if handle_system_commands(command):

        return "System command executed"

    # ==========================================
    # WORKSPACE COMMANDS
    # ==========================================

    if handle_workspace_commands(command):

        return "Workspace command executed"

    # ==========================================
    # REMEMBER CUSTOM COMMAND
    # ==========================================

    if "remember command" in command:

        trigger = command.replace(
            "remember command",
            ""
        ).strip()

        speak("Enter action for this command")

        action = input("⚡ Action: ")

        add_command(trigger, action)

        speak("Custom command saved successfully.")

        return "Custom command saved"

    # ==========================================
    # TIME
    # ==========================================

    elif "time" in command:

        current = datetime.datetime.now().strftime(
            "%I:%M %p"
        )

        response = f"The time is {current}"

        speak(response)

        return response

    # ==========================================
    # DATE
    # ==========================================

    elif "date" in command:

        today = datetime.datetime.now().strftime(
            "%d %B %Y"
        )

        response = f"Today's date is {today}"

        speak(response)

        return response

    # ==========================================
    # YOUTUBE
    # ==========================================

    elif "youtube" in command:

        speak("Opening YouTube")

        webbrowser.open("https://youtube.com")

        return "Opening YouTube"

    # ==========================================
    # SEARCH WEB
    # ==========================================

    elif "search" in command:

        query = command.replace(
            "search",
            ""
        ).strip()

        if query:

            speak(f"Searching {query}")

            url = f"https://google.com/search?q={query}"

            webbrowser.open(url)

            return f"Searching {query}"

        else:

            return "Please say what to search"

    # ==========================================
    # FIND FILES
    # ==========================================

    elif "find" in command:

        filename = command.replace(
            "find",
            ""
        ).strip()

        results = search_files(filename)

        if results:

            response = (
                f"Found {len(results)} matching files"
            )

            speak(response)

            return response

        else:

            return "No matching files found"

    # ==========================================
    # OPEN APPS
    # ==========================================

    elif "open" in command:

        if not open_apps(command):

            return "Application or folder not found"

    # ==========================================
    # STUDY MODE
    # ==========================================

    elif "teach me" in command:

        topic = command.replace(
            "teach me",
            ""
        ).strip()

        found = False

        for key in study_topics:

            if key in topic:

                response = study_topics[key]

                speak(response)

                found = True

                return response

        if not found:

            return "Study topic not found"

    # ==========================================
    # SAVE NOTE
    # ==========================================

    elif "save note" in command:

        note = command.replace(
            "save note",
            ""
        ).strip()

        if note:

            save_note(note)

            return "Note saved successfully"

        else:

            return "Please say the note"

    # ==========================================
    # SHOW NOTES
    # ==========================================

    elif "show notes" in command:

        notes = show_notes()

        if notes:

            return "\\n".join(notes)

        else:

            return "No notes found"

    # ==========================================
    # REMEMBER APP
    # ==========================================

    elif "remember app" in command:

        return (
            "Use terminal mode for app memory setup"
        )

    # ==========================================
    # LAUNCH SAVED APP
    # ==========================================

    elif "launch" in command:

        app_name = command.replace(
            "launch",
            ""
        ).strip()

        if open_saved_app(app_name):

            return f"Launching {app_name}"

        else:

            return "Saved app not found"

    # ==========================================
    # REMINDERS
    # ==========================================

    elif "remind me" in command:

        return (
            "Reminder setup currently works "
            "in terminal mode"
        )

    # ==========================================
    # OFFLINE BRAIN
    # ==========================================

    elif (
        "hello" in command or
        "hi" in command or
        "who are you" in command or
        "motivate me" in command or
        "joke" in command
    ):

        response = get_offline_response(command)

        speak(response)

        return response

    # ==========================================
    # EXIT
    # ==========================================

    elif (
        "exit" in command or
        "stop" in command or
        "shutdown jarvis" in command
    ):

        speak("Goodbye Mani")

        exit()

    # ==========================================
    # AI CHAT
    # ==========================================

    else:

        response = ask_ai(command)

        speak(response)

        return response