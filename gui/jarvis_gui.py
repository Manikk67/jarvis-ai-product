import customtkinter as ctk
import threading

from core.voice_engine import speak
from core.jarvis_engine import handle_commands
from core.live_listener import listen_once

# ==========================================
# APP SETTINGS
# ==========================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ==========================================
# MAIN WINDOW
# ==========================================

app = ctk.CTk()

app.title("JARVIS AI")

app.geometry("1500x850")

# ==========================================
# GLOBAL VARIABLES
# ==========================================

voice_active = False

current_mode = "chat"

waiting_for_mode = True

# ==========================================
# SPEAK WELCOME
# ==========================================

def startup_voice():

    speak(
        "Jarvis system initialized. "
        "Welcome Mani. "
        "Please choose voice mode or chat mode."
    )

threading.Thread(
    target=startup_voice,
    daemon=True
).start()

# ==========================================
# GRID CONFIG
# ==========================================

app.grid_rowconfigure(0, weight=1)

app.grid_columnconfigure(1, weight=1)

# ==========================================
# SIDEBAR
# ==========================================

sidebar = ctk.CTkFrame(
    app,
    width=300,
    fg_color="#0f172a"
)

sidebar.grid(
    row=0,
    column=0,
    sticky="ns"
)

# ==========================================
# TITLE
# ==========================================

title = ctk.CTkLabel(
    sidebar,
    text="🤖 JARVIS",
    font=("Arial", 34, "bold"),
    text_color="#38bdf8"
)

title.pack(pady=(30, 10))

# ==========================================
# STATUS LABEL
# ==========================================

status_label = ctk.CTkLabel(
    sidebar,
    text="🟢 SYSTEM ONLINE",
    font=("Arial", 16, "bold"),
    text_color="#22c55e"
)

status_label.pack(pady=10)

# ==========================================
# MODE LABEL
# ==========================================

mode_label = ctk.CTkLabel(
    sidebar,
    text="⚡ WAITING FOR MODE",
    font=("Arial", 16, "bold"),
    text_color="#facc15"
)

mode_label.pack(pady=10)

# ==========================================
# USER MANUAL
# ==========================================

def open_manual():

    manual = ctk.CTkToplevel(app)

    manual.geometry("1000x700")

    manual.title("JARVIS USER MANUAL")

    title = ctk.CTkLabel(
        manual,
        text="📘 JARVIS USER MANUAL",
        font=("Arial", 28, "bold")
    )

    title.pack(pady=20)

    box = ctk.CTkTextbox(
        manual,
        font=("Consolas", 15)
    )

    box.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )

    manual_text = """

🚀 OVERVIEW
JARVIS is a futuristic AI desktop assistant.

⚡ COMMANDS

open youtube
take screenshot
volume up
volume down
mute volume
lock computer
study workspace
save note
show notes
find pdf
search AI news

🧠 CUSTOM COMMANDS

remember command movie

🔥 EFFECTIVE USAGE

Use short commands
Use voice for distance
Use text in noisy places

🏆 CREDITS

1. ChatGPT
2. Manikandan K

"""

    box.insert("0.0", manual_text)

# ==========================================
# MANUAL BUTTON
# ==========================================

manual_button = ctk.CTkButton(
    sidebar,
    text="📘 USER MANUAL",
    height=45,
    command=open_manual,
    fg_color="#2563eb"
)

manual_button.pack(pady=15)

# ==========================================
# HISTORY TITLE
# ==========================================

history_title = ctk.CTkLabel(
    sidebar,
    text="🕘 COMMAND HISTORY",
    font=("Arial", 18, "bold")
)

history_title.pack(pady=(20, 10))

# ==========================================
# HISTORY BOX
# ==========================================

history_box = ctk.CTkTextbox(
    sidebar,
    width=260,
    height=350,
    font=("Consolas", 13),
    fg_color="#111827"
)

history_box.pack(pady=10)

# ==========================================
# MAIN FRAME
# ==========================================

main_frame = ctk.CTkFrame(
    app,
    fg_color="#020617"
)

main_frame.grid(
    row=0,
    column=1,
    sticky="nsew"
)

main_frame.grid_rowconfigure(1, weight=1)

