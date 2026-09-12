import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔥 Welcome to BOF Pro Alert Bot!\nCommands:\n/top - Show top 5 market signals\n/scan <SYMBOL> - Scan specific stock")

async def top(update: Update, context: ContextTypes.DEFAULT_TYPE):
    res = requests.get(f"{API_BASE_URL}/api/signals/fullscan").json()
    msg = "🔥 **TOP MARKET SIGNALS**\n\n"
    for item in res[:5]:
        msg += f"• *{item['symbol']}* | Score: {item['score']}/5 | {item['direction']} | Entry: ₹{item['entry']}\n"
    await update.message.reply_markdown(msg)

if __name__ == "__main__":
    app = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("top", top))
    app.run_polling()
