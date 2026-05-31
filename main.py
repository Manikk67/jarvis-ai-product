"""JARVIS AI — Telegram-first productivity assistant."""

from core.logging_config import setup_logging
from core.telegram_bot import run_bot


def main() -> None:
    setup_logging()
    run_bot()


if __name__ == "__main__":
    main()
