import json
import os

COMMANDS_FILE = "data/commands.json"

# ==========================================
# LOAD COMMANDS
# ==========================================

def load_commands():

    if not os.path.exists(COMMANDS_FILE):

        return {}

    with open(COMMANDS_FILE, "r") as file:

        try:

            return json.load(file)

        except:

            return {}

# ==========================================
# SAVE COMMANDS
# ==========================================

def save_commands(commands):

    with open(COMMANDS_FILE, "w") as file:

        json.dump(commands, file, indent=4)

# ==========================================
# ADD COMMAND
# ==========================================

def add_command(trigger, action):

    commands = load_commands()

    commands[trigger.lower()] = action.lower()

    save_commands(commands)

# ==========================================
# GET COMMAND
# ==========================================

def get_command(trigger):

    commands = load_commands()

    return commands.get(trigger.lower())