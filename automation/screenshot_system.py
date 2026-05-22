import pyautogui
import datetime
import os

# ==========================================
# TAKE SCREENSHOT
# ==========================================

def take_screenshot():

    screenshots_folder = "screenshots"

    os.makedirs(screenshots_folder, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = f"screenshot_{timestamp}.png"

    filepath = os.path.join(screenshots_folder, filename)

    screenshot = pyautogui.screenshot()

    screenshot.save(filepath)

    return filepath