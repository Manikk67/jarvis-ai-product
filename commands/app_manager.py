import json
import os

APPS_FILE = "data/apps.json"

# ==========================
# LOAD APPS
# ==========================

def load_apps():

    if not os.path.exists(APPS_FILE):

        return {}

    with open(APPS_FILE, "r") as file:

        try:

            return json.load(file)

        except:

            return {}

# ==========================
# SAVE APPS
# ==========================

def save_apps(apps):

    with open(APPS_FILE, "w") as file:

        json.dump(apps, file, indent=4)

# ==========================
# ADD APP
# ==========================

def add_app(app_name, app_path):

    apps = load_apps()

    apps[app_name.lower()] = app_path

    save_apps(apps)

# ==========================
# OPEN SAVED APP
# ==========================

def open_saved_app(app_name):

    apps = load_apps()

    app_name = app_name.lower()

    if app_name in apps:

        try:

            os.startfile(apps[app_name])

            return True

        except:

            return False

    return False