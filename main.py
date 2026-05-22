from core.voice_engine import (
    speak,
    take_command
)

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

from automation.reminder_system import (
    add_reminder,
    start_reminder_system
)

from automation.file_searcher import (
    search_files
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

import webbrowser
import datetime
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

    # OPEN APPS
    for app in apps:

        if app in command:

            os.startfile(apps[app])

            speak(f"Opening {app}")

            return True

    # OPEN FOLDERS
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
# HANDLE COMMANDS
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

        return

    # ==========================================
    # MEDIA COMMANDS
    # ==========================================

    if handle_media_commands(command):

        return

    # ==========================================
    # SYSTEM COMMANDS
    # ==========================================

    if handle_system_commands(command):

        return

    # ==========================================
    # WORKSPACE COMMANDS
    # ==========================================

    if handle_workspace_commands(command):

        return

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

    # ==========================================
    # TIME
    # ==========================================

    elif "time" in command:

        current = datetime.datetime.now().strftime(
            "%I:%M %p"
        )

        speak(f"The time is {current}")

    # ==========================================
    # DATE
    # ==========================================

    elif "date" in command:

        today = datetime.datetime.now().strftime(
            "%d %B %Y"
        )

        speak(f"Today's date is {today}")

    # ==========================================
    # YOUTUBE
    # ==========================================

    elif "youtube" in command:

        speak("Opening YouTube")

        webbrowser.open("https://youtube.com")

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

            url = (
                f"https://google.com/search?q={query}"
            )

            webbrowser.open(url)

        else:

            speak("Please say what to search.")

    # ==========================================
    # FIND FILES
    # ==========================================

    elif "find" in command:

        filename = command.replace(
            "find",
            ""
        ).strip()

        speak(f"Searching for {filename}")

        results = search_files(filename)

        if results:

            speak(
                f"I found {len(results)} matching files."
            )

            for file in results[:5]:

                print(f"\n📂 {file}")

        else:

            speak("No matching files found.")

    # ==========================================
    # OPEN APPS / FOLDERS
    # ==========================================

    elif "open" in command:

        if not open_apps(command):

            speak(
                "Application or folder not found"
            )

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

                speak(study_topics[key])

                found = True

                break

        if not found:

            speak("Study topic not found.")

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

            speak("Note saved successfully.")

        else:

            speak("Please say the note.")

    # ==========================================
    # SHOW NOTES
    # ==========================================

    elif "show notes" in command:

        notes = show_notes()

        if notes:

            for note in notes:

                speak(note)

        else:

            speak("No notes found.")

    # ==========================================
    # REMEMBER APP
    # ==========================================

    elif "remember app" in command:

        app_name = command.replace(
            "remember app",
            ""
        ).strip()

        speak(
            f"Enter full path for {app_name}"
        )

        app_path = input("📁 App Path: ")

        add_app(app_name, app_path)

        speak(
            f"{app_name} saved successfully."
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

            speak(f"Launching {app_name}")

        else:

            speak("Saved app not found.")

    # ==========================================
    # REMINDER SYSTEM
    # ==========================================

    elif "remind me" in command:

        try:

            speak(
                "What should I remind you about?"
            )

            reminder_message = input(
                "📝 Reminder Message: "
            )

            speak(
                "Enter reminder time in seconds"
            )

            seconds = int(
                input("⏳ Seconds: ")
            )

            add_reminder(
                reminder_message,
                seconds
            )

            speak(
                "Reminder added successfully."
            )

        except:

            speak("Invalid reminder input.")

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

        response = get_offline_response(
            command
        )

        speak(response)

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

# ==========================================
# MAIN SYSTEM
# ==========================================

def main():

    start_reminder_system()

    print("=" * 50)
    print("🤖 JARVIS AI SYSTEM")
    print("=" * 50)

    print("\nChoose Input Mode:")
    print("1. Voice Mode 🎤")
    print("2. Text Mode 💬")

    mode = input(
        "\nEnter choice (1 or 2): "
    )

    speak("Jarvis system initialized")

    # VOICE MODE
    if mode == "1":

        while True:

            command = take_command()

            if command:

                handle_commands(command)

    # TEXT MODE
    elif mode == "2":

        while True:

            command = input(
                "\n💬 You: "
            ).lower()

            handle_commands(command)

    else:

        print("❌ Invalid mode selected")

# ==========================================

if __name__ == "__main__":

    main()