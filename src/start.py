from telegram import Update
from telegram.ext import ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/start command - Welcome message"""
    await update.message.reply_text(
        "Welcome! Send me a photo, and I'll turn it into anime!"
        "Made by Arabasta.")
