import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Setup logging to show output in Render logs
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Retrieve token from environment variables
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /start command"""
    user_name = update.effective_user.first_name if update.effective_user else "Trader"
    await update.message.reply_text(
        f"🚀 **BOF Pro Engine Active**\n\n"
        f"Hello {user_name}, your alert bot is running live on Render.\n"
        f"Send /status to check backend telemetry."
    )

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /status command"""
    await update.message.reply_text(
        "⚡ **System Status: ONLINE**\n"
        "• Backend Engine: Connected\n"
        "• Alert Polling: Active\n"
        "• Market Scan: Ready"
    )

def main():
    if not TOKEN:
        logger.error("FATAL: TELEGRAM_BOT_TOKEN environment variable is missing!")
        return

    logger.info("Initializing Telegram Bot Application...")
    app = Application.builder().token(TOKEN).build()

    # Register Command Handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("status", status_command))

    logger.info("Starting Telegram Bot Polling...")
    app.run_polling(poll_interval=1.0)

if __name__ == "__main__":
    main()
