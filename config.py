import os
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from project root .env
_env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(_env_path)

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
ASSISTANT_NAME = os.getenv("ASSISTANT_NAME", "Jarvis")
USER_NAME = os.getenv("USER_NAME", "User")
