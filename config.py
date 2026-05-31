import os
from pathlib import Path

from dotenv import load_dotenv

_env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(_env_path)

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
ASSISTANT_NAME = os.getenv("ASSISTANT_NAME", "Jarvis")
USER_NAME = os.getenv("USER_NAME", "User")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_ADMIN_USER_ID = int(os.getenv("TELEGRAM_ADMIN_USER_ID", "0"))
TELEGRAM_PASSWORD = os.getenv("TELEGRAM_PASSWORD", "")