main_frame.grid_columnconfigure(0, weight=1)

# ==========================================
# HEADER
# ==========================================

header = ctk.CTkLabel(
    main_frame,
    text="⚡ JARVIS AI CONTROL CENTER",
    font=("Arial", 30, "bold"),
    text_color="#38bdf8"
)

header.grid(
    row=0,
    column=0,
    pady=20
)

# ==========================================
# CHAT BOX
# ==========================================

chat_box = ctk.CTkTextbox(
    main_frame,
    font=("Consolas", 16),
    fg_color="#111827",
    border_color="#38bdf8",
    border_width=2,
    corner_radius=20
)

chat_box.grid(
    row=1,
    column=0,
    sticky="nsew",
    padx=20,
    pady=20
)

chat_box.insert(
    "end",
    "🤖 Jarvis: System initialized successfully.\n\n"
)

# ==========================================
# PROCESS COMMAND
# ==========================================

def process_command(command):

    global waiting_for_mode
    global voice_active

    if not command:
        return

    command = command.lower()

    # ==========================================
    # MODE SELECTION
    # ==========================================

    if waiting_for_mode:

        chat_box.insert(
            "end",
            f"🧑 You: {command}\n\n"
        )

        if "voice" in command:

            waiting_for_mode = False

            voice_active = True

            mode_label.configure(
                text="🎤 VOICE MODE"
            )

            chat_box.insert(
                "end",
                "🤖 Jarvis: Voice mode activated.\n\n"
            )

            speak("Voice mode activated")

            return

        elif "chat" in command:

            waiting_for_mode = False

            voice_active = False

            mode_label.configure(
                text="💬 CHAT MODE"
            )

            chat_box.insert(
                "end",
                "🤖 Jarvis: Chat mode activated.\n\n"
            )

            speak("Chat mode activated")

            return

        else:

            chat_box.insert(
                "end",
                "🤖 Jarvis: Please choose voice mode or chat mode.\n\n"
            )

            return

    # ==========================================
    # NORMAL COMMANDS
    # ==========================================

    chat_box.insert(
        "end",
        f"🧑 You: {command}\n\n"
    )

    history_box.insert(
        "end",
        f"{command}\n"
    )

    chat_box.see("end")

    response = handle_commands(command)

    if response:

        chat_box.insert(
            "end",
            f"🤖 Jarvis: {response}\n\n"
        )

        chat_box.see("end")

# ==========================================
# SEND MESSAGE
# ==========================================

def send_message():

    command = entry.get()

    entry.delete(0, "end")

    process_command(command)

# ==========================================
# VOICE LOOP
# ==========================================

def voice_loop():

    while True:

        try:

            command = listen_once()

            if command:

                app.after(
                    0,
                    lambda c=command:
                    process_command(c)
                )

        except:

            pass

# ==========================================
# INPUT FRAME
# ==========================================

input_frame = ctk.CTkFrame(
    main_frame,
    fg_color="#0f172a",
    corner_radius=20
)

input_frame.grid(
    row=2,
    column=0,
    sticky="ew",
    padx=20,
    pady=20
)

input_frame.grid_columnconfigure(0, weight=1)

# ==========================================
# ENTRY BOX
# ==========================================

entry = ctk.CTkEntry(
    input_frame,
    height=55,
    font=("Arial", 18),
    placeholder_text="Type command..."
)

entry.grid(
    row=0,
    column=0,
    sticky="ew",
    padx=15,
    pady=15
)

# ==========================================
# SEND BUTTON
# ==========================================

send_button = ctk.CTkButton(
    input_frame,
    text="🚀 SEND",
    width=160,
    height=55,
    font=("Arial", 18, "bold"),
    command=send_message,
    fg_color="#2563eb"
)

send_button.grid(
    row=0,
    column=1,
    padx=15,
    pady=15
)

# ==========================================
# ENTER KEY SUPPORT
# ==========================================

entry.bind(
    "<Return>",
    lambda event: send_message()
)

# ==========================================
# START VOICE THREAD
# ==========================================

threading.Thread(
    target=voice_loop,
    daemon=True
).start()

# ==========================================
# RUN APP
# ==========================================

app.mainloop()