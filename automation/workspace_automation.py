import os
import webbrowser
import time

# ==========================================
# STUDY WORKSPACE
# ==========================================

def start_study_workspace():

    # Open Chrome
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

    try:
        os.startfile(chrome_path)
    except:
        pass

    time.sleep(2)

    # Open YouTube LoFi
    webbrowser.open(
        "https://www.youtube.com/results?search_query=lofi+study+music"
    )

    time.sleep(1)

    # Open Notepad
    os.system("start notepad")

    time.sleep(1)

    # Open Calculator
    os.system("start calc")

    time.sleep(1)

    # Open Desktop Folder
    desktop_path = os.path.join(
        os.path.expanduser("~"),
        "OneDrive",
        "Desktop"
    )

    try:
        os.startfile(desktop_path)
    except:
        pass

# ==========================================
# CODING WORKSPACE
# ==========================================

def start_coding_workspace():

    # Open Chrome
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

    try:
        os.startfile(chrome_path)
    except:
        pass

    time.sleep(2)

    # Open GitHub
    webbrowser.open("https://github.com")

    time.sleep(1)

    # Open StackOverflow
    webbrowser.open("https://stackoverflow.com")

    time.sleep(1)

    # Open Notepad
    os.system("start notepad")

    time.sleep(1)

    # Open Calculator
    os.system("start calc")