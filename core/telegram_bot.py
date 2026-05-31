"""Secure Telegram bot — primary JARVIS interface."""

import logging
import urllib.parse
import urllib.request

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

import config
from automation.reminder_system import start_reminder_system
from commands.register_commands import register_all_commands
from core.command_registry import is_whitelisted
from core.jarvis_engine import handle_commands
from core.logging_config import setup_logging

logger = logging.getLogger(__name__)

logged_in_users: set[int] = set()


def _is_admin(user_id: int) -> bool:
    return user_id == config.TELEGRAM_ADMIN_USER_ID


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id

    if not _is_admin(user_id):
        logger.warning("Unauthorized /start from user %s", user_id)
        await update.message.reply_text("Unauthorized user.")
        return

    await update.message.reply_text(
        "JARVIS Security System Active\n\n"
        "Use: /login <password>\n"
        "Then send any command like: open youtube, study workspace, help"
    )


async def login_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id

    if not _is_admin(user_id):
        await update.message.reply_text("Access denied.")
        return

    if not context.args:
        await update.message.reply_text("Usage: /login <password>")
        return

    if context.args[0] == config.TELEGRAM_PASSWORD:
        logged_in_users.add(user_id)
        logger.info("User %s logged in", user_id)
        await update.message.reply_text("Login successful. JARVIS remote control enabled.")
    else:
        logger.warning("Failed login attempt from user %s", user_id)
        await update.message.reply_text("Wrong password.")


async def logout_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    logged_in_users.discard(user_id)
    await update.message.reply_text("Logged out.")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id

    if not _is_admin(user_id) or user_id not in logged_in_users:
        await update.message.reply_text("Please login first: /login <password>")
        return

    response = handle_commands("help")
    await update.message.reply_text(response)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    text = update.message.text.strip()

    if not _is_admin(user_id):
        logger.warning("Blocked unauthorized message from user %s", user_id)
        await update.message.reply_text("Unauthorized access.")
        return

    if user_id not in logged_in_users:
        await update.message.reply_text("Please login first: /login <password>")
        return

    if not is_whitelisted(text) and not text.lower().startswith(("explain", "summarize", "what", "how", "tell")):
        logger.info("Non-whitelisted command attempt: %s", text)

    logger.info("Telegram command from %s: %s", user_id, text)

    try:
        response = handle_commands(text)
        await update.message.reply_text(response)
    except Exception as exc:
        logger.exception("Telegram handler error")
        await update.message.reply_text(f"Error: {exc}")


def _send_telegram_message(text: str) -> None:
    """Send a message to the admin user (best-effort, for reminders)."""
    if not config.TELEGRAM_BOT_TOKEN or not config.TELEGRAM_ADMIN_USER_ID:
        return

    try:
        data = urllib.parse.urlencode({
            "chat_id": config.TELEGRAM_ADMIN_USER_ID,
            "text": text,
        }).encode()
        url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
        urllib.request.urlopen(url, data=data, timeout=10)
    except Exception as exc:
        logger.warning("Could not send Telegram notification: %s", exc)


def _reminder_notify(message: str) -> None:
    logger.info("Reminder triggered: %s", message)
    _send_telegram_message(message)


def run_bot() -> None:
    setup_logging()
    register_all_commands()

    if not config.TELEGRAM_BOT_TOKEN:
        raise SystemExit(
            "TELEGRAM_BOT_TOKEN not set. Copy .env.example to .env and configure it."
        )

    if not config.TELEGRAM_ADMIN_USER_ID:
        raise SystemExit("TELEGRAM_ADMIN_USER_ID not set in .env")

    start_reminder_system(on_trigger=_reminder_notify)

    app = (
        Application.builder()
        .token(config.TELEGRAM_BOT_TOKEN)
        .build()
    )

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("login", login_command))
    app.add_handler(CommandHandler("logout", logout_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Starting JARVIS Telegram bot...")
    print("JARVIS AI — Telegram bot running. Press Ctrl+C to stop.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)
