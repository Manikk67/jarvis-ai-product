from automation.screenshot_system import (
    take_screenshot
)

from automation.volume_control import (
    volume_up,
    volume_down,
    mute_volume,
    unmute_volume
)

from core.voice_engine import speak

# ==========================================
# HANDLE MEDIA COMMANDS
# ==========================================

def handle_media_commands(command):

    command = command.lower()

    # SCREENSHOT
    if "screenshot" in command:

        filepath = take_screenshot()

        speak("Screenshot captured successfully.")

        print(f"📸 Saved at: {filepath}")

        return True

    # VOLUME UP
    elif "volume up" in command:

        volume_up()

        speak("Volume increased")

        return True

    # VOLUME DOWN
    elif "volume down" in command:

        volume_down()

        speak("Volume decreased")

        return True

    # MUTE
    elif "mute volume" in command:

        mute_volume()

        speak("Volume muted")

        return True

    # UNMUTE
    elif "unmute volume" in command:

        unmute_volume()

        speak("Volume unmuted")

        return True

    return False