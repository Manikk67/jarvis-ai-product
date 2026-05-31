# JARVIS AI

> A secure, Telegram-first productivity assistant for Windows — automate daily tasks, launch workspaces, manage reminders, and get AI help from your phone.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?logo=windows)
![License](https://img.shields.io/badge/License-MIT-green)

---

## Overview

**JARVIS AI** is a personal productivity assistant that runs on your Windows PC and is controlled remotely via Telegram. Send a message — get things done. No technical knowledge required.

Designed for single-user daily use: system control, app launching, workspace automation, reminders, and AI assistance.

---

## Features

| Category | Capabilities |
|----------|-------------|
| **Telegram Control** | Secure remote access with password login and user ID restriction |
| **System** | Brightness, volume, screenshots, lock, shutdown, restart |
| **Files** | Open Desktop, Documents, Downloads, Pictures, Videos |
| **Apps** | Chrome, Cursor, Python, YouTube, ChatGPT, Gemini, Copilot, WhatsApp |
| **Workspaces** | One-command study or work setup (config-driven) |
| **Reminders** | Persistent reminders with natural language parsing |
| **AI** | Groq-powered explain/summarize (optional) |

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Manikk67/jarvis-ai-product.git
cd jarvis-ai-product
```

### 2. Create a virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment

```bash
copy .env.example .env
```

Edit `.env`:

```env
TELEGRAM_BOT_TOKEN=your_bot_token_from_botfather
TELEGRAM_ADMIN_USER_ID=your_telegram_user_id
TELEGRAM_PASSWORD=your_secure_password
GROQ_API_KEY=your_groq_api_key          # optional, for AI commands
ASSISTANT_NAME=Jarvis
USER_NAME=YourName
```

### 5. Run JARVIS

```bash
python main.py
```

---

## Telegram Setup

1. Open Telegram and message [@BotFather](https://t.me/BotFather)
2. Create a new bot with `/newbot` and copy the token
3. Get your Telegram user ID from [@userinfobot](https://t.me/userinfobot)
4. Add both to your `.env` file
5. Start JARVIS with `python main.py`
6. In Telegram, send `/start` then `/login your_password`
7. Send commands like `open youtube` or `study workspace`

---

## Commands

Send any of these via Telegram (aliases work too):

### System
| Command | Aliases |
|---------|---------|
| brightness up | increase brightness, brighter |
| brightness down | decrease brightness, dimmer |
| volume up | increase volume, louder |
| volume down | decrease volume, quieter |
| volume up to 50% | set volume to 30% |
| mute volume | mute, silence |
| unmute volume | unmute |
| screenshot | take screenshot, capture screen |
| open cmd | open command prompt, open terminal |
| lock computer | lock pc, lock screen |
| shutdown computer | shutdown, shutdown pc |
| restart computer | restart pc, reboot |

### Files
| Command | Aliases |
|---------|---------|
| open desktop | launch desktop |
| open documents | launch documents |
| open downloads | launch downloads |
| open pictures | launch pictures |
| open videos | launch videos |

### Apps
| Command | Aliases |
|---------|---------|
| open youtube | launch youtube, yt |
| open chatgpt | launch chatgpt |
| open gemini | launch gemini |
| open copilot | launch copilot |
| open whatsapp | launch whatsapp |
| open chrome | launch chrome |
| open cursor | launch cursor |
| open files | open file explorer |
| open python | launch python |

### Workspaces
| Command | What it opens |
|---------|---------------|
| study workspace | Documents, Chrome, ChatGPT, Notepad |
| work workspace | Chrome, ChatGPT, Gemini, WhatsApp, Files, Notepad |

### Reminders
| Command | Example |
|---------|---------|
| remind me to ... | remind me to call mom in 5 minutes |
| show reminders | list reminders |
| delete reminder | delete reminder abc123 |

### AI & Help
| Command | Description |
|---------|-------------|
| hello | Greeting |
| time | Current time |
| date | Today's date |
| motivate me | Motivational quote |
| explain ... | AI explanation (needs Groq key) |
| summarize ... | AI summary (needs Groq key) |
| help | List all commands |

---

## Workspaces

Workspaces are defined in `config/workspace_config.json`. Add new workspaces without editing code:

```json
{
  "my workspace": {
    "description": "Custom setup",
    "items": [
      {"type": "app", "target": "chrome"},
      {"type": "browser", "target": "chatgpt"},
      {"type": "folder", "target": "documents"}
    ]
  }
}
```

Item types: `app`, `browser`, `folder`

---

## Security

- **Admin-only access** — Only your Telegram user ID can use the bot
- **Password login** — `/login <password>` required before commands execute
- **No hardcoded secrets** — All credentials in `.env` (never commit this file)
- **Command whitelist** — Unknown commands are rejected safely
- **Logging** — All commands logged to `logs/jarvis.log`

If you previously exposed a Telegram token in source code, **revoke it in BotFather** and generate a new one.

---

## Configuration Files

| File | Purpose |
|------|---------|
| `config/settings.json` | App discovery, browser URLs, folder aliases |
| `config/workspace_config.json` | Workspace definitions |
| `data/app_paths.json` | Saved app paths (auto-discovered or manual) |
| `data/reminders.json` | Persistent reminders |
| `.env` | Secrets and user settings |

### App Discovery

JARVIS automatically searches for apps in:
- Program Files
- Program Files (x86)
- LocalAppData
- Start Menu shortcuts

If an app is not found, add its path manually to `data/app_paths.json`:

```json
{
  "cursor": "C:\\Users\\You\\AppData\\Local\\Programs\\cursor\\Cursor.exe"
}
```

---

## Project Structure

```
JARVIS_AI/
├── config/              # Settings and workspace templates
├── core/                # Engine, registry, Telegram bot, AI
├── commands/            # Command registration
├── automation/        # PC control, reminders, screenshots
├── data/                # Runtime user data
├── tests/               # Automated test suite
├── logs/                # Runtime logs
├── main.py              # Start Telegram bot
├── config.py            # .env loader
└── requirements.txt
```

---

## Running Tests

```bash
python -m pytest tests/ -v
```

See [test_report.md](test_report.md) for results.

---

## Screenshots

<!-- Add Telegram conversation screenshots here -->
_Screenshots coming soon — add images to `screenshots/` and link them here._

---

## Credits

**Author:** Manikandan K  
**Project:** JARVIS AI — Personal Productivity Assistant  
**License:** MIT

---

## Support

Star the repository on GitHub and report issues via GitHub Issues.
