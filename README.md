# 🤖 JARVIS AI

> A futuristic Python desktop AI assistant for Windows — voice control, smart chat, automation, and a modern GUI.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?logo=windows)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📖 Overview

**JARVIS AI** is a personal desktop assistant inspired by Iron Man's JARVIS. It combines offline responses, Groq-powered AI chat (Llama 3.1), speech recognition, text-to-speech, and Windows automation in one project.

Use it from the **terminal** (`main.py`) or the **graphical interface** (`gui/jarvis_gui.py`).

---

## ✨ Features

| Category | Capabilities |
|----------|--------------|
| 🎤 **Voice** | Listen via microphone, speak responses with TTS |
| 💬 **AI Chat** | Groq API (Llama 3.1 8B instant) for open-ended questions |
| 🧠 **Offline** | Greetings, jokes, motivation without internet |
| 🖥️ **System** | Open apps/folders, volume, screenshots, PC control |
| 📝 **Productivity** | Notes, reminders, custom commands, file search |
| 🎓 **Study** | Built-in study topics (`teach me …`) |
| 🎨 **GUI** | Dark-themed CustomTkinter desktop app |

---

## 📸 Screenshots

<!-- Add your screenshots here after release -->
<!-- ![JARVIS GUI](screenshots/gui_preview.png) -->

_Screenshots coming soon — place images in `screenshots/` and link them here._

---

## 🛠️ Technologies Used

- **Python 3.9+**
- **Groq** — LLM API
- **CustomTkinter** — GUI
- **pyttsx3** — Text-to-speech
- **SpeechRecognition** — Voice input (Google STT)
- **PyAutoGUI** — Screenshots
- **pycaw** — Windows volume control
- **Flask** — Optional REST API (`core/api_server.py`)
- **PyInstaller** — Windows `.exe` builds

---

## 📁 Project Structure

```
JARVIS_AI/
├── automation/          # Reminders, screenshots, volume, PC control
├── commands/            # Apps, notes, media, system, workspace handlers
├── core/                # AI, voice, offline brain, engine, API server
├── gui/                 # CustomTkinter desktop UI
├── data/                # User JSON storage (gitignored at runtime)
├── screenshots/         # Saved screenshots (gitignored)
├── main.py              # CLI entry (voice + text mode)
├── config.py            # Loads settings from .env
├── requirements.txt
├── jarvis.ico           # App icon
├── README.md
└── LICENSE
```

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/Manikk67/jarvis-ai.git
cd jarvis-ai
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> **Note:** On Windows, if `PyAudio` fails to install, try:
> `pip install pipwin && pipwin install pyaudio`

### 4. Configure environment variables

```bash
copy .env.example .env
```

Edit `.env` and add your [Groq API key](https://console.groq.com/):

```env
GROQ_API_KEY=your_groq_api_key_here
ASSISTANT_NAME=Jarvis
USER_NAME=YourName
```

---

## ▶️ Run Commands

### CLI assistant (voice or text)

```bash
python main.py
```

### GUI desktop app

```bash
python gui/jarvis_gui.py
```

### Optional Flask API (localhost:5000)

```bash
python core/api_server.py
```

---

## 📦 Build Windows EXE (PyInstaller)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=jarvis.ico gui/jarvis_gui.py
```

The executable is created in `dist/` (ignored by git).

---

## 🗣️ Example Commands

| Say / type | Action |
|-------------|--------|
| `what time is it` | Current time |
| `today's date` | Current date |
| `open chrome` | Launch Chrome |
| `open desktop` | Open Desktop folder |
| `search python tutorials` | Google search |
| `youtube` | Open YouTube |
| `take screenshot` | Save PNG to `screenshots/` |
| `volume up` / `volume down` | Adjust system volume |
| `save note buy milk` | Save a note |
| `show notes` | Read saved notes |
| `remind me` | Set a timed reminder |
| `teach me loops` | Study mode topic |
| `hello` / `joke` | Offline responses |
| `exit` | Quit JARVIS |

---

## 🔐 Security

- **Never commit** `.env` or API keys.
- If a key was ever exposed in code or git history, **rotate it** in the Groq console.
- User-specific paths live in `data/*.json` (gitignored).

---

## 🔮 Future Plans

- [ ] Cross-platform support (macOS / Linux)
- [ ] Wake-word detection ("Hey Jarvis")
- [ ] Plugin system for custom commands
- [ ] Cloud sync for notes and reminders
- [ ] Multi-language voice support
- [ ] Settings panel in GUI

---

## 👤 Credits

**Author:** Manikandan K  
**Project:** JARVIS AI — Personal Desktop Assistant  
**License:** MIT

---

## ⭐ Support

If you find this project useful, star the repository on GitHub and share feedback via Issues!
