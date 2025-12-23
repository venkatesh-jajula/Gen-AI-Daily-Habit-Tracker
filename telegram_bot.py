import os
import httpx
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import asyncio

# Python 3.14+ fix: ensure an event loop exists in main thread
try:
    asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
API_URL = os.getenv("HABIT_API_URL", "http://127.0.0.1:8000/message")

if not BOT_TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN missing in .env")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hi! I’m HabitTracker.\n\nTry:\n- add habit no alcohol\n- tick no alcohol\n- weekly summary\n- list habits\n- today status"
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Commands:\n"
        "- add habit <name>\n"
        "- tick <name> [today/yesterday/2025-12-21]\n"
        "- weekly summary\n"
        "- list habits\n"
        "- today status / status for yesterday"
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = (update.message.text or "").strip()
    if not user_text:
        return

    payload = {"text": user_text}

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post(API_URL, json=payload)
            r.raise_for_status()
            data = r.json()
            reply = data.get("reply", "No reply returned.")
    except Exception as e:
        reply = f"Error talking to API: {e}"

    await update.message.reply_text(reply)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.run_polling()

if __name__ == "__main__":
    main()
