# JARVIS AI — Project Audit Report

**Date:** 2026-05-31  
**Scope:** Full codebase analysis before product transformation

---

## 1. Folder Structure

```
JARVIS_AI/
├── main.py                      # CLI entry with duplicate command router
├── config.py                    # .env loader (GROQ_API_KEY, names unused)
├── convert_icon.py              # One-off icon utility (non-runtime)
├── requirements.txt             # Missing python-telegram-bot
├── package.json / package-lock  # Experimental Electron (broken main path)
├── core/
│   ├── jarvis_engine.py         # Command router (GUI/API)
│   ├── ai_engine.py             # Groq Llama 3.1
│   ├── voice_engine.py          # TTS + STT
│   ├── offline_brain.py         # Greetings, jokes, motivation
│   ├── live_listener.py         # Mic listener for GUI
│   ├── api_server.py            # Flask POST /jarvis (no auth)
│   └── telegram_control.py      # Orphaned bot with hardcoded secrets
├── commands/
│   ├── app_manager.py           # data/apps.json persistence
│   ├── command_memory.py        # Custom command triggers
│   ├── notes_system.py          # In-memory only (not persisted)
│   ├── study_data.py            # Static study topics
│   ├── media_commands.py        # Screenshot + volume
│   ├── system_commands.py       # Shutdown/restart/lock
│   └── workspace_commands.py    # Study/coding workspaces
├── automation/
│   ├── reminder_system.py       # In-memory reminders
│   ├── screenshot_system.py     # pyautogui screenshots
│   ├── volume_control.py        # pycaw (import-time init)
│   ├── pc_control.py            # os.system PC control
│   ├── workspace_automation.py  # Hardcoded workspace launchers
│   └── file_searcher.py         # Full C:\ walk (dangerous)
├── gui/jarvis_gui.py            # 900+ line CustomTkinter UI
├── frontend/                    # Experimental Electron UI
└── data/apps.json               # User app paths (gitignored pattern)
```

---

## 2. Architecture Overview

The project had **four parallel entry points** with **three separate command routers**:

| Entry Point | Router | Integration |
|-------------|--------|-------------|
| `main.py` CLI | Local `handle_commands` | Full features + interactive input |
| `gui/jarvis_gui.py` | `jarvis_engine.handle_commands` | Partial (blocks reminders/app memory) |
| `core/api_server.py` | `jarvis_engine.handle_commands` | No authentication |
| `core/telegram_control.py` | Separate mini-router (4 commands) | Not connected to main engine |

**Data flow (before refactor):** User input → substring-matched if/elif chain → automation modules → TTS response.

**Critical flaw:** Any new command required editing multiple files; behavior diverged between CLI and engine.

---

## 3. Dependency Analysis

### Python (requirements.txt)

| Package | Status |
|---------|--------|
| groq | Used — AI chat |
| python-dotenv | Used — config |
| pyttsx3, SpeechRecognition, PyAudio | Used — voice (CLI/GUI) |
| customtkinter | Used — GUI only |
| pyautogui | Used — screenshots |
| pycaw, comtypes | Used — Windows volume |
| flask, flask-cors | Used — optional API |
| Pillow | Used — convert_icon.py only |
| **python-telegram-bot** | **Missing** — required by telegram_control.py |

### Node.js

| Package | Status |
|---------|--------|
| electron | Experimental; package.json points to non-existent `index.js` |

### Unused config

- `ASSISTANT_NAME` and `USER_NAME` loaded but never used (hardcoded "Mani"/"Jarvis")

---

## 4. Duplicate Code

| Pattern | Locations |
|---------|-----------|
| Full command router (~400 lines) | `main.py` vs `core/jarvis_engine.py` |
| `open_apps()` + folder maps | Both routers |
| Chrome path hardcoding | Routers + workspace_automation.py |
| Speech listen logic | voice_engine vs live_listener |
| Telegram mini-router | Third duplicate of hello/youtube/time |
| User manual text | GUI + frontend/index.html |

---

## 5. Dead Code

| Item | Reason |
|------|--------|
| `core/telegram_control.py` | Not imported; not integrated |
| `convert_icon.py` | One-off utility |
| `frontend/` entire folder | Experimental, broken npm config |
| `config.ASSISTANT_NAME`, `USER_NAME` | Never read |
| `jarvis_engine.add_app` import | Never called from GUI |
| `gui/jarvis_gui.voice_active` | Set but never read |
| `notes_system.py` | In-memory only; no persistence |
| `study_data.py` | Not in product spec |
| `file_searcher.py` | Dangerous full-drive scan |
| `command_memory.py` | Experimental custom triggers |

---

## 6. Unused Modules

- `live_listener.py` — only GUI voice loop
- `api_server.py` — optional, no auth, not primary interface
- `package.json` / Electron stack — abandoned experiment

---

## 7. Broken Imports / References

| Issue | Severity |
|-------|----------|
| `telegram.ext` without package in requirements | High |
| Run from wrong cwd breaks `from core.` imports | Medium |
| Electron `main: index.js` does not exist | Medium |
| `show_notes` returns literal `\n` not newlines | Low |

---

## 8. Security Issues

| Issue | Severity |
|-------|----------|
| **Hardcoded Telegram bot token** in source | Critical |
| **Hardcoded password** `"200519"` | Critical |
| **Hardcoded admin Telegram user ID** | High |
| Flask API open on localhost with no auth | Medium |
| Electron `nodeIntegration: true`, `webSecurity: false` | Medium |
| Shutdown/restart without confirmation | Medium |
| Full C:\ file search | Medium |

---

## 9. Performance Issues

| Issue | Impact |
|-------|--------|
| `os.walk("C:\\")` file search | Can freeze system for minutes |
| pycaw initialized at import time | Slow/failing startup without audio |
| GUI voice loop always listening | Constant mic + network STT |
| Substring command matching | False positives trigger wrong actions |

---

## 10. Complexity Issues

1. **Dual routers** — maintenance burden, divergent behavior
2. **Substring matching** — `"time" in command` matches "sometimes"
3. **Recursive custom commands** — no cycle detection
4. **Hardcoded personal paths** — OneDrive Desktop, author Cursor shortcut
5. **900+ line monolithic GUI**
6. **No centralized command registry**
7. **No config-driven workspaces**

---

## 11. Feature Status (Pre-Transform)

### Working (Windows, project root, deps installed)

- CLI voice/text modes
- Groq AI chat (with API key)
- Offline greetings, jokes, motivation
- Time/date, YouTube, Google search
- Open apps/folders (hardcoded paths)
- Screenshots, volume control
- PC lock, shutdown, restart
- Study/coding workspaces (hardcoded)
- CustomTkinter GUI (partial)

### Broken / Incomplete

- Telegram bot (orphaned, missing dep, exposed secrets)
- Electron UI (broken config)
- Notes persistence (RAM only)
- Reminders persistence (RAM only)
- GUI reminders / remember app (stub messages)
- File search (works but impractical)
- Brightness control (not implemented)
- Volume set to percentage (not implemented)

---

## 12. Transformation Priorities

1. Consolidate to single command registry + engine
2. Move secrets to `.env`
3. Make Telegram the primary interface
4. Config-driven apps, workspaces, reminders
5. Remove experimental/dead code
6. Add tests and documentation

---

*Generated as Phase 1 of JARVIS AI product transformation.*
