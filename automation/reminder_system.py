import threading
import time
from core.voice_engine import speak

reminders = []

# ==========================================
# ADD REMINDER
# ==========================================

def add_reminder(message, seconds):

    reminder = {

        "message": message,

        "time": time.time() + seconds
    }

    reminders.append(reminder)

# ==========================================
# CHECK REMINDERS
# ==========================================

def reminder_checker():

    while True:

        current_time = time.time()

        for reminder in reminders[:]:

            if current_time >= reminder["time"]:

                speak(f"Reminder: {reminder['message']}")

                reminders.remove(reminder)

        time.sleep(1)

# ==========================================
# START REMINDER THREAD
# ==========================================

def start_reminder_system():

    thread = threading.Thread(target=reminder_checker)

    thread.daemon = True

    thread.start()